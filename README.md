# ULID with sequence
Universally Unique Lexicographically Sortable Identifiers (ULIDs) with sequence in Python
are intended for use as surrogate keys:
* in high performance databases of any type,
* in [Anchor Modeling](https://en.wikipedia.org/wiki/Anchor_modeling) technique.
## Advantages over UUID and GUID
* Best performance for searching and CRUD operations due to lack of data fragmentation (see evidence in article ["GUIDs as fast primary keys under multiple databases"](https://www.codeproject.com/Articles/388157/GUIDs-as-fast-primary-keys-under-multiple-database) and in [Russian translation](http://www.interface.ru/home.asp?artId=29255))
* Independence of MAC address (information security and also no risk of collisions because of possible duplication of MAC addresses)
* Copying in one click
* Shorter string representation
* Readability
## Specification
[This specification](https://github.com/ahawker/ulid/issues/306#issuecomment-451850395) is used:

ULID with sequence is calculated as

    ttttttttttsssrrrrrrrrrrrrr

    where

    t is Timestamp (10 characters or 48 bit), UNIX-time in milliseconds (UTC)
    s is Sequence (3 characters or 15 bit), generated for each ULID with the same database and Timestamp
    r is Randomness (13 characters or 65 bit), generated in advance by true random number generator, separately for each ULID

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
* Multithreading
* New ULID data type in DBMS: ID(timestamp_length, sequence_length, randomness_length). The lengths of the parts must be expressed in bits. Default values: 48, 15, and 65
* C ++ implementation
* True randomness

