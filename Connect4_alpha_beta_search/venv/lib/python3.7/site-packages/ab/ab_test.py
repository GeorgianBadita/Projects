import collections
import uuid
import unittest

from ab import ab


class ABTestCase(unittest.TestCase):

    def test_calc_none_bucket(self):
        with self.assertRaisesRegex(ab.ABTestError, "saw <class 'NoneType'>"):
            ab.calc(None, buckets=2)

    def test_calc_negative_bucket(self):
        with self.assertRaisesRegex(ab.ABTestError, 'saw -1'):
            ab.calc(0, buckets=-1)

    def test_calc_0_bucket(self):
        with self.assertRaisesRegex(ab.ABTestError, 'saw 0'):
            ab.calc(0, buckets=0)

    def test_calc_1_bucket(self):
        with self.assertRaisesRegex(ab.ABTestError, 'saw 1'):
            ab.calc(0, buckets=1)

    def test_calc_zero_2_buckets(self):
        self.assertEqual(ab.calc(0, buckets=2), 1)

    def test_calc_2_buckets(self):
        self.assertEqual(ab.calc(99, buckets=2), 1)
        self.assertEqual(ab.calc(98, buckets=2), 0)

    def test_calc_3_buckets(self):
        self.assertEqual(ab.calc(99, buckets=3), 1)
        self.assertEqual(ab.calc(98, buckets=3), 0)

    def test_calc_100_buckets(self):
        self.assertEqual(ab.calc(99, buckets=100), 60)

    def test_100_users(self):
        user_ids = list(range(100))
        allocations = ab.allocate(user_ids, buckets=2)
        allocation_keys = sorted([int(k) for k in allocations.keys()])
        self.assertEqual(allocation_keys, list(range(0, 2)))
        self.assertEqual(allocations[0], 43)
        self.assertEqual(allocations[1], 57)

    def test_1000_users(self):
        user_ids = list(range(1000))
        allocations = ab.allocate(user_ids, buckets=2)
        allocation_keys = sorted([int(k) for k in allocations.keys()])
        self.assertEqual(allocation_keys, list(range(0, 2)))
        self.assertEqual(allocations[0], 481)
        self.assertEqual(allocations[1], 519)

    def test_one_million_emails(self):
        emails = [str(uuid.uuid4()) for i in range(1000000)]
        allocations = ab.allocate(emails, buckets=100)
        allocation_keys = sorted([int(k) for k in allocations.keys()])
        self.assertEqual(allocation_keys, list(range(0, 100)))
        for value in allocations.values():
            int_value = int(value)
            self.assertGreaterEqual(int_value, 9500)
            self.assertLessEqual(int_value, 10500)

    def test_get_bucket_example(self):
        user_id = 1
        test_name = 'my_test_v1'
        buckets = ['control', 'variant1', 'variant2']
        allocation = ab.get_bucket(user_id, test=test_name, buckets=buckets)
        self.assertEqual(allocation, 'control')

    def test_get_bucket_test_name_changes_allocation(self):
        user_id = 1
        test_name = 'my_test_v2'  # difference
        buckets = ['control', 'variant1', 'variant2']
        allocation = ab.get_bucket(user_id, test=test_name, buckets=buckets)
        self.assertEqual(allocation, 'variant1')

    def test_get_bucket_example_1000_users(self):
        allocations = collections.defaultdict(int)
        test_name = 'my_test_v2'
        buckets = ['control', 'variant1', 'variant2']
        for user_id in range(1000):
            bucket = ab.get_bucket(user_id, test=test_name, buckets=buckets)
            allocations[bucket] += 1
        self.assertEqual(allocations['control'], 356)
        self.assertEqual(allocations['variant1'], 310)
        self.assertEqual(allocations['variant2'], 334)
