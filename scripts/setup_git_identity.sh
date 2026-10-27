#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
git -C "$repo_root" config --local user.name QianKuang8
git -C "$repo_root" config --local user.email 71264725+QianKuang8@users.noreply.github.com
git -C "$repo_root" config --local user.useConfigOnly true

git -C "$repo_root" var GIT_AUTHOR_IDENT
git -C "$repo_root" var GIT_COMMITTER_IDENT
