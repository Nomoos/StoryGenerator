# Návrh systému pro generování a distribuci short videí
# Short Video Generation and Distribution System Design (CS)

**Verze:** 1.0  
**Datum:** 2025-01-09  
**Status:** Návrh specifikace

---

## Přehled

Tento dokument poskytuje kompletní návrh systému pro automatizované vytváření a distribuci krátkých videí (YouTube Shorts, Instagram Reels, TikTok) s důrazem na:

- **Monetizaci** v regionech s nejvyšším CPM (USA, Kanada, Německo, UK, Skandinávie, Austrálie, Japonsko)
- **Lokalizaci** napříč jazyky, hlasy a kulturními kontexty  
- **Analýzu obsahových mezer** pro identifikaci nedostatečně pokrytých témat s vysokým potenciálem
- **Automatizaci a škálování** pro udržitelnou a nákladově efektivní produkci obsahu

**Hlavní diferenciátory:**
- Multi-regionální lokalizace s nativními hlasy a kulturní adaptací
- AI-řízená identifikace obsahových mezer pro rychlý organický růst
- Hybridní AI architektura (C# orchestrace + Python ML) pro optimální poměr cena/kvalita
- Platformově specifická optimalizace (9:16 formát, titulky, trendové audio)

> **Poznámka:** Tento dokument je zkrácená česká verze. Pro kompletní technickou specifikaci viz [SHORT_VIDEO_SYSTEM_DESIGN.md](./SHORT_VIDEO_SYSTEM_DESIGN.md).

---

## Obsah

1. [Strategický rámec](#1-strategický-rámec)
2. [Pipeline generování obsahu](#2-pipeline-generování-obsahu)
3. [Strategie lokalizace](#3-strategie-lokalizace)
4. [Výzkum trhu a obsahové mezery](#4-výzkum-trhu-a-obsahové-mezery)
5. [Automatizace a škálování](#5-automatizace-a-škálování)
6. [Monetizace a expanze](#6-monetizace-a-expanze)
7. [Implementační plán](#7-implementační-plán)

---

## 1. Strategický rámec

### 1.1 Cíle

**Hlavní cíl:**  
Automaticky (nebo poloautomaticky) vytvářet krátká videa s vysokým engagementem, cílící na publikum v zemích s nejvyšším CPM.

**Metriky úspěchu:**
- **CPM:** $8-15 v cílových regionech (US, CA, DE, UK, AU)
- **Watch Time:** >80% průměrná doba sledování
- **Engagement Rate:** >5% (lajky + komentáře + sdílení / zobrazení)
- **Míra růstu:** >10% měsíční růst odběratelů
- **Náklady na produkci:** <$2 na video (včetně API nákladů)

### 1.2 Cílové regiony a CPM vrstvy

| Vrstva | Regiony | Odhad CPM | Priorita | Poznámky |
|--------|---------|-----------|----------|----------|
| **Vrstva 1** | USA, Kanada, Německo, UK, Austrálie | $8-15 | P0 | Nejvyšší monetizace |
| **Vrstva 2** | Skandinávie, Japonsko, Švýcarsko | $6-10 | P1 | Vysoké CPM, vyžaduje lokalizaci |
| **Vrstva 3** | Francie, Nizozemsko, Singapur, J. Korea | $4-8 | P1 | Rostoucí trhy |
| **Vznikající** | SAE, S. Arábie, Polsko, Česko | $2-6 | P2 | Nižší CPM, menší konkurence |

### 1.3 Diferenciátory obsahu

1. **Lokální adaptace:**
   - Nativní jazykové voiceovery (nejen titulky)
   - Regionální reference a příklady
   - Kulturně specifický humor a vyprávění
   - Integrace lokálních trendů

2. **Cílení na obsahové mezery:**
   - Analýza nedostatečně pokrytých témat pomocí AI
   - Identifikace "rostoucích trendů" před saturací
   - Zaměření na témata s vysokým vyhledáváním ale nízkou kvalitou obsahu

3. **Kvalita ve velkém měřítku:**
   - Hybridní AI pipeline (lokální + cloudové modely)
   - Automatické hodnocení kvality a vylepšování
   - A/B testování háčků, náhledů, titulků

---

## 2. Pipeline generování obsahu

### 2.1 Přehled

Pipeline transformuje **téma** na **lokalizované, platformově připravené video** v 6-8 fázích:

```
Téma → Scénář → Voiceover → Vizuály → Sestavení → Post-produkce → Nahrání
  ↓       ↓         ↓          ↓          ↓            ↓             ↓
(AI)    (AI)     (TTS)      (AI Art)   (FFmpeg)    (Editace)     (APIs)
```

### 2.2 Fáze pipeline

#### Fáze 1: Výběr tématu a analýza trendů (5-10 minut)
- **AI Model:** Mistral 7B nebo Llama 3.1 8B (lokální)
- **Zdroje dat:** Google Trends, YouTube Trending, TikTok, Reddit
- **Výstup:** 20-50 prioritizovaných video konceptů s háčky

#### Fáze 2: Generování scénáře (2-5 minut)
- **AI Model:** Hybrid - Llama 3.1 8B (návrhy) → GPT-4o (vylepšení)
- **Délka:** 30-60 sekund (60-100 slov)
- **Náklady:** $0.02-0.05 na finální scénář

#### Fáze 3: Generování voiceoveru (1-3 minuty)
- **TTS poskytovatel:** ElevenLabs (primární) nebo Azure TTS
- **Lokalizace:** Nativní přízvuky pro každý region
- **Kvalita:** 48kHz, normalizováno na -16 LUFS

#### Fáze 4: Generování vizuálů (5-15 minut)
- **Nástroje:** SDXL, Stable Diffusion, Stock APIs
- **Formát:** 9:16 (portrait, 1080x1920)
- **Styly:** Minimalistický, stock footage, AI-generované, motion graphics

#### Fáze 5: Generování titulků (1-2 minuty)
- **Nástroj:** WhisperX (word-level alignment)
- **Styly:** Dynamické slovo-po-slově (TikTok styl)
- **Multi-jazyk:** Primární + volitelný překlad

#### Fáze 6: Sestavení videa (2-5 minut)
- **Nástroj:** FFmpeg
- **Formát:** MP4, H.264, 1080x1920, 30 fps
- **Kvalita:** 8-12 Mbps (video), 192 kbps (audio)

#### Fáze 7: Post-produkce a metadata (1-2 minuty)
- Generování náhledu
- Branding (intro/outro)
- SEO-optimalizovaný titulek
- Hashtags (20-30 relevantních)

---

## 3. Strategie lokalizace

### 3.1 Multi-regionální přístup

**Filosofie:** Skutečná lokalizace jde za překlad—adaptuje obsah tak, aby rezonoval s lokální kulturou, humorem a trendy.

### 3.2 Vrstvy lokalizace

| Vrstva | Regiony | Hloubka lokalizace | Cenový multiplikátor |
|--------|---------|-------------------|---------------------|
| **Plná** | US, UK, DE, JP | Přepsání scénáře + nativní hlas + lokální příklady | 1.5x |
| **Standardní** | CA, AU, FR, ES | Překlad + nativní hlas + kulturní revize | 1.2x |
| **Základní** | Ostatní | Překlad + generický hlas | 1.0x |

### 3.3 Komponenty lokalizace

1. **Jazyk a hlas:**
   - Překlad skrze DeepL nebo GPT-4
   - Výběr hlasu podle regionu a demografických dat
   - Správné přízvuky a dialekty

2. **Kulturní adaptace:**
   - US: Pop-kulturní reference, sportovní analogie
   - UK: Britský humor, podhodnocení, fotbal
   - DE: Zaměření na efektivitu, přesnost
   - JP: Úrovně zdvořilosti, anime/manga reference

3. **Lokalizace titulků:**
   - Primární: Odpovídá jazyku voiceoveru
   - Sekundární: Anglický překlad (pro mezinárodní trhy)

4. **Vizuální lokalizace:**
   - Překlad textu v obrázcích
   - Kulturně vhodná symbolika barev
   - Vyhýbání se kulturně necitlivému obsahu

---

## 4. Výzkum trhu a obsahové mezery

### 4.1 Framework analýzy obsahových mezer

**Definice:** Obsahová mezera = Vysoká poptávka (objem vyhledávání) + Nízká nabídka (kvalitní obsah)

**Skóre příležitosti:**
```
Příležitost = (Objem vyhledávání × Rychlost trendu) / (Konkurence × Kvalita obsahu)
```

### 4.2 Zdroje dat

| Zdroj | Metrika | Frekvence | Použití |
|-------|---------|-----------|---------|
| Google Trends | Zájem o vyhledávání v čase | Denně | Identifikace rostoucích témat |
| YouTube Trending | Nejsledovanější shorts | Denně | Analýza úspěšných formátů |
| TikTok Creative Center | Výkonnost hashtagů | Hodinově | Zachycení virálních trendů |
| Reddit Trending | Upvotes, komentáře | Hodinově | Objevování niche zájmů |

### 4.3 Proces identifikace mezer

1. **Agregace trendů** ze všech zdrojů
2. **Analýza konkurence** (počet videí, průměrné zobrazení, kvalita)
3. **Skóre příležitosti** (0-100 bodů)
4. **Regionální analýza mezer** (co funguje v US vs. DE vs. JP)

### 4.4 Příklady obsahových mezer

**Vysoká příležitost (80-100 bodů):**
- "AI nástroje pro [vznikající profese]" - vysoké vyhledávání, nízká kvalita
- "[Tech téma] jednoduše vysvětleno" - komplexní témata bez přístupného obsahu

**Střední příležitost (50-79 bodů):**
- "[Zavedené téma] 2025 update" - aktualizace zastaralého obsahu

---

## 5. Automatizace a škálování

### 5.1 CMS Architektura

**Komponenty:**
1. **Content Repository:** SQLite (dev) → PostgreSQL (prod)
2. **Asset Storage:** Lokální file system (dev) → S3/Azure Blob (prod)
3. **Workflow Engine:** Python Celery pro fronty úloh
4. **API Layer:** FastAPI pro externí integrace

### 5.2 Automatizace workflow

**Technologie:**
- **Orchestrace:** C# (.NET 9)
- **ML Inference:** Python
- **Databáze:** PostgreSQL
- **Cache/Fronta:** Redis
- **Video zpracování:** FFmpeg

### 5.3 Batch zpracování

**Scénáře:**
1. **Noční dávka:** Zpracování všech scénářů → voiceovery → videa
2. **Lokalizační dávka:** Generování všech lokálních variant úspěšných videí
3. **Re-render dávka:** Aktualizace brandingu napříč existujícími videi

### 5.4 A/B testování

**Testované proměnné:**
- Titulky (5 variant na video)
- Náhledy (3-5 variant)
- Háčky (první 3 sekundy)
- CTA (závěr)
- Kombinace hashtagů

---

## 6. Monetizace a expanze

### 6.1 Zdroje příjmů

**Primární:**
1. **Příjmy z reklam na platformách:**
   - YouTube Shorts Fund / AdSense
   - TikTok Creator Fund
   - Instagram Reels Play Bonus

2. **Očekávané příjmy (na 1M zobrazení):**
   - US: $1,000 - $1,500
   - UK/CA/DE: $800 - $1,200
   - Vrstva 2: $500 - $800
   - Vznikající: $200 - $500

**Sekundární:**
3. **Affiliate marketing**
4. **Brand dealy**
5. **Vlastní produkty/služby**

### 6.2 Časová osa monetizace

**Měsíc 1-3: Založení**
- Zaměření na kvalitu obsahu a konzistenci
- Budování základny odběratelů (cíl: 10k na platformu)
- Žádost o monetizační programy

**Měsíc 4-6: Aktivace příjmů**
- Dosažení monetizačních prahů
- První příjmy: $500-2,000/měsíc

**Měsíc 7-12: Škálování**
- Multi-kanálové publikování (3+ platformy)
- Expanze lokalizace (5+ jazyků)
- Cílový příjem: $5,000-15,000/měsíc

**Rok 2: Optimalizace**
- Zaměření na high-CPM regiony (pravidlo 80/20)
- Automatizovaná lokalizace top performerů
- Cílový příjem: $20,000-50,000/měsíc

### 6.3 Struktura nákladů

**Fixní náklady (měsíčně):**
- AI API náklady: $200-500 (GPT-4, ElevenLabs)
- Storage/hosting: $50-100 (S3, databáze)
- Nástroje/předplatná: $100-200
- **Celkem:** $350-800/měsíc

**Variabilní náklady (na video):**
- Generování scénáře: $0.02-0.05
- Voiceover (TTS): $0.10-0.30
- Generování vizuálů: $0.05-0.50
- Zpracování: $0.05-0.10
- **Celkem:** $0.22-0.95 na video

**Náklady na lokalizaci (na video):**
- Překlad: $0.05-0.10 (automatizovaný)
- Dodatečný voiceover: $0.10-0.30
- **Celkem:** $0.15-0.40

---

## 7. Implementační plán

### Fáze 1: MVP (Týdny 1-4)

**Cíl:** Jednoregionový, pouze anglický systém s jádrem pipeline

**Týden 1:** Založení
- [x] Revize existujících komponent pipeline
- [ ] Nastavení databázového schématu (PostgreSQL)
- [ ] Konfigurace API integrací
- [ ] Vytvoření základních konfiguračních souborů

**Týden 2:** Jádro pipeline
- [ ] Implementace modulu agregace trendů
- [ ] Vybudování generování scénářů (lokální + cloud hybrid)
- [ ] Integrace generování voiceoveru
- [ ] Připojení k existujícímu generování vizuálů

**Týden 3:** Sestavení a QA
- [ ] Pipeline sestavení videa (FFmpeg)
- [ ] Generování titulků (WhisperX)
- [ ] Kontroly kvality a validace
- [ ] Generování metadat

**Týden 4:** Testování a iterace
- [ ] End-to-end testování s reálnými daty
- [ ] Optimalizace výkonu
- [ ] Vylepšení error handlingu
- [ ] Dokumentace

**Dodávky:**
- Funkční pipeline pro anglický (US) trh
- 10-20 testovacích videí
- Základní analytický dashboard
- Deployment na jednom serveru

### Fáze 2: Lokalizace (Týdny 5-8)

**Cíl:** Multi-regionová podpora s automatizovanou lokalizací

**Dodávky:**
- 5 podporovaných regionů (US, UK, CA, AU, DE)
- Automatizovaná lokalizační pipeline
- Náklady na video < $2
- Skóre kvality > 80%

### Fáze 3: Škálování a automatizace (Týdny 9-12)

**Cíl:** Vysokoobjemová produkce s plnou automatizací

**Dodávky:**
- Kapacita 50-100 videí/den
- Automatizovaná end-to-end pipeline
- Analytický dashboard s KPI
- Připraveno na monetizační programy

### Fáze 4: Monetizace (Měsíce 4-6)

**Cíl:** Generování příjmů a expanze

**Dodávky:**
- Dosažení monetizačních prahů
- Expanze do 10+ regionů
- Optimalizace příjmů ($5k+/měsíc cíl)

---

## Závěr

Tento systém poskytuje kompletní řešení pro automatizované vytváření a distribuci krátkých videí s důrazem na:

✅ **Monetizaci** v nejvyšších CPM regionech  
✅ **Lokalizaci** s nativními hlasy a kulturní adaptací  
✅ **Analýzu obsahových mezer** pro konkurenční výhodu  
✅ **Automatizaci** pro škálování na 50-100+ videí denně  
✅ **Integraci** s existující StoryGenerator pipeline  

**Další kroky:**
1. Revize a schválení návrhu
2. Nastavení vývojového prostředí
3. Začátek Fáze 1 implementace
4. Týdenní progress meetings

---

## Reference

**Kompletní anglická specifikace:**  
[SHORT_VIDEO_SYSTEM_DESIGN.md](./SHORT_VIDEO_SYSTEM_DESIGN.md)

**Související dokumenty:**
- [VIRAL_VIDEO_REQUIREMENTS.md](./VIRAL_VIDEO_REQUIREMENTS.md)
- [YOUTUBE_CONTENT_STRATEGY.md](./YOUTUBE_CONTENT_STRATEGY.md)
- [ai-model-comparison-for-game-design.md](./gpt-research/ai-model-comparison-for-game-design.md)

**Externí zdroje:**
- YouTube Creator Academy
- TikTok Creative Center
- ElevenLabs API dokumentace
- WhisperX GitHub

---

**Status dokumentu:** ✅ Kompletní  
**Poslední aktualizace:** 2025-01-09  
**Další revize:** 2025-02-09
