import numpy as np

class GSRIScoringEngine:
    """
    Bayesian-based systemic risk monitor for the Omni-Sentinel environment.
    Calculates the Global Systemic Risk Index (G-SRI).
    """
    def __init__(self, prior_risk=0.2):
        self.prior_risk = prior_risk
        self.threshold = 40.0

    def calculate_gsri(self, telemetry_data):
        """
        Calculates GSRI using a simplified Bayesian update.
        telemetry_data: dict containing risk factors (0.0 to 1.0)
        """
        # Risk factors: alignment_drift, compute_anomaly, breakout_probability
        factors = list(telemetry_data.values())
        if not factors:
            return self.prior_risk * 100

        # Likelihood of high risk given telemetry
        likelihood = np.mean(factors)

        # Posterior risk (simplified)
        posterior = (likelihood * self.prior_risk) / (likelihood * self.prior_risk + (1 - likelihood) * (1 - self.prior_risk))

        gsri = posterior * 100
        return round(gsri, 2)

    def is_safe(self, gsri):
        return gsri < self.threshold

if __name__ == "__main__":
    engine = GSRIScoringEngine()
    test_data = {"alignment_drift": 0.1, "compute_anomaly": 0.05, "breakout_probability": 0.02}
    gsri = engine.calculate_gsri(test_data)
    print(f"G-SRI: {gsri} (Safe: {engine.is_safe(gsri)})")
