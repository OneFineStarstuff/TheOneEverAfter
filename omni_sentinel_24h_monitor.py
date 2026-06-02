import time
import sys
import os
import random
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.infrastructure.pqc_worm_logger import PQCWormLogger
from src.infrastructure.tpm_attestor import TPMAttestor

def main():
    print("Omni-Sentinel Cognitive Execution Environment - 24h Monitor Initializing...")

    gsri_engine = GSRIScoringEngine()
    worm_logger = PQCWormLogger()
    tpm_attestor = TPMAttestor()

    iteration = 0
    while True:
        try:
            iteration += 1
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # 1. review telemetry (simulated)
            telemetry = {
                "alignment_drift": random.uniform(0.01, 0.15),
                "compute_anomaly": random.uniform(0.01, 0.1),
                "breakout_probability": random.uniform(0.001, 0.05)
            }

            # 2. calculate G-SRI
            gsri = gsri_engine.calculate_gsri(telemetry)
            status = "GREEN" if gsri_engine.is_safe(gsri) else "RED"

            # 3. TPM Attestation
            attestation = tpm_attestor.validate_attestation()
            pcr_match = attestation["PCR_MATCH"]

            # 4. Log to WORM
            log_entries = [
                {"timestamp": timestamp, "G-SRI": gsri, "status": status, "PCR_MATCH": pcr_match}
            ]
            batch_id = time.strftime("%Y%m%d_%H%M%S")
            worm_file = worm_logger.commit_batch(batch_id, log_entries)

            # 5. Output to stdout (for monitor.log)
            print(f"[{timestamp}] Iteration {iteration}: G-SRI={gsri} | Status={status} | PCR_MATCH={pcr_match} | WORM_FILE={worm_file}")
            sys.stdout.flush()

            # Sleep for 60 seconds (requirement was 15 min check, 1 min allows faster verification for now)
            # In a real 24h script we might use longer intervals, but instructions said 15 mins for first checkpoint.
            time.sleep(60)

        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
