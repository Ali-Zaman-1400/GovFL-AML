# GovFL-AML
**Federated Cross-Institution AI Governance Network**
_A Blockchain-based Federated Learning Framework for Algorithmic AML Enforcement and AI Compliance_

## Overview
GovFL-AML provides a federated, privacy-preserving AI framework that allows financial institutions and crypto-exchanges to collaboratively detect AML anomalies without sharing raw data.  
It integrates:
- Federated Learning (FL) for distributed model training  
- Blockchain Governance Ledger for auditability & compliance evidence  
- Algorithmic Enforcement Layer for automatic AML policy execution  

## Core Components
| Module | Description |
|---------|-------------|
| node_agent/ | Local training, Differential Privacy, Feature Engineering |
| aggregator/ | Secure model aggregation and reputation weighting |
| gov_ledger/ | Smart contracts for policy, audit logs, and compliance proofs |
| data/ | Preprocessing scripts for Elliptic & XBlock datasets |
| experiments/ | Jupyter notebooks for benchmarks & ablation studies |
| docs/ | Paper drafts, architecture diagrams, references |

## Installation
```bash
git clone https://github.com/<your-username>/GovFL-AML.git
cd GovFL-AML
pip install -r requirements.txt
```

## Datasets
- Elliptic Dataset – Bitcoin transaction graph with AML labels  
- XBlock-ETH – Ethereum transactions with OFAC-tagged addresses  

## Evaluation Metrics
- PR-AUC  
- Recall @ 1% FPR  
- Compliance Accuracy  
- Communication Overhead  
- ε-budget usage  

## License
MIT License

## Citation
If you use this framework, please cite:
> Zamanpour, A. et al. "GovFL-AML: Federated Cross-Institution AI Governance Network for Algorithmic AML Enforcement." (Under submission, 2025)
