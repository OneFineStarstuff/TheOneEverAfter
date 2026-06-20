import unittest
import os
import json
import shutil
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.infrastructure.pqc_worm_logger import PQCWormLogger
from src.infrastructure.tpm_attestor import TPMAttestor


class TestGovernanceSystem(unittest.TestCase):
    def setUp(self):
        self.test_bucket = "test_worm_bucket"
        if os.path.exists(self.test_bucket):
            shutil.rmtree(self.test_bucket)

    def tearDown(self):
        if os.path.exists(self.test_bucket):
            shutil.rmtree(self.test_bucket)

    def test_gsri_calculation(self):
        engine = GSRIScoringEngine()
        # High risk telemetry
        test_data = {"drift": 0.9, "anomaly": 0.9, "breakout": 0.9}
        gsri = engine.calculate_gsri(test_data)
        self.assertGreater(gsri, 40.0)
        self.assertFalse(engine.is_safe(gsri))

        # Low risk telemetry
        test_data = {"drift": 0.01, "anomaly": 0.01, "breakout": 0.01}
        gsri = engine.calculate_gsri(test_data)
        self.assertLess(gsri, 40.0)
        self.assertTrue(engine.is_safe(gsri))

    def test_pqc_worm_logger(self):
        logger = PQCWormLogger(bucket_path=self.test_bucket)
        batch_id = "TEST_BATCH"
        entries = [{"test": "data"}]
        filename = logger.commit_batch(batch_id, entries)

        filepath = os.path.join(self.test_bucket, filename)
        self.assertTrue(os.path.exists(filepath))

        with open(filepath, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["batch_id"], batch_id)
            self.assertIn("pqc_signature", data)

    def test_tpm_attestation(self):
        attestor = TPMAttestor()
        result = attestor.validate_attestation()
        self.assertTrue(result["PCR_MATCH"])
        self.assertEqual(result["status"], "VALIDATED")


if __name__ == "__main__":
    unittest.main()
