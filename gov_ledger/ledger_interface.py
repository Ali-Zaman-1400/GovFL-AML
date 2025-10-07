import os, json, hashlib, time
LOG = 'gov_ledger/log.json'
def record_event(event, data):
    os.makedirs('gov_ledger', exist_ok=True)
    entry = {'timestamp': time.time(), 'event': event, 'data': data}
    entry['hash'] = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    with open(LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
