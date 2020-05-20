from typing import Dict, Tuple, NamedTuple
import math
import scipy.stats

HIGH_CONFIDENCE = 0.05
CONTROL_KEY = 'control'


# PUBLIC


class Data(NamedTuple):
    conversion_rate: float
    conversion_rate_uncertainty: float
    uplift: float
    z_score: float
    p_value: float
    is_better_than_control: bool
    is_significant: bool
    # TODO(DAN): is_winner: bool


def get_results(
        scores: Dict[str, Tuple[int, int]],
        control_key: str = CONTROL_KEY,
        p: float = HIGH_CONFIDENCE):
    assert_control_key(scores)
    control = scores[CONTROL_KEY]
    cr_c = conversion_rate(control)
    cru_c = conversion_rate_uncertainty(control)

    data = {}
    data[CONTROL_KEY] = Data(
        conversion_rate=cr_c,  # TODO(DAN): ± format
        conversion_rate_uncertainty=cru_c,
        uplift=0.0,
        z_score=0.0,
        p_value=0.0,
        is_better_than_control=False,
        is_significant=False)

    for bucket, test in scores.items():
        if bucket == CONTROL_KEY:
            continue
        cr_t = conversion_rate(test)
        cru_t = conversion_rate_uncertainty(test)
        uplift = conversion_uplift(control, test)
        z_t = z_score(cr_t, cru_t, cr_c, cru_c)
        p_t = p_value(z_t)
        is_better_than_control = uplift > 0
        is_significant = p_t < p
        data[bucket] = Data(
            conversion_rate=cr_t,  # TODO(DAN): ± format
            conversion_rate_uncertainty=cru_t,
            uplift=uplift,
            z_score=z_t,
            p_value=p_t,
            is_better_than_control=is_better_than_control,
            is_significant=is_significant)

    return data

# PRIVATE


class StatsError(Exception):
    pass


def conversion_rate(test: Tuple[float]) -> float:
    """Successes versus Trials."""
    return test[1] / test[0]


def conversion_rate_uncertainty(test: Tuple[float]) -> float:
    """Standard error rate."""
    rate = conversion_rate(test)
    return math.sqrt((rate * (1 - rate)) / test[0])


def conversion_uplift(control: Tuple[float],
                      test: Tuple[float]) -> float:
    """Determine if test is better than control."""
    control_rate = conversion_rate(control)
    test_rate = conversion_rate(test)
    return (test_rate - control_rate) / control_rate


def z_score(test_conversion_rate: float,
            test_uncertainty_rate: float,
            control_conversion_rate: float,
            control_uncertainty_rate: float) -> float:
    """Standard deviations away from mean value."""
    numerator = test_conversion_rate - control_conversion_rate
    denominator = math.sqrt(
        test_uncertainty_rate ** 2 + control_uncertainty_rate ** 2)
    return numerator / denominator


def p_value(z_score: float) -> float:
    """Statistical significance. Lower = better."""
    return scipy.stats.norm.sf(abs(z_score))


def assert_control_key(scores: Dict[str, Tuple[int, int]]):
    if CONTROL_KEY not in scores:
        raise StatsError(f'{CONTROL_KEY} is required to test results')
