# Omni-Sentinel Cognitive Execution Environment

Omni-Sentinel is a high-assurance governance and execution framework designed for cognitive agents and AI systems. It provides a multi-layered defense-in-depth architecture anchored in hardware trust, Bayesian risk monitoring, and post-quantum cryptographic audit trails.

## 🚀 Overview

The system is built to ensure that cognitive tasks are executed within safe, measurable, and immutable boundaries. It integrates advanced hardware attestation with real-time risk scoring to mitigate alignment drift and systemic risks.

## 🏗️ Architecture (The G-Stack)

1.  **Hardware Root of Trust**: TEE/TPM with PCR_MATCH enforcement. Verifies the integrity of the execution environment.
2.  **Cognitive Control Plane**: Bayesian G-SRI (Global Systemic Risk Index) scoring engine regulating model execution based on real-time telemetry.
3.  **Immutable Evidence Store**: PQC-signed (ML-DSA) WORM (Write-Once-Read-Many) audit logs stored in an immutable bucket (e.g., AWS S3 Object Lock).

## 📁 Project Structure

- `src/governance_engine/`: Contains the Bayesian scoring logic for risk assessment.
- `src/infrastructure/`: Hardware attestation and immutable logging implementations.
- `src/roadmap/`: Documentation regarding reference architecture and future master roadmap.
- `tests/`: Automated test suite for validating governance logic.
- `mock_s3_bucket/`: Simulated immutable storage for audit logs.

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- NumPy
- oqs-python (for ML-DSA signatures)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/omni-sentinel/omni-sentinel.git
   cd omni-sentinel
   ```

2. Install dependencies:
   ```bash
   pip install numpy oqs-python
   ```

### Usage

#### G-SRI Scoring
```python
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine

engine = GSRIScoringEngine()
telemetry = {"alignment_drift": 0.1, "compute_anomaly": 0.05}
gsri = engine.calculate_gsri(telemetry)
print(f"G-SRI: {gsri}")
```

#### PQC-WORM Logging
```python
from src.infrastructure.pqc_worm_logger import PQCWormLogger

logger = PQCWormLogger()
logger.commit_batch("batch_001", [{"event": "GSRI_CHECK", "value": 15.5}])
```

## 🧪 Testing

Run the test suite:

```bash
PYTHONPATH=. python3 tests/test_governance.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## 📝 Citation

If you use this software in your research, please cite it as follows:

```
@software{omni_sentinel_2026,
  author = {{Omni-Sentinel Contributors}},
  title = {Omni-Sentinel Cognitive Execution Environment},
  version = {1.0.0},
  year = {2026},
  url = {https://github.com/omni-sentinel/omni-sentinel}
}
```
