import unittest

from ab import stats


class StatsTestCase(unittest.TestCase):

    def test_conversion_rate(self):
        test = (1000, 10)
        out = stats.conversion_rate(test)
        self.assertEqual(out, 0.01)

    def test_conversion_rate_2(self):
        test = (1000, 123)
        out = stats.conversion_rate(test)
        self.assertEqual(out, 0.123)

    def test_conversion_rate_uncertainty(self):
        test = (1000, 10)
        out = stats.conversion_rate_uncertainty(test)
        self.assertEqual(out, 0.003146426544510455)

    def test_conversion_rate_uncertainty_2(self):
        test = (1000, 123)
        out = stats.conversion_rate_uncertainty(test)
        self.assertEqual(out, 0.010386096475577337)

    def test_conversion_no_uplift(self):
        control = (1000, 10)
        test = (1000, 10)
        out = stats.conversion_uplift(control, test)
        self.assertEqual(out, 0)

    def test_conversion_uplift_test(self):
        control = (1000, 10)
        test = (1000, 50)
        out = stats.conversion_uplift(control, test)
        self.assertEqual(out, 4.0)

    def test_conversion_uplift_control(self):
        control = (1000, 50)
        test = (1000, 10)
        out = stats.conversion_uplift(control, test)
        self.assertEqual(out, -0.7999999999999999)

    def test_z_score_even(self):
        test = (1000, 10)
        test_rate = stats.conversion_rate(test)
        test_unc = stats.conversion_rate_uncertainty(test)
        control = (1000, 10)
        control_rate = stats.conversion_rate(control)
        control_unc = stats.conversion_rate_uncertainty(control)
        out = stats.z_score(test_rate, test_unc, control_rate, control_unc)
        self.assertEqual(out, 0.0)

    def test_z_score_variant_winning(self):
        test = (1000, 50)
        test_rate = stats.conversion_rate(test)
        test_unc = stats.conversion_rate_uncertainty(test)
        control = (1000, 10)
        control_rate = stats.conversion_rate(control)
        control_unc = stats.conversion_rate_uncertainty(control)
        out = stats.z_score(test_rate, test_unc, control_rate, control_unc)
        self.assertEqual(out, 5.279636773484547)

    def test_z_score_control_winning(self):
        test = (1000, 10)
        test_rate = stats.conversion_rate(test)
        test_unc = stats.conversion_rate_uncertainty(test)
        control = (1000, 50)
        control_rate = stats.conversion_rate(control)
        control_unc = stats.conversion_rate_uncertainty(control)
        out = stats.z_score(test_rate, test_unc, control_rate, control_unc)
        self.assertEqual(out, -5.279636773484547)

    def test_p_value_default(self):
        z_score = 0.0
        self.assertEqual(stats.p_value(z_score), 0.5)

    def test_p_value_variant_winning(self):
        test = (1000, 50)
        test_rate = stats.conversion_rate(test)
        test_unc = stats.conversion_rate_uncertainty(test)
        control = (1000, 10)
        control_rate = stats.conversion_rate(control)
        control_unc = stats.conversion_rate_uncertainty(control)
        z_score = stats.z_score(test_rate, test_unc, control_rate, control_unc)
        self.assertEqual(stats.p_value(z_score), 6.472011328743767e-08)

    def test_p_value_control_winning(self):
        test = (1000, 10)
        test_rate = stats.conversion_rate(test)
        test_unc = stats.conversion_rate_uncertainty(test)
        control = (1000, 50)
        control_rate = stats.conversion_rate(control)
        control_unc = stats.conversion_rate_uncertainty(control)
        z_score = stats.z_score(test_rate, test_unc, control_rate, control_unc)
        self.assertEqual(stats.p_value(z_score), 6.472011328743767e-08)

    def test_get_results_missing_control_key(self):
        with self.assertRaises(stats.StatsError):
            scores = {
                'variant1': (1000, 25),
                'variant2': (1000, 50),
            }
            stats.get_results(scores)

    def test_get_results(self):
        scores = {
            'control': (1000, 10),
            'variant1': (1000, 25),
            'variant2': (1000, 50),
        }
        data = stats.get_results(scores)
        self.assertEqual(len(data), 3)
        control = data['control']

        # Control
        self.assertEqual(len(control), 7)
        self.assertEqual(control.conversion_rate, 0.01)
        self.assertEqual(control.conversion_rate_uncertainty,
                         0.003146426544510455)
        self.assertEqual(control.uplift, 0.0)
        self.assertEqual(control.z_score, 0.0)
        self.assertEqual(control.p_value, 0.0)
        self.assertEqual(control.is_better_than_control, False)
        self.assertEqual(control.is_significant, False)

        # Variant1
        variant1 = data['variant1']
        self.assertEqual(len(variant1), 7)
        self.assertEqual(variant1.conversion_rate, 0.025)
        self.assertEqual(variant1.conversion_rate_uncertainty,
                         0.0049371044145328745)
        self.assertEqual(variant1.uplift, 1.5)
        self.assertEqual(variant1.z_score, 2.5621380568422687)
        self.assertEqual(variant1.p_value, 0.005201497829248816)
        self.assertEqual(variant1.is_better_than_control, True)
        self.assertEqual(variant1.is_significant, True)

        # Variant2
        variant2 = data['variant2']
        self.assertEqual(len(variant2), 7)
        self.assertEqual(variant2.conversion_rate, 0.05)
        self.assertEqual(variant2.conversion_rate_uncertainty,
                         0.006892024376045111)
        self.assertEqual(variant2.uplift, 4.0)
        self.assertEqual(variant2.z_score, 5.279636773484547)
        self.assertEqual(variant2.p_value, 6.472011328743767e-08)
        self.assertEqual(variant2.is_better_than_control, True)
        self.assertEqual(variant2.is_significant, True)
