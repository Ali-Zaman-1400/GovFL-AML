#!/usr/bin/env bash
# Simple demo runner: launches aggregator + N node_agent processes on one machine.
# Usage: ./run_demo.sh --nodes 3 --rounds 3
NODES=3
ROUNDS=3
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --nodes) NODES="$2"; shift; shift; ;;
    --rounds) ROUNDS="$2"; shift; shift; ;;
    *) shift; ;;
  esac
done
echo "Starting demo: nodes=$NODES rounds=$ROUNDS"
# start aggregator
python3 aggregator/aggregator.py --nodes $NODES --rounds $ROUNDS &
AGG_PID=$!
sleep 1
# start node agents
for i in $(seq 0 $(($NODES-1))); do
  python3 node_agent/train_local.py --node_id $i --nodes $NODES --round $((0)) &
  sleep 0.5
done
wait $AGG_PID
echo "Demo finished"        