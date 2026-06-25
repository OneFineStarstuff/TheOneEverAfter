import unittest
from src.governance_engine.compliance_engine import ComplianceEngine, MASFEATCompliance, HKMAEthicsCompliance
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine


class TestComplianceSystem(unittest.TestCase):
    def setUp(self):
        self.engine = ComplianceEngine()

    def test_mas_feat_fairness(self):
        mas = MASFEATCompliance()
        # Fair scenario
        fair_rates = {"group_a": 0.5, "group_b": 0.55}
        proof = mas.generate_zk_fairness_proof(fair_rates)
        self.assertTrue(proof["fairness_verified"])
        self.assertLessEqual(proof["metrics"]["dp_diff"], 0.1)

        # Unfair scenario
        unfair_rates = {"group_a": 0.8, "group_b": 0.4}
        proof = mas.generate_zk_fairness_proof(unfair_rates)
        self.assertFalse(proof["fairness_verified"])
        self.assertGreater(proof["metrics"]["dp_diff"], 0.1)

    def test_hkma_ethics_cae(self):
        hkma = HKMAEthicsCompliance()
        attributions = {"age": 0.45, "income": -0.12, "location": 0.05}
        cae = hkma.generate_cae(attributions)

        self.assertEqual(cae["version"], "1.0")
        self.assertEqual(cae["contextual_bounds"]["max"], 0.45)
        self.assertEqual(cae["contextual_bounds"]["min"], -0.12)
        self.assertIn("attribution_score", cae)
        self.assertIn("integrity_seal", cae)

    def test_gsri_compliance_integration(self):
        gsri_engine = GSRIScoringEngine()
        telemetry = {
            "drift": 0.05,
            "selection_rates": {"a": 0.5, "b": 0.8}  # Unfair
        }
        gsri = gsri_engine.calculate_gsri(telemetry)
        compliance = gsri_engine.verify_compliance(telemetry)

        self.assertFalse(gsri_engine.is_safe(gsri, compliance))
        self.assertFalse(compliance["mas_feat"]["fairness_verified"])
        self.assertEqual(compliance["ethics_maturity_score"], 3.0)


if __name__ == "__main__":
    unittest.main()
