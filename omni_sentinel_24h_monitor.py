import time
import sys
import random
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.infrastructure.pqc_worm_logger import PQCWormLogger
from src.infrastructure.tpm_attestor import TPMAttestor


def run_iteration(iteration, gsri_engine, worm_logger, tpm_attestor):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # 1. review telemetry (simulated)
    # Enhanced to include regulatory compliance factors for MAS FEAT and HKMA Ethics
    telemetry = {
        "alignment_drift": random.uniform(0.01, 0.15),
        "compute_anomaly": random.uniform(0.01, 0.1),
        "breakout_probability": random.uniform(0.001, 0.05),
        "selection_rates": {
            "expert_node_retail_01": random.uniform(0.75, 0.85),
            "expert_node_retail_02": random.uniform(0.75, 0.85)
        },
        "attributions": {
            "input_variance": random.uniform(-0.1, 0.1),
            "weight_entropy": random.uniform(0.0, 1.0)
        }
    }

    # 2. calculate G-SRI and Regulatory Compliance Remediation
    gsri = gsri_engine.calculate_gsri(telemetry)
    compliance = gsri_engine.verify_compliance(telemetry)

    # Integrated check: Safety now depends on both G-SRI and Regulatory Fairness (MAS FEAT)
    status = "GREEN" if gsri_engine.is_safe(gsri, compliance) else "RED"

    # 3. TPM Attestation
    attestation = tpm_attestor.validate_attestation()
    pcr_match = attestation["PCR_MATCH"]

    # 4. Log to WORM with PQC Signature
    # Including compliance audit trails (ZK-proof hashes and CAE integrity seals)
    log_entries = [
        {
            "timestamp": timestamp,
            "iteration": iteration,
            "G-SRI": gsri,
            "status": status,
            "PCR_MATCH": pcr_match,
            "regulatory_audit": {
                "mas_feat_proof": compliance["mas_feat"]["proof_hash"],
                "hkma_ethics_cae_seal": compliance["hkma_ethics_cae"].get("integrity_seal")
            }
        }
    ]
    batch_id = time.strftime("%Y%m%d_%H%M%S")
    worm_file = worm_logger.commit_batch(batch_id, log_entries)

    return {
        "timestamp": timestamp,
        "iteration": iteration,
        "G-SRI": gsri,
        "status": status,
        "PCR_MATCH": pcr_match,
        "WORM_FILE": worm_file
    }


def main():
    print("Omni-Sentinel Cognitive Execution Environment - 24h Monitor Initializing...")

    gsri_engine = GSRIScoringEngine()
    worm_logger = PQCWormLogger()
    tpm_attestor = TPMAttestor()

    iteration = 0
    while True:
        try:
            iteration += 1
            result = run_iteration(iteration, gsri_engine, worm_logger, tpm_attestor)

            # 5. Output to stdout (for monitor.log)
            print(f"[{result['timestamp']}] Iteration {iteration}: G-SRI={result['G-SRI']} | Status={result['status']} | PCR_MATCH={result['PCR_MATCH']} | WORM_FILE={result['WORM_FILE']}")
            sys.stdout.flush()

            # Sleep for 60 seconds for real-time monitoring simulation
            time.sleep(60)

        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
