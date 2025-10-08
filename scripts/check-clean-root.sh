#!/usr/bin/env bash
set -euo pipefail
allowed_regex='^(\.git|\.gitignore|\.gitattributes|\.editorconfig|README\.md|LICENSE|QUICKSTART\.md|CLEANUP\.md|package\.json|pyproject\.toml|pom\.xml|build\.gradle|requirements\.txt|\.env\.example|src|tests|docs|scripts|assets|examples|data|\.github|\.idea)$'
bad=0
while IFS= read -r entry; do
  base="$(basename "$entry")"
  [[ "$base" =~ $allowed_regex ]] || { echo "❌ Unexpected root item: $base"; bad=1; }
done < <(find . -maxdepth 1 -mindepth 1 -printf "%f\n")
exit $bad
