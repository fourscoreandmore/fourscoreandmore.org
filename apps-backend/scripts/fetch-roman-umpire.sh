#!/bin/sh
# Download app/romanUmpire.py from the When-in-Rome submodule's pinned commit,
# without checking out the (large) submodule. The Upsun build hook copies it
# from the submodule instead. Tests that need it are skipped without it.
set -eu
cd "$(dirname "$0")/.."
sha=$(git ls-tree HEAD When-in-Rome | awk '{print $3}')
curl -sSfL -o app/romanUmpire.py \
  "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/$sha/Code/romanUmpire.py"
echo "Fetched romanUmpire.py from When-in-Rome@$sha"
