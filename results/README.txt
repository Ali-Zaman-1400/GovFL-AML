# Results Directory — GovFL-AML MVP

This folder contains all output metrics, logs, and model snapshots generated during
federated training and aggregation rounds.

---

##  Contents

| File | Description |
|------|--------------|
| `round_metrics.csv` | Numerical metrics for each round (AUC, accuracy, reputation weights, ε) |
| `ledger_log.json` | Copy of the events recorded in `gov_ledger/log.json` |
| `global_model_round_X.pt` | Aggregated model checkpoint after round *X* |
| `demo_summary.txt` | Compact summary printed by the demo script |
| `timing_profile.json` | (Optional) Time per node per round — used for runtime analysis |

---

##  Example Metrics

| Round | Avg Local Acc | Global AUC | ε (DP) | Reputation Weights | Comm. Overhead (KB) |
|--------|----------------|-------------|--------|--------------------|----------------------|
| 1 | 0.83 | 0.84 | 3.0 | [0.34, 0.33, 0.33] | 380 |
| 2 | 0.86 | 0.87 | 3.0 | [0.35, 0.34, 0.31] | 410 |
| 3 | 0.88 | 0.89 | 3.0 | [0.36, 0.33, 0.31] | 415 |

All metrics are logged automatically by the **aggregator** module
after each successful round and are useful for paper reporting.

---

##  How to Generate

Once the environment is ready and dependencies are installed:

```bash
./experiments/run_demo.sh --nodes 3 --rounds 3
