from typing import List, Dict
import collections
import hashlib

HASH_LEN = 16
MAX_HASH = HASH_LEN**40
HASH_ENCODING = 'utf-8'


# PUBLIC

def get_bucket(value, test: str, buckets: List[str]) -> str:
    """Given a value for a unique test name, determine the bucket.
    Test name is factored into allocation to ensure allocations
    are unique. Without this, user_id 1 could always end up in the
    same bucket, every time you ran a new experiment.
    """
    buckets_len = len(buckets)
    test_name_hash = hash_value(test)
    input_value = f'{value}{test_name_hash}'
    allocation = calc(input_value, buckets_len)
    return buckets[allocation]


class ABTestError(Exception):
    pass


# PRIVATE


def assert_buckets(buckets: int):
    if buckets < 2:
        raise ABTestError(f'Must have two or more buckets (saw {buckets})')


def assert_value(value):
    if not isinstance(value, (int, str)):
        value_type = type(value)
        raise ABTestError(f'Value must be a string or int (saw {value_type})')


def hash_value(value) -> int:
    assert_value(value)
    safe_value = str(value).encode(HASH_ENCODING)
    return int(hashlib.sha1(safe_value).hexdigest(), HASH_LEN)


def calc(value, buckets: int) -> int:
    """Given a value, calculate the bucket index."""
    assert_buckets(buckets)
    val_hash = hash_value(value)
    div = MAX_HASH / buckets
    return int(float(val_hash / div))


def allocate(values, buckets: int) -> Dict[str, str]:
    """Allocate values into named buckets by index.
    This is useful for verifying that distribution is even.
    """
    allocations = collections.defaultdict(int)
    for i in values:
        bucket = calc(i, buckets)
        allocations[bucket] += 1
    return allocations
