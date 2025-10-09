# 📦 Repository Cleanup Guide

Tento dokument popisuje postup, jak **najít a odstranit starý nebo nepoužívaný materiál**, který nemá vazby na hlavní účel aplikace. Postup je navržen tak, aby byl bezpečný, auditovatelný a snadno opakovatelný.

---

## 🎯 Cíle
- Udržovat repozitář čistý a čitelný.  
- Zbavit se mrtvého kódu, assetů a skriptů bez využití.  
- Snížit velikost repozitáře a buildů.  
- Udržet konzistenci mezi CI/CD a lokálním prostředím.  

---

## 🔑 Kroky úklidu

### 1. Identifikace core scope
- Urči hlavní entrypointy (produkční build/run).  
- Zahrň složky nezbytné pro chod aplikace:  
  - `src/` (produkční kód)  
  - `config/`, `.env.example`  
  - `migrations/`  
  - CI/CD (`.github/`, `Dockerfile`, `helm/`, `infra/`)  
  - Licenční a právní soubory (`LICENSE`, `NOTICE`, `CHANGELOG`).  

---

### 2. Detekce osiřelých souborů
Použij statickou analýzu a nástroje podle stacku:

- **JavaScript/TypeScript**: `ts-prune`, `depcruise`, `madge`.  
- **Python**: `vulture`, `unimport`.  
- **Go**: `go vet`, `staticcheck`, analýza nepoužitých pkg.  

Doplň manuální hledání pomocí:

```bash
git ls-files | grep -E '\.(js|ts|tsx|css|scss|png|jpg|svg|json)$' \
  | xargs -n1 basename | sort | uniq -c | sort -n
```

---

### 3. DRY-RUN test
Nejdřív jen simulace – žádné mazání:

```bash
# dependencies: ripgrep (rg)
PROTECT='(migrations|infra|deploy|.github|docs/legal|LICENSE|NOTICE|CHANGELOG)'

mapfile -t CANDIDATES < <(git ls-files \
  | grep -E '\.(js|jsx|ts|tsx|css|scss|png|jpg|svg|json)$' \
  | grep -Ev "$PROTECT")

echo "=== DRY RUN: nerefencované soubory ==="
> /tmp/orphans.txt
for f in "${CANDIDATES[@]}"; do
  if ! rg -n --hidden --glob '!.git' --fixed-strings "$(basename "$f")" \
    --no-ignore --ignore-file .gitignore -g '!'"$f" >/dev/null; then
    echo "$f" | tee -a /tmp/orphans.txt
  fi
done

mkdir -p .trash
while read -r f; do
  test -n "$f" && mkdir -p ".trash/$(dirname "$f")" \
    && git mv -k "$f" ".trash/$f" 2>/dev/null || true
done </tmp/orphans.txt

# ověř build & test
npm run build && npm test
```

Pokud build/test projdou, je kandidát bezpečně odstranitelný.

---

### 4. Reálné odstranění a PR
Po ověření smaž `.trash` obsah a vytvoř PR:

```bash
BRANCH=chore/cleanup-orphans
git checkout -b "$BRANCH"
git rm -r .trash/*
git commit -m "chore(cleanup): remove orphaned and unused files not linked to core app"
git push -u origin "$BRANCH"
gh pr create --fill --title "chore: cleanup orphans" --body "Automated removal of unused/orphaned files. See CLEANUP.md checklist."
```

---

## ⚠️ Safety Net
Nikdy nemaž:
- **Migrations / schema** – i když se nevolají, mohou být klíčové.  
- **Infra** (`infra/`, `deploy/`, `.github/`, Dockerfile, helm charts).  
- **Legal** (`LICENSE`, `NOTICE`, `docs/legal`).  
- **Generované soubory** (ověř `.gitattributes`, kódové generátory).  
- **Historické dokumenty** (požadavky auditu).  

---

## ✅ Checklist pro Code Review
Před mergem PR:
- [ ] Prošel build a test suite.  
- [ ] Ověřeny manuálně klíčové flow aplikace.  
- [ ] Žádné smazání migration/infra/licenčních souborů.  
- [ ] Všechny změny přehledně popsány v PR.

---

## 🛠️ Nástroje pro detekci nepoužívaných souborů

### Python Stack
```bash
# Instalace nástrojů
pip install vulture unimport

# Detekce mrtvého Python kódu
vulture src/ --min-confidence 80

# Detekce nepoužívaných importů
unimport --check src/
```

### JavaScript/TypeScript Stack
```bash
# Instalace nástrojů
npm install -g ts-prune depcheck madge

# Detekce nepoužívaných exportů (TypeScript)
ts-prune

# Detekce nepoužívaných dependencies
depcheck

# Analýza závislostí
madge --circular src/
```

### C# Stack
```bash
# Použij Resharper nebo Rider pro detekci
# - Unused using directives
# - Unused private members
# - Unreachable code

# CLI alternativa (pokud máš dotnet-format)
dotnet format analyzers --verify-no-changes
```

---

## 📊 Reporting a Metriky

Po úklidu zaznamenej:
- Počet odstraněných souborů
- Uvolněné místo (MB/GB)
- Počet odstraněných řádků kódu
- Čas build před/po

```bash
# Příklad reportu
echo "### Cleanup Results" > cleanup-report.md
echo "- Files removed: $(cat /tmp/orphans.txt | wc -l)" >> cleanup-report.md
echo "- Space freed: $(du -sh .trash/)" >> cleanup-report.md
echo "- Date: $(date)" >> cleanup-report.md
```

---

## 🔄 Periodicita

Doporučený harmonogram:
- **Měsíčně**: Rychlá kontrola mrtvého kódu pomocí automatických nástrojů
- **Kvartálně**: Důkladná revize s manuální kontrolou
- **Při velkých refaktorech**: Vždy po dokončení

---

## 📝 Související dokumenty

- `CLEANUP.md` - Obecný cleanup a reorganizační checklist
- `docs/REORGANIZATION_GUIDE.md` - Guide pro reorganizaci struktury
- `docs/REPOSITORY_STRUCTURE.md` - Doporučená struktura repozitáře

---

## 💡 Tipy a Best Practices

1. **Vždy začni s dry-run** - Nikdy nemaž soubory rovnou
2. **Používej `.trash` složku** - Umožňuje snadné vrácení
3. **Commituj po malých krocích** - Snadnější rollback
4. **Dokumentuj důvody** - Proč byl soubor odstraněn
5. **Review s týmem** - Důležité pro větší změny
6. **Testuj před i po** - Build a testy musí projít
7. **Backup větve** - Před začátkem cleanup procesu

---

## 🚨 Troubleshooting

### Build selže po cleanup
```bash
# Obnov soubory z .trash
git restore --source=HEAD~1 path/to/file

# Nebo vrať celý commit
git revert HEAD
```

### Ztracený důležitý soubor
```bash
# Najdi v historii
git log --all --full-history -- path/to/file

# Obnov z konkrétního commitu
git checkout <commit-hash> -- path/to/file
```

### Falešné positive při detekci
```bash
# Přidej do whitelist souboru
echo "path/to/file" >> .cleanup-whitelist

# Nebo přidej komentář do kódu
# KEEP: Tento soubor je potřeba pro [důvod]
```

---

## 🎓 Příklady použití

### Příklad 1: Detekce nepoužívaných Python modulů
```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
vulture src/Python/ --min-confidence 80 > /tmp/dead-code.txt
cat /tmp/dead-code.txt
```

### Příklad 2: Najdi soubory, které nikde nejsou importovány
```bash
#!/bin/bash
for file in $(find src/Python -name "*.py"); do
  filename=$(basename "$file" .py)
  if ! rg -q "import.*$filename|from.*$filename" --glob "*.py" .; then
    echo "Orphaned: $file"
  fi
done
```

### Příklad 3: Najdi obrázky, které nejsou odkazovány
```bash
#!/bin/bash
for img in $(find assets -type f -name "*.png" -o -name "*.jpg"); do
  imgname=$(basename "$img")
  if ! rg -q "$imgname" --glob "*.{md,html,jsx,tsx}" .; then
    echo "Unused image: $img"
  fi
done
```

---

## 📞 Support

Pro otázky nebo problémy:
1. Zkontroluj tento dokument a související guides
2. Konzultuj s týmem před velkými změnami
3. Vytvoř issue s labelem `cleanup` pro diskusi

---

**Poslední aktualizace**: 2024-01-09  
**Verze**: 1.0.0
