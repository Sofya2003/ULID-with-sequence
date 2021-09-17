# ULID with sequence
Universally Unique Lexicographically Sortable Identifiers (ULIDs) with sequence in Python
are intended for use as surrogate keys:
* in high performance databases of any type,
* in [Anchor Modeling](https://en.wikipedia.org/wiki/Anchor_modeling) technique.
## Advantages over UUID and GUID
* Best performance for searching and CRUD operations due to lack of data fragmentation (see Benchmarks of sequential UUID below)
* Independence of MAC address (information security and also no risk of collisions because of possible duplication of MAC addresses)
* Copying in one click
* Shorter string representation
* Readability
## Benchmarks of sequential UUID
* [Choosing a Fast Unique Identifier (UUID) for Lucene](https://dzone.com/articles/choosing-fast-unique)
* [Storing UUID Values in MySQL](https://www.percona.com/blog/2014/12/19/store-uuid-optimized-way/)
* [Sequential UUID Generators](https://www.2ndquadrant.com/en/blog/sequential-uuid-generators/)
* [MySQL Performance When Using UUID For Primary Key](https://blog.programster.org/mysql-performance-when-using-uuid-for-primary-key)
* [GUIDs as fast primary keys under multiple databases](https://www.codeproject.com/Articles/388157/GUIDs-as-fast-primary-keys-under-multiple-database)
* [Первичный ключ – GUID или автоинкремент? (Russian)](https://habr.com/ru/post/265437/)
* [Первичный ключ – GUID или автоинкремент? Часть вторая (Russian)](https://habr.com/ru/post/268605/)
* [SQL ключи во всех подробностях (Russian)](https://habr.com/ru/company/oleg-bunin/blog/348172/#uuid)
* [GUID в роли быстрого первичного ключа для разных БД (Russian)](http://www.interface.ru/home.asp?artId=29255)
## Specification
[This specification](https://github.com/ahawker/ulid/issues/306#issuecomment-451850395) is used:

ULID with sequence is calculated as

    ttttttttttsssrrrrrrrrrrrrr (implemented)
    or
    ttttttttttsssrrrrrrrrrrrxx (planned)

    where

    t is Clock sequence (10 characters or 48 bits), UNIX-time (UTC) in milliseconds, big-endian
    s is Sequence (3 characters or 15 bits), generated for each ULID with the same database table and Timestamp
    r is Randomness (13/11 characters or 65/55 bits), generated in advance by quantum-mechanical TRNG or CSPRNG, separately for each ULID
    x is Entity type (2 characters or 10 bits), pointing to one database table with ULID as a primary key




    Long ULID for high-load critical systems and IoT (planned):

    160 bits or 32 characters in Crockford's base32
    0        1         2         3 
    12345678901234567890123456789012
    nnnnnnnnnnnnsssrrrrrrrrrrrrrrrxx

    n is Timestamp (12 characters or 60 bits), UNIX-time (UTC) in 100 ns resolution, big-endian (the same as timestamp in UUID version 1)
    s is Clock sequence (Count) (3 characters or 15 bits), generated for each ULID with the same database table and Timestamp.
         On overflow ULIDs with the maximum Clock sequence number should be generated until the Timestamp changes
    r is Randomness (15 characters or 75 bits), generated in advance by quantum-mechanical TRNG or CSPRNG, unique for each ULID
         Last several characters of Randomness may be populated with shard/partition and/or implementation defined ID (for example, hash) of ULID generator
    x is Local entity type (2 characters or 10 bits), pointing to one database table with long ULID as a primary key, 
         specifically to anchor in Anchor modeling, hub in Data vault modeling, dimension table in Star schema.
         In Anchor modeling the anchor name prefix must match the local entity type

    Strict monotonicity is not guaranteed, especially for the leap second. Therefore ULID should never be used for creation of a clustered index.

    The 8-4-4-4-12 format of UUID with 4 hyphens may only be used in textual representation for backward compatibility:
    nnnnnnnn-nnnn-sssr-rrrr-rrrrrrrrrrxx

    But string format without hyphens is preferable.

    The storage format (text, binary, UUID, integer, byte array, JSONB) in the database depends on the DBMS and implementation, and it is not prescribed.

The string representation in [Crockford's base32](https://www.crockford.com/base32.html) is used.
## Implementation
The binary format has not been implemented. The implemented string format is great for PostgreSQL and MySQL and satisfactory for Oracle.

Cryptographically secure Python Secrets module is used to generate random part instead of old Python Random module.
## Usage
next(ulid)
## Test
benchmark()

The performance is about 5000 ULIDs per second on ordinary PC.
## Prior Art
[The canonical specification for ULID](https://github.com/ulid/spec) was [modified](https://github.com/ahawker/ulid/issues/306#issuecomment-451850395) by adding of three-character sequence for increasing ULIDs within a millisecond.

The modified specification is more secure, because it's impossible to find a valid ULID by increment or decrement of the known ULID.
## Future improvements
* Calculation of random parts in advance
* Ability to shift the date and time in timestamp of ULIDs for each database table separately (for information security reasons)
* Multithreading (see Multithreading in database below)
* New ULID data type in DBMS named ID
* C, C++ or Rust implementation
* True randomness
## Multithreading in database
This problem should be solved in approximately the same way as for auto increment primary key, i.e. separately for each table with surrogate primary key. That is, when writing to the table, the separate instance of the ULID generator must be created for this table. If within one calendar millisecond or longer there were no requests for generating ULIDs, then this instance of the generator should be destroyed.

If the table record is received from an external source, then, in addition to the ULID generated by the database, the record should contain an initial identifier from the external source (for reconciliation, data exchange, etc.). Therefore, you do not have to sort records received from external sources in accordance with received theirs ULIDs.
## References
[Comment on habr.com (Russian)](https://habr.com/ru/post/572700/comments/#comment_23418560)
