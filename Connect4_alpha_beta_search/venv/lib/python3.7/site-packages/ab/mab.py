from typing import List, Tuple, Dict
import logging
import random

from ab import store

NAMESPACE = 'mab'
KEY_TRIALS = 'trials'
KEY_SUCCESSES = 'successes'

# 10% explore, 90% exploit
RATE = .1


# PUBLIC

def get_bucket(test: str, buckets: List[str], rate: float = RATE) -> str:
    """Obtain a bucket for a test with multi-arm bandit strategy."""
    assert_explore_rate(rate)
    assert_buckets(buckets)
    chance = random.random()  # 0.0-1.0
    if chance <= rate:
        return explore(test, buckets)
    return exploit(test, buckets)


def success(test: str, bucket: str):
    """Mark a trial success for a test."""
    try:
        return store.incr(format_key(test, bucket, KEY_SUCCESSES))
    except store.StoreError as e:
        logging.exception(e)
        return None


class MABTestError(Exception):
    pass


# PRIVATE


def assert_explore_rate(rate: float):
    if 0.0 < rate > 1.0:
        message = f'Explore rate must be between 0.0 and 1.0 (saw: {rate})'
        raise MABTestError(message)


def assert_buckets(buckets: List[str]):
    if len(buckets) < 2:
        raise MABTestError(f'Must have two or more buckets (saw {buckets})')


def format_key(test: str, bucket: str, key: str) -> str:
    return f'{NAMESPACE}:{test}:{bucket}:{key}'


def trial(test: str, bucket: str):
    return store.incr(format_key(test, bucket, KEY_TRIALS))


def get_state(test: str, buckets: List[str]) -> Dict[str, int]:
    keys = []
    for bucket in buckets:
        keys.append(format_key(test, bucket, KEY_TRIALS))
        keys.append(format_key(test, bucket, KEY_SUCCESSES))
    payload = store.mget(keys)
    data, index = {}, 0
    for bucket in buckets:
        data[bucket] = {
            KEY_TRIALS: int(payload[index] or 0),
            KEY_SUCCESSES: int(payload[index + 1] or 0)}
        index += 2
    return data


def get_state_with_tuples(
        test: str, buckets: List[str]) -> Dict[str, Tuple[int, int]]:
    return {bucket: (item[KEY_TRIALS], item[KEY_SUCCESSES])
            for bucket, item in get_state(test, buckets).items()}


def get_scores(test: str, buckets: List[str]) -> Dict[str, int]:
    return {key: stats[KEY_SUCCESSES] / (stats[KEY_TRIALS] or 1)
            for key, stats in get_state(test, buckets).items()}


def explore(test: str, buckets: List[str]) -> str:
    bucket = random.choice(buckets)
    trial(test, bucket)
    return bucket


def exploit(test: str, buckets: List[str]) -> str:
    # TODO(DAN): use stats.get_results() to pick optimal bucket.
    scores = get_scores(test, buckets)

    # If all buckets are even, explore.
    if len(set(scores.values())) == 1:
        return explore(test, buckets)

    # Exploit leading bucket.
    bucket = max(scores, key=scores.get)
    trial(test, bucket)
    return bucket
