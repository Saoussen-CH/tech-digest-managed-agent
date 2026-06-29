#!/usr/bin/env bash
# Regenerate the codelab HTML from index.lab.md using claat.
# Output goes to docs/ for GitHub Pages hosting.
#
# Prerequisites: go install github.com/googlecodelabs/tools/claat@latest
#
# Preview locally with: claat serve (from this directory)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CODELAB_ID="managed-agents-gemini-api"
DOCS_DIR="$SCRIPT_DIR/../docs"

rm -rf "$CODELAB_ID"
/home/saoussen/go/bin/claat export index.lab.md

echo "Copying to docs/..."
rm -rf "$DOCS_DIR"
mkdir -p "$DOCS_DIR"
cp -r "$CODELAB_ID"/. "$DOCS_DIR"/
touch "$DOCS_DIR/.nojekyll"

echo "Done. Codelab at docs/index.html"
