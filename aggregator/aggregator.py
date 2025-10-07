import time, os, torch, json
from model_merge import average_weights
from reputation import compute_reputation
from ledger_interface import record_event

IN_DIR = '../out_models'
GLOBAL_MODEL = 'global_model.pt'

def wait_for_round(nodes, round_id, timeout=60):
    metas = []
    start = time.time()
    while time.time() - start < timeout:
        metas = [f for f in os.listdir(IN_DIR) if f.endswith('.meta.json') and f'round_{round_id}' in f]
        if len(metas) >= nodes:
            return metas
        time.sleep(1)
    return metas

def aggregate_round(nodes, round_id):
    metas = wait_for_round(nodes, round_id)
    if not metas:
        print('Timeout waiting for models')
        return
    local_states = []
    scores = []
    for m in metas:
        path = os.path.join(IN_DIR, m.replace('.meta.json',''))
        d = torch.load(path)
        local_states.append(d['state_dict'])
        scores.append(d['acc'])
    weights = compute_reputation(scores)
    new_state = average_weights(local_states, weights)
    torch.save(new_state, GLOBAL_MODEL)
    record_event('Aggregated', {'round': round_id, 'weights': weights.tolist()})
    print(f'Aggregated round {round_id}, weights={weights}')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--nodes', type=int, default=3)
    p.add_argument('--rounds', type=int, default=3)
    args = p.parse_args()
    os.makedirs('../out_models', exist_ok=True)
    for r in range(args.rounds):
        record_event('RoundStarted', {'round': r})
        print(f'Waiting for round {r} models...')
        aggregate_round(args.nodes, r)
        time.sleep(1)
    print('Aggregator finished')
