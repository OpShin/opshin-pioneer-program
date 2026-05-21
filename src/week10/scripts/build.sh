#!/usr/bin/env bash
#
# Build the week 10 PlutusTx vesting validator and copy the resulting
# `.plutus` envelope into `src/week10/assets/`.
#
# Designed to run inside the project's dev container (which has GHC,
# cabal and the plutus-pioneer-program checkout available). Outside the
# container you need: GHC 8.10.7, cabal 3.6.x, and the
# `plutus-pioneer-program/` directory present at the repo root.
#
# Usage:
#     src/week10/scripts/build.sh

set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
plutus_root=$repo_root/plutus-pioneer-program/code
week03=$plutus_root/Week03
week10_assets=$repo_root/src/week10/assets

if ! command -v cabal >/dev/null 2>&1; then
    echo "error: cabal not found on PATH." >&2
    echo "Run this script inside the dev container (.devcontainer/) where" >&2
    echo "GHC and cabal are pre-installed." >&2
    exit 1
fi

if [ ! -d "$week03" ]; then
    echo "error: expected $week03 to exist." >&2
    echo "The plutus-pioneer-program submodule/clone is required for this lecture." >&2
    exit 1
fi

mkdir -p "$week10_assets"
mkdir -p "$week03/assets"

echo ">> compiling Vesting via cabal repl (this can take a minute on a cold cache)"
# Drive `cabal repl` non-interactively: load the `week03` library, run
# `Vesting.saveVal`, then quit. saveVal writes ./assets/vesting.plutus
# relative to CWD.
(
    cd "$week03"
    printf 'Vesting.saveVal\n:quit\n' | cabal repl week03
)

cp "$week03/assets/vesting.plutus" "$week10_assets/vesting.plutus"
echo ">> wrote $week10_assets/vesting.plutus"
