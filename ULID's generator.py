import time
import base32_crockford
import secrets


def ulid(used_ulid):
    if not used_ulid:
        new_sequence = 0
        old_timestamp = 0
    while new_sequence <= 32767:  # serial search of new_sequence
        new_timestamp = int(round(time.time() * 1000))  # timestamp calculation
        new_randomness = secrets.randbits(65)  # randomness calculation
        if old_timestamp == new_timestamp:  # within a millisecond
            new_sequence += 1  # sequence increment
        else:  # new millisecond
            new_sequence = 0
        yield(base32_crockford.encode(new_timestamp).zfill(10) +
              base32_crockford.encode(new_sequence).zfill(3) +
              base32_crockford.encode(new_randomness).zfill(13))
        old_timestamp = new_timestamp
    else:
        while old_timestamp == int(round(time.time() * 1000)):
            pass
        ulid(used_ulid)


def benchmark():
    duration = float(input('Please enter test duration in seconds: '))
    start_time = time.time()
    counter = 1
    end_time = start_time + duration
    used_ulid = False
    take_ulid = ulid(used_ulid)
    print('First ULID:', next(take_ulid))
    while time.time() <= end_time:
        print(next(take_ulid))
        counter += 1
    print('Last  ULID:', next(take_ulid))
    print('Seconds per ULID:', duration / counter)
    print('Number of ULIDs per second:', counter / duration)


benchmark()
