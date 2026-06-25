import hashlib
import json
import numpy as np
from src.governance_engine.compliance_engine import ComplianceEngine


class GSRIScoringEngine:
    """
    Bayesian-based systemic risk monitor for the Omni-Sentinel environment.
    Calculates the Global Systemic Risk Index (G-SRI).
    Integrates regulatory compliance remediation for MAS FEAT and HKMA Ethics.
    """
    def __init__(self, prior_risk=0.2):
        self.prior_risk = prior_risk
        self.threshold = 40.0
        self.compliance_engine = ComplianceEngine()

    def calculate_gsri(self, telemetry_data):
        """
        Calculates GSRI using a simplified Bayesian update.
        telemetry_data: dict containing risk factors (0.0 to 1.0)
        """
        # Extract direct risk factors for Bayesian update
        direct_factors = {k: v for k, v in telemetry_data.items() if isinstance(v, (int, float))}
        factors = list(direct_factors.values())

        if not factors:
            return float(self.prior_risk * 100)

        # Likelihood of high risk given telemetry
        likelihood = np.mean(factors)

        # Posterior risk (simplified)
        posterior = (likelihood * self.prior_risk) / (likelihood * self.prior_risk + (1 - likelihood) * (1 - self.prior_risk))

        gsri = float(posterior * 100)
        return round(gsri, 2)

    def generate_gsri_proof(self, gsri, telemetry_data):
        """
        Generates a simulated ZK-proof for the GSRI calculation.
        """
        is_safe = bool(gsri < self.threshold)
        proof_data = {
            "gsri": float(gsri),
            "threshold": float(self.threshold),
            "is_safe": is_safe,
            "timestamp": str(np.datetime64('now')),
            "telemetry_summary": hashlib.sha3_512(str(telemetry_data).encode()).hexdigest()[:16]
        }

        # High-assurance proof using SHA3-512
        proof_hash = hashlib.sha3_512(json.dumps(proof_data, sort_keys=True).encode()).hexdigest()

        return {
            "gsri_proof_hash": proof_hash,
            "verification_status": "VERIFIED"
        }

    def verify_compliance(self, telemetry_data):
        """
        Verifies regulatory compliance against MAS FEAT and HKMA Ethics.
        """
        return self.compliance_engine.run_remediation_audit(telemetry_data)

    def is_safe(self, gsri, compliance_results=None):
        """
        Determines if the environment is safe based on GSRI and optional compliance status.
        """
        if compliance_results:
            # If MAS FEAT fairness is not verified, it's an automatic UNSAFE state
            if not compliance_results.get("mas_feat", {}).get("fairness_verified", True):
                return False

        return bool(gsri < self.threshold)


if __name__ == "__main__":
    engine = GSRIScoringEngine()
    test_data = {
        "alignment_drift": 0.1,
        "compute_anomaly": 0.05,
        "breakout_probability": 0.02,
        "selection_rates": {"group_a": 0.8, "group_b": 0.75},
        "attributions": {"feature_1": 0.5, "feature_2": -0.2}
    }
    gsri = engine.calculate_gsri(test_data)
    compliance = engine.verify_compliance(test_data)
    proof = engine.generate_gsri_proof(gsri, test_data)
    print(f"G-SRI: {gsri}")
    print(f"GSRI Proof: {proof}")
    print(f"Compliance Results: {compliance}")
    print(f"Safe: {engine.is_safe(gsri, compliance)}")
