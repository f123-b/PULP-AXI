#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/.deps/axi"
REV="4da15979747f326bde2f9869c64e587ce599772c"
mkdir -p "${ROOT}/.deps"
if [[ ! -d "${DEST}/.git" ]]; then
  git clone https://github.com/pulp-platform/axi.git "${DEST}"
fi
git -C "${DEST}" fetch --depth 1 origin "${REV}"
git -C "${DEST}" checkout --detach "${REV}"
echo "PULP AXI pinned at $(git -C "${DEST}" rev-parse HEAD)"
