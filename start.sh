#!/bin/bash
# Start the Panel dashboard
exec panel serve dashboard.py --address 0.0.0.0 --port ${PORT:-5000} --allow-websocket-origin=*
