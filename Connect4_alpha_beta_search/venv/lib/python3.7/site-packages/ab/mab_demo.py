from ab import mab

TEST_NAME = 'MY_DEMO_TEST_V1'
TEST_CONTROL = 'control'
TEST_VARIANT1 = 'variant1'
TEST_VARIANT2 = 'variant2'
TEST_BUCKETS = (
    TEST_CONTROL,
    TEST_VARIANT1,
    TEST_VARIANT2,
)

while True:
    bucket = mab.get_bucket(TEST_NAME, TEST_BUCKETS)
    try:
        val = input(f'Did {bucket} succeed? y/n: ').strip()
    except KeyboardInterrupt:
        exit()
    if val == 'y':
        mab.success(TEST_NAME, bucket)
    print(mab.get_scores(TEST_NAME, TEST_BUCKETS))
