# ULID with sequence
Universally Unique Lexicographically Sortable Identifiers (ULIDs) with sequence in Python
are intended for use as surrogate keys in high performance databases of any type.
## Specification
[This specification](https://github.com/ahawker/ulid/issues/306#issuecomment-451850395) is used:

ULID with sequence is calculated as

    ttttttttttsssrrrrrrrrrrrrr

    where

    t is Timestamp (10 characters), UNIX-time in milliseconds (UTC)
    s is Sequence (3 characters), generated for each ULID with the same database and Timestamp
    r is Randomness (13 characters), generated in advance by true random number generator, separately for each ULID

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
