GovFL-AML MVP - Execution Guide (Ubuntu, Python 3.10, CPU)
=========================================================

This package contains a minimal, runnable MVP of the GovFL-AML framework.
It is designed to run on a single Ubuntu machine with Python 3.10 and CPU-only.
Communication between node agents and the aggregator is implemented via the filesystem 
(model files are written to `out_models/` and polled by the aggregator) to make the demo 
simple and portable across VMs.

Structure
---------
- node_agent/: local trainer and DP wrapper
- aggregator/: model aggregator and reputation-based weighting
- gov_ledger/: simple ledger interface (JSON log)
- data/processed/: synthetic Elliptic-like sample data for quick testing
- experiments/run_demo.sh: script that launches aggregator + N nodes (default N=3)

Quick start (recommended)
-------------------------
1. Create a Python virtualenv (Python 3.10) and install requirements:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Make the run script executable:
   chmod +x experiments/run_demo.sh

3. Run demo (aggregator + 3 node agents, configurable):
   ./experiments/run_demo.sh --nodes 3 --rounds 3

What the demo does
-------------------
- Each node trains a tiny local model on its portion of the synthetic dataset for `epochs` rounds.
- Each node writes its local model state to out_models/
- Aggregator waits for models from all nodes, computes reputation weights based on local accuracy
  reported by each node, performs a weighted average of model parameters, writes the global model back.
- Gov ledger records events (RoundStarted, UpdateSubmitted, Aggregated) in gov_ledger/log.json
- After `--rounds` rounds demo exits and results (metrics) are saved to results/

How to replace synthetic data with real Elliptic subset
------------------------------------------------------
1. Download Elliptic dataset from its official source (Kaggle) and place raw files under data/raw/elliptic/
2. Replace the synthetic file data/processed/elliptic_sample.npz or run provided preprocessing notebooks (not included in this MVP zip).
3. Rerun the demo script.

Notes
-----
- This MVP is intentionally light-weight for quick reproducibility on a single machine.
- For production/prototype, replace filesystem IPC with a secure channel (gRPC / Flower), and replace ledger 
  logging with an on-chain solution or secure off-chain proof-store.
