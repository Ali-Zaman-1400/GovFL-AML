import argparse, os, yaml, torch, time, json
import numpy as np
from model import SimpleMLP
from dp_wrapper import add_noise

def load_data(path, node_id, nodes):
    data = np.load(path)
    X = data['X']
    y = data['y']
    # simple partition by index for node simulation
    n = X.shape[0]
    idx = np.arange(n)
    parts = np.array_split(idx, nodes)
    sel = parts[node_id]
    return torch.tensor(X[sel], dtype=torch.float32), torch.tensor(y[sel], dtype=torch.float32)

def local_train(args):
    cfg = yaml.safe_load(open(args.config)) if args.config else {}
    epochs = cfg.get('epochs', 2)
    lr = cfg.get('learning_rate', 0.001)
    dp_epsilon = cfg.get('dp_epsilon', 3.0)
    device = 'cpu'

    X, y = load_data(args.data, args.node_id, args.nodes)
    model = SimpleMLP(in_dim=X.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.BCELoss()

    for epoch in range(epochs):
        model.train()
        perm = torch.randperm(X.size(0))
        for i in range(0, X.size(0), 32):
            idx = perm[i:i+32]
            xb = X[idx]
            yb = y[idx].unsqueeze(1)
            pred = model(xb)
            loss = loss_fn(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # compute simple local accuracy for reputation
    model.eval()
    with torch.no_grad():
        pred = (model(X) > 0.5).float().squeeze()
        acc = (pred == y).float().mean().item()

    # apply DP noise to parameters (simulation)
    add_noise(model, epsilon=dp_epsilon)

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, f'model_node_{args.node_id}_round_{args.round}.pt')
    torch.save({'state_dict': model.state_dict(), 'acc': acc}, fname)

    # simple metadata file
    meta = {'node_id': args.node_id, 'round': args.round, 'acc': acc, 'timestamp': time.time()}
    with open(fname + '.meta.json', 'w') as f:
        json.dump(meta, f)
    print(f'[node {args.node_id}] finished round {args.round}, acc={acc:.4f}, wrote {fname}')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--node_id', type=int, required=True)
    p.add_argument('--nodes', type=int, default=3)
    p.add_argument('--data', type=str, default='../data/processed/elliptic_sample.npz')
    p.add_argument('--out_dir', type=str, default='../out_models')
    p.add_argument('--round', type=int, default=0)
    p.add_argument('--config', type=str, default='../node_agent/config.yaml')
    args = p.parse_args()
    local_train(args)
