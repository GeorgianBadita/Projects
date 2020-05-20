import random
import collections
import unittest
from unittest import mock

from ab import store_mock
from ab import mab
from ab import stats


class MultiArmedBanditTestCase(unittest.TestCase):

    def test_trial(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            self.assertEqual(mab.trial('my_test_v1', 'control'), 1)
            self.assertEqual(mab.trial('my_test_v1', 'control'), 2)

    def test_success(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            self.assertEqual(mab.success('my_test_v1', 'control'), 1)
            self.assertEqual(mab.success('my_test_v1', 'control'), 2)

    def test_get_state_default(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            data = mab.get_state(test_name, buckets)
            self.assertEqual(list(data.keys()), buckets)
            self.assertEqual(data['control'][mab.KEY_TRIALS], 0)
            self.assertEqual(data['control'][mab.KEY_SUCCESSES], 0)
            self.assertEqual(data['variant1'][mab.KEY_TRIALS], 0)
            self.assertEqual(data['variant1'][mab.KEY_SUCCESSES], 0)
            self.assertEqual(data['variant2'][mab.KEY_TRIALS], 0)
            self.assertEqual(data['variant2'][mab.KEY_SUCCESSES], 0)

    def test_get_state_with_tuples_default(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            data = mab.get_state_with_tuples(test_name, buckets)
            self.assertEqual(list(data.keys()), buckets)
            self.assertEqual(data['control'][0], 0)
            self.assertEqual(data['control'][1], 0)
            self.assertEqual(data['variant1'][0], 0)
            self.assertEqual(data['variant1'][1], 0)
            self.assertEqual(data['variant2'][0], 0)
            self.assertEqual(data['variant2'][1], 0)

    def test_get_state_used(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            mab.trial('my_test_v1', 'control')
            mab.trial('my_test_v1', 'control')
            mab.success('my_test_v1', 'control')
            mab.success('my_test_v1', 'control')
            mab.trial('my_test_v1', 'variant1')
            mab.success('my_test_v1', 'variant1')
            mab.trial('my_test_v1', 'variant2')
            data = mab.get_state(test_name, buckets)
            self.assertEqual(list(data.keys()), buckets)
            self.assertEqual(data['control'][mab.KEY_TRIALS], 2)
            self.assertEqual(data['control'][mab.KEY_SUCCESSES], 2)
            self.assertEqual(data['variant1'][mab.KEY_TRIALS], 1)
            self.assertEqual(data['variant1'][mab.KEY_SUCCESSES], 1)
            self.assertEqual(data['variant2'][mab.KEY_TRIALS], 1)
            self.assertEqual(data['variant2'][mab.KEY_SUCCESSES], 0)

    def test_get_state_with_tuples_used(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            mab.trial('my_test_v1', 'control')
            mab.trial('my_test_v1', 'control')
            mab.success('my_test_v1', 'control')
            mab.success('my_test_v1', 'control')
            mab.trial('my_test_v1', 'variant1')
            mab.success('my_test_v1', 'variant1')
            mab.trial('my_test_v1', 'variant2')
            data = mab.get_state_with_tuples(test_name, buckets)
            self.assertEqual(list(data.keys()), buckets)
            self.assertEqual(data['control'][0], 2)
            self.assertEqual(data['control'][1], 2)
            self.assertEqual(data['variant1'][0], 1)
            self.assertEqual(data['variant1'][1], 1)
            self.assertEqual(data['variant2'][0], 1)
            self.assertEqual(data['variant2'][1], 0)

    def test_cold_start_exploit_explores(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 275)
            self.assertGreaterEqual(seen['variant1'], 275)
            self.assertGreaterEqual(seen['variant2'], 275)
            self.assertEqual(sum(seen.values()), 1000)

    def test_exploit_variant_1_single_trial_still_exploring(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            mab.trial(test_name, 'variant1')  # first trial with no success
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 275)
            self.assertGreaterEqual(seen['variant1'], 275)
            self.assertGreaterEqual(seen['variant2'], 275)
            self.assertEqual(sum(seen.values()), 1000)

    def test_exploit_variant_1_three_trials_still_exploring(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            mab.trial(test_name, 'variant1')  # first trial with no success
            mab.trial(test_name, 'variant1')  # second trial with no success
            mab.trial(test_name, 'variant1')  # third trial with no success
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 250)
            self.assertGreaterEqual(seen['variant1'], 250)
            self.assertGreaterEqual(seen['variant2'], 250)
            self.assertEqual(sum(seen.values()), 1000)

    def test_exploit_variant_1_one_trial_with_begins_exploitation(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            mab.trial(test_name, 'variant1')
            mab.success(test_name, 'variant1')  # first trial with success
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 10)
            self.assertGreaterEqual(seen['variant1'], 850)
            self.assertGreaterEqual(seen['variant2'], 10)
            self.assertEqual(sum(seen.values()), 1000)

    def test_exploit_two_variants_with_success(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            mab.trial(test_name, 'variant1')
            mab.success(test_name, 'variant1')  # first trial with success
            mab.trial(test_name, 'variant2')
            mab.success(test_name, 'variant2')  # other trial with success
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 10)
            self.assertGreaterEqual(seen['variant1'], 400)
            self.assertGreaterEqual(seen['variant2'], 400)
            self.assertEqual(sum(seen.values()), 1000)

    def test_exploit_all_buckets_with_success(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            mab.trial(test_name, 'control')
            mab.success(test_name, 'control')  # first trial with success
            mab.trial(test_name, 'variant1')
            mab.success(test_name, 'variant1')  # second trial with success
            mab.trial(test_name, 'variant2')
            mab.success(test_name, 'variant2')  # third trial with success
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 250)
            self.assertGreaterEqual(seen['variant1'], 250)
            self.assertGreaterEqual(seen['variant2'], 250)
            self.assertEqual(sum(seen.values()), 1000)

    def test_variant_dominates(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            for x in range(3):  # poor showing, control...
                mab.trial(test_name, 'control')
                mab.success(test_name, 'control')
            for x in range(9):  # Not bad, variant1...
                mab.trial(test_name, 'variant2')
                mab.success(test_name, 'variant2')
            for x in range(100):  # Variant2 leading the way.
                mab.trial(test_name, 'variant2')
                mab.success(test_name, 'variant2')
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 15)
            self.assertLessEqual(seen['control'], 75)
            self.assertGreaterEqual(seen['variant1'], 15)
            self.assertLessEqual(seen['variant1'], 75)
            self.assertGreaterEqual(seen['variant2'], 850)
            self.assertLessEqual(seen['variant2'], 990)
            self.assertEqual(sum(seen.values()), 1000)

    def test_variant_dominates_low_exploration(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            seen = collections.Counter()
            for x in range(3):  # poor showing, control...
                mab.trial(test_name, 'control')
                mab.success(test_name, 'control')
            for x in range(9):  # Not bad, variant1...
                mab.trial(test_name, 'variant2')
                mab.success(test_name, 'variant2')
            for x in range(100):  # Variant2 leading the way.
                mab.trial(test_name, 'variant2')
                mab.success(test_name, 'variant2')
            for x in range(1000):
                bucket = mab.get_bucket(test_name, buckets, rate=.05)
                seen[bucket] += 1
                self.assertTrue(bucket in buckets)
            self.assertGreaterEqual(seen['control'], 5)
            self.assertLessEqual(seen['control'], 75)
            self.assertGreaterEqual(seen['variant1'], 5)
            self.assertLessEqual(seen['variant1'], 75)
            self.assertGreaterEqual(seen['variant2'], 900)
            self.assertLessEqual(seen['variant2'], 990)
            self.assertEqual(sum(seen.values()), 1000)

    # I stress tested this and it always seems to pass.
    # If it breaks, enable this because random is random.
    # @unittest.skip('comment & run: make stress_test_mab')
    def test_simulate_experiment(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            # Trying to simulate random 30% trial, random 10% success rate.
            for x in range(10000):
                # ~30% in trial
                if random.random() <= .3:
                    bucket = mab.get_bucket(test_name, buckets)
                    # ~10% of trial members succeed.
                    if random.random() <= .1:
                        mab.success(test_name, bucket)
            scores = mab.get_scores(test_name, buckets)
            # Leaving headroom for random
            self.assertLessEqual(scores['control'], .15)
            self.assertGreaterEqual(scores['control'], .01)
            self.assertLessEqual(scores['variant1'], .15)
            self.assertGreaterEqual(scores['variant1'], .01)
            self.assertLessEqual(scores['variant2'], .15)
            self.assertGreaterEqual(scores['variant2'], .01)
            state = mab.get_state_with_tuples(test_name, buckets)
            results = stats.get_results(state)
            self.assertGreaterEqual(results['variant1'].p_value, 0.0)
            self.assertLessEqual(results['variant1'].p_value, 0.5)

    # I stress tested this and it always seems to pass.
    # If it breaks, enable this because random is random.
    # @unittest.skip('comment & run: make stress_test_mab')
    def test_simulate_experiment_variant1_outperforms(self):
        with mock.patch('ab.store.get') as store_patch:
            store_patch.return_value = store_mock.MockRedis()
            test_name = 'my_test_v1'
            buckets = ['control', 'variant1', 'variant2']
            # Trying to simulate random 30% trial, random 10% success rate.
            for x in range(10000):
                if random.random() <= .3:  # ~30% in trial
                    bucket = mab.get_bucket(test_name, buckets)
                    # Variant 1 outperforming at ~30% success rate
                    success_chance = random.random()
                    if bucket == 'variant1' and success_chance <= .3:
                        mab.success(test_name, bucket)
                    # Only 5% of control and variant 2 members succeed.
                    elif success_chance <= .05:
                        mab.success(test_name, bucket)
            scores = mab.get_scores(test_name, buckets)
            self.assertGreaterEqual(scores['control'], .0)
            self.assertLessEqual(scores['control'], .15)
            # Variant 1 consistently does better.
            self.assertGreaterEqual(scores['variant1'], .15)
            self.assertLessEqual(scores['variant1'], .35)
            self.assertGreaterEqual(scores['variant2'], .0)
            self.assertLessEqual(scores['variant2'], .15)
            state = mab.get_state_with_tuples(test_name, buckets)
            results = stats.get_results(state)
            self.assertTrue(results['variant1'].is_better_than_control)
            self.assertTrue(results['variant1'].is_significant)
            self.assertGreaterEqual(results['variant1'].p_value, 0.0)
            self.assertLessEqual(results['variant1'].p_value, 0.001)
