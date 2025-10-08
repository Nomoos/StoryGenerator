# 🧹 Repository Cleanup & Reorg — Step-by-Step Checklist

> Save as `CLEANUP.md`. Follow in order. All steps use GitHub-style checkboxes and copy‑pasteable commands.  
> ⚠️ Destructive steps include **dry‑runs first**; only run the "apply" command when you're sure.

---

## 0) Prep & Safety

- [ ] **Confirm clean worktree (commit or stash everything).**
  ```bash
  git status
  ```

- [ ] **Create a dedicated reorg branch (date‑stamped) & backup tag.**
  ```bash
  BRANCH="chore/reorg-$(date +%F)"
  TAG="backup/pre-reorg-$(date +%F)"
  git checkout -b "$BRANCH"
  git tag "$TAG"
  git push -u origin "$BRANCH"
  git push --tags
  ```

---

## 1) Inventory & Size

- [ ] **List largest tracked blobs (find accidental binaries).**
  ```bash
  git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize:disk) %(rest)' \
  | awk '$1=="blob"{print $3, $4}' \
  | numfmt --to=iec --suffix=B --padding=7 | sort -h | tail -n 30
  ```

- [ ] **Dry‑run: what would `git clean` remove (untracked/ignored)?**
  ```bash
  git clean -n -d -x
  # If OK, apply:
  # git clean -f -d -x
  ```

---

## 2) .gitignore & De‑track Generated Files

- [ ] **Ensure a sane `.gitignore` (append baseline entries).**
  ```bash
  printf "%s\n" \
  "# OS" ".DS_Store" "Thumbs.db" \
  "" "# Editors" ".idea/" ".vscode/" \
  "" "# Dependencies" "node_modules/" "venv/" ".venv/" \
  "" "# Builds" "dist/" "build/" "out/" "coverage/" \
  "" "# Logs" "*.log" "npm-debug.log*" "yarn-debug.log*" \
  >> .gitignore
  git add .gitignore && git commit -m "chore: update .gitignore"
  ```

- [ ] **Untrack committed generated/dep folders (keep locally).**
  ```bash
  git rm -r --cached node_modules dist build out coverage 2>/dev/null || true
  git commit -m "chore: stop tracking generated/dep folders" || true
  ```

---

## 3) Standard Directory Layout (keep top level clean)

**Allowed top‑level items (adjust to your stack):**  
`src/`, `tests/`, `docs/`, `scripts/`, `assets/`, `.github/`, `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md`, `LICENSE`, one project manifest (`package.json` or `pyproject.toml` or `pom.xml`/`build.gradle`).

- [ ] **Create folders.**
  ```bash
  mkdir -p src tests scripts docs assets .github/workflows
  ```

- [ ] **Move implementation code into `src/` (examples; edit!).**
  ```bash
  [ -d "app" ] && git mv app src || true
  [ -d "lib" ] && git mv lib src || true
  for f in *.py; do [ -f "$f" ] && git mv "$f" src/; done
  for f in *.js *.ts *.jsx *.tsx; do [ -f "$f" ] && git mv "$f" src/; done
  ```

- [ ] **Move tests to `tests/`.**
  ```bash
  find . -type d -name "test*" -maxdepth 2 -not -path "./tests" -exec bash -lc 'for d; do git mv "$d" tests/$(basename "$d") || true; done' bash {} +
  ```

- [ ] **Move docs & assets.**
  ```bash
  [ -d "documentation" ] && git mv documentation docs || true
  for d in public static images img media; do
    [ -d "$d" ] && git mv "$d" assets/$(basename "$d") || true
  done
  ```

- [ ] **Move scripts/CLIs to `scripts/`.**
  ```bash
  [ -d "bin" ] && git mv bin scripts || true
  ```

- [ ] **Commit structure moves.**
  ```bash
  git commit -m "refactor: enforce clean top-level structure (src/tests/docs/scripts/assets)"
  ```

---

## 4) Deduplication (keep one canonical)

- [ ] **Find exact duplicates by content (portable).**
  ```bash
  find . -type f -not -path "./.git/*" -print0 \
  | xargs -0 -I{} sh -c 'sha256sum "{}"' \
  | sort | awk '{h=$1;$1="";sub(/^ +/,"");files[h]=files[h] "\n" $0} END{for(k in files){n=split(files[k],a,"\n"); if(n>2){print "# Duplicates (" n-1 "):"; for(i=2;i<=n;i++) print a[i]}}}'
  ```

- [ ] **Resolve duplicates: keep a canonical path, remove others (or symlink/copy).**
  ```bash
  # Example (edit paths):
  CANON="src/utils/helpers.ts"; git add "$CANON"
  git rm path/to/duplicate/helpers.ts
  git commit -m "refactor: deduplicate helpers.ts (use $CANON)"
  ```

---

## 5) Language‑Specific Touch‑Ups (optional)

- [ ] **Node/TypeScript.**
  ```bash
  # Ensure main/types/scripts paths in package.json and tsconfig rootDir/outDir
  jq '.main="dist/index.js" | .types="dist/index.d.ts"' package.json > package.tmp && mv package.tmp package.json || true
  jq '.compilerOptions |= (.outDir="dist" | .rootDir="src")' tsconfig.json > tsconfig.tmp && mv tsconfig.tmp tsconfig.json || true
  git add package.json tsconfig.json 2>/dev/null || true
  git commit -m "chore(node): align paths for src layout" || true
  ```

- [ ] **Python.**
  ```bash
  touch src/__init__.py
  printf "[tool.pytest.ini_options]\npythonpath = [\"src\"]\n" > pytest.ini
  git add src/__init__.py pytest.ini
  git commit -m "chore(python): src-layout + pytest path"
  ```

- [ ] **Java.**
  ```bash
  mkdir -p src/main/java src/test/java
  # Move packages accordingly, then:
  git commit -m "refactor(java): maven/gradle standard layout" || true
  ```

---

## 6) **SOLID Principles Check** (design hygiene)

- [ ] **S (Single Responsibility):** Each class/module has one reason to change.  
  Actions:
  - Split "god" files into cohesive modules.
  - Extract side‑effects (I/O, logging) from pure logic.

- [ ] **O (Open/Closed):** Extend behavior via new types, not edits.  
  Actions:
  - Replace `switch`/`if` dispatch with polymorphism or strategy maps.
  - Prefer composition over deep inheritance.

- [ ] **L (Liskov Substitution):** Subtypes don't violate base expectations.  
  Actions:
  - Avoid weakening preconditions / strengthening postconditions.
  - Remove "not implemented" branches in subclasses.

- [ ] **I (Interface Segregation):** Smaller, purpose‑built interfaces.  
  Actions:
  - Split fat interfaces; keep consumer‑centric contracts.
  - Use optional capabilities via adapters.

- [ ] **D (Dependency Inversion):** Depend on abstractions, inject concretes.  
  Actions:
  - Introduce ports/adapters; pass dependencies via constructor/factory.
  - Hide third‑party SDKs behind your interfaces.

---

## 7) **Code Hygiene Check** (practical checklist)

- [ ] **Naming & structure:** Clear, consistent naming; modules < ~500 LOC; functions < ~50 LOC (guideline).
- [ ] **Dead code:** Remove unused files, exports, params.  
  ```bash
  # JS/TS (requires depcheck): npx depcheck || true
  # Python (optional): pip install vulture && vulture src || true
  ```
- [ ] **Secrets & keys:** Ensure no secrets in repo.  
  ```bash
  git secrets --scan 2>/dev/null || true
  trufflehog filesystem --no-update --fail || true
  ```
- [ ] **Dependencies:** Audit vulnerabilities / prune.  
  ```bash
  npm audit --audit-level=high 2>/dev/null || true
  pip install pip-audit >/dev/null 2>&1 || true; pip-audit || true
  # Python alt: pip install safety && safety check || true
  ```
- [ ] **Lint & format (one‑off run).**
  ```bash
  npx prettier -w . 2>/dev/null || true
  npx eslint . --fix 2>/dev/null || true
  black src tests 2>/dev/null || true
  flake8 src tests 2>/dev/null || true
  ```
- [ ] **Tests:** Ensure unit tests run from `tests/`; add smoke tests if missing.
- [ ] **Logging & errors:** Use structured logging; avoid swallowing exceptions.
- [ ] **Boundaries:** Validate inputs at public boundaries (API/controllers/CLIs).
- [ ] **Performance & complexity:** Hot paths measured; cyclomatic complexity reasonable.
- [ ] **Docs:** README updated to reflect new structure and commands.

---

## 8) **Remove Existing CI & Add Single Auto‑Merge (pre‑review)**

> Removes all existing workflows, and installs a **single** workflow that will auto‑merge PRs **without review** when the PR has the `automerge` label, is mergeable, and all checks (if any) are green. Ensure your repo/branch protections allow this behavior.

- [ ] **Remove all existing workflows.**
  ```bash
  git rm -r .github/workflows 2>/dev/null || true
  mkdir -p .github/workflows
  git commit -m "ci: remove old workflows"
  ```

- [ ] **Add auto‑merge workflow (label‑gated).**
  ```bash
  cat > .github/workflows/auto-merge.yml <<'YML'
  name: Auto Merge (Pre-Review)
  on:
    pull_request:
      types: [labeled, synchronize, reopened, ready_for_review]
  permissions:
    contents: write
    pull-requests: write
  jobs:
    auto-merge:
      if: contains(github.event.pull_request.labels.*.name, 'automerge')
      runs-on: ubuntu-latest
      steps:
        - uses: actions/github-script@v7
          with:
            script: |
              const pr = context.payload.pull_request;
              const {owner, repo} = context.repo;
              const prNumber = pr.number;

              // Get fresh PR data (mergeability may be stale on event payload)
              const {data} = await github.pulls.get({owner, repo, pull_number: prNumber});
              if (data.draft) {
                core.setFailed('PR is draft');
                return;
              }

              // Optional: require successful checks on the head SHA (if any checks exist)
              try {
                const cref = data.head.sha;
                const checks = await github.checks.listForRef({owner, repo, ref: cref});
                const runs = checks.data.check_runs;
                const hasBlocking = runs.some(r => (r.status === 'completed' && r.conclusion && !['success','skipped','neutral'].includes(r.conclusion)));
                if (hasBlocking) {
                  core.setFailed('Blocking checks not passed');
                  return;
                }
              } catch (e) {
                // No checks app installed; proceed.
                core.info('No check runs found; proceeding.');
              }

              if (data.mergeable_state !== 'clean' && data.mergeable_state !== 'has_hooks') {
                core.setFailed('Not mergeable yet: ' + data.mergeable_state);
                return;
              }

              await github.pulls.merge({
                owner, repo, pull_number: prNumber, merge_method: 'squash'
              });
              core.info('PR merged.');
  YML

  git add .github/workflows/auto-merge.yml
  git commit -m "ci: add single auto-merge workflow (label: automerge)"
  ```

- [ ] **Usage:** Add the `automerge` label to a PR to auto‑merge it once mergeable.

---

## 9) Finalize

- [ ] **Run test/build (best effort).**
  ```bash
  npm test 2>/dev/null || true
  pytest -q 2>/dev/null || true
  ```

- [ ] **Push branch & open PR for the reorg.**
  ```bash
  git push -u origin "$BRANCH"
  ```

- [ ] **After merge: prune local/remote and clean up.**
  ```bash
  git checkout main
  git pull --ff-only
  git branch -d "$BRANCH"
  git remote prune origin
  ```

---

## Appendix: Root Cleanliness Guard (manual run, optional)

> Run locally to ensure top‑level is clean; **not** wired into CI by default (since CI is restricted to auto‑merge).

```bash
mkdir -p scripts
cat > scripts/check-clean-root.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
allowed_regex='^(\.git|\.gitignore|\.gitattributes|\.editorconfig|README\.md|LICENSE|QUICKSTART\.md|CLEANUP\.md|package\.json|pyproject\.toml|pom\.xml|build\.gradle|requirements\.txt|\.env\.example|src|tests|docs|scripts|assets|examples|data|\.github|\.idea)$'
bad=0
while IFS= read -r entry; do
  base="$(basename "$entry")"
  [[ "$base" =~ $allowed_regex ]] || { echo "❌ Unexpected root item: $base"; bad=1; }
done < <(find . -maxdepth 1 -mindepth 1 -printf "%f\n")
exit $bad
SH
chmod +x scripts/check-clean-root.sh
```

**Test the guard:**
```bash
bash scripts/check-clean-root.sh
```

**Optional: Wire into CI (if not using auto-merge only):**
```bash
cat > .github/workflows/root-guard.yml <<'YML'
name: Root Guard
on: [push, pull_request]
jobs:
  guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/check-clean-root.sh
YML
git add .github/workflows/root-guard.yml
git commit -m "ci: enforce clean top-level via root guard"
```

---

## Notes

- **Backup first:** The backup tag created in step 0 allows quick rollback if needed.
- **Incremental commits:** Commit after each major step to track progress.
- **Team coordination:** Communicate with team members before major restructuring.
- **CI/CD updates:** After restructuring, update any CI/CD scripts that reference old paths.
- **Documentation:** Keep documentation in sync with the new structure.

---

## See Also

- `docs/REORGANIZE.md` - Detailed reorganization guide with duplicate detection
- `docs/REORGANIZATION_SUMMARY.md` - Summary of completed reorganization work
- `docs/TEST_FILES.md` - Git tracking policy for test and content files
- `scripts/check-clean-root.sh` - Root cleanliness validation script
