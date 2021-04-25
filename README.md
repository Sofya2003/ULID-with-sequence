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

    t is Timestamp (10 characters or 48 bit), UNIX-time in milliseconds (UTC)
    s is Sequence (3 characters or 15 bit), generated for each ULID with the same database and Timestamp
    r is Randomness (13/11 characters or 65/55 bit), generated in advance by true random number generator, separately for each ULID
    x is Entity type (2 characters or 10 bit), corresponding to the database tables

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

