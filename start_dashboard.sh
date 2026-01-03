#!/bin/bash
# Start the Mason's Famous Lobsters Dashboard

echo "Starting Mason's Famous Lobsters P&L Dashboard..."
echo "=================================================="

# Initialize database
echo "Initializing database..."
python database.py

# Start dashboard
echo "Starting dashboard on port ${PORT:-5000}..."
panel serve dashboard.py \
  --address 0.0.0.0 \
  --port ${PORT:-5000} \
  --allow-websocket-origin=* \
  --num-procs=1

echo "Dashboard is running!"
