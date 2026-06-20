import unittest
import os
import shutil
import json
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.infrastructure.pqc_worm_logger import PQCWormLogger
from src.infrastructure.tpm_attestor import TPMAttestor
from omni_sentinel_24h_monitor import run_iteration


class TestMonitorSystem(unittest.TestCase):
    def setUp(self):
        self.test_bucket = "test_monitor_worm_bucket"
        if os.path.exists(self.test_bucket):
            shutil.rmtree(self.test_bucket)
        self.gsri_engine = GSRIScoringEngine()
        self.worm_logger = PQCWormLogger(bucket_path=self.test_bucket)
        self.tpm_attestor = TPMAttestor()

    def tearDown(self):
        if os.path.exists(self.test_bucket):
            shutil.rmtree(self.test_bucket)

    def test_run_iteration(self):
        # Run a single iteration
        result = run_iteration(1, self.gsri_engine, self.worm_logger, self.tpm_attestor)

        # Basic field checks
        self.assertEqual(result["iteration"], 1)
        self.assertIn("G-SRI", result)
        self.assertIn("status", result)
        self.assertIn("PCR_MATCH", result)
        self.assertIn("WORM_FILE", result)

        # Verify WORM file exists and contains regulatory audit data
        filepath = os.path.join(self.test_bucket, result["WORM_FILE"])
        self.assertTrue(os.path.exists(filepath))

        with open(filepath, 'r') as f:
            data = json.load(f)
            entry = data["entries"][0]
            self.assertIn("regulatory_audit", entry)
            self.assertIn("mas_feat_proof", entry["regulatory_audit"])
            self.assertIn("hkma_ethics_cae_seal", entry["regulatory_audit"])


if __name__ == "__main__":
    unittest.main()
