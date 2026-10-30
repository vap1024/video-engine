#!/bin/bash
# video-engine - Remotion render wrapper.
#
# Why the network namespace: on some hosts Remotion's port probe
# (connect checks to 0.0.0.0 / ::) is fooled by transparent proxying
# and reports "No available ports found". Inside a fresh netns the
# probes are honest. Rendering itself needs no network.
#
# Usage: render-remotion.sh still|video <CompId> <out> [propsJson]
# Env:   REMOTION_DIR - path to the remotion/ project (default:
#        ../remotion relative to this script).
set -e
MODE="$1"; COMP="$2"; OUT="$3"; PROPS="${4:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTION_DIR="${REMOTION_DIR:-$SCRIPT_DIR/../remotion}"
unshare -Urn bash -c "
  ip link set lo up
  cd '$REMOTION_DIR'
  nice -n 10 node render.mjs '$MODE' '$COMP' '$OUT' '$PROPS'
"
