---
name: ridgewood
description: Use this skill whenever the user asks for neighborhood or address recommendations in a city using the "Ridgewood" profile. Trigger when the user says "use the Ridgewood skill", "apply the Ridgewood profile", or asks for local/authentic neighborhood and venue recommendations for a specific city. This skill identifies the right neighborhoods first, then finds specific cafés, bars, and restaurants that match a very specific local/authentic/non-touristy profile. Always use this skill before attempting any city recommendation if the Ridgewood profile is mentioned.
---

# Ridgewood Skill — Local Neighborhood & Venue Recommender

## What this skill does

This skill guides Claude through a two-step process for any city:
1. **Identify the right neighborhoods** matching a specific urban profile
2. **Find specific venues** (cafés, bars, restaurants) within those neighborhoods

The reference city is **New York City**. When in doubt about whether a recommendation is on-target, compare it against the NYC reference list in `references/nyc-reference.md`.

---

## The Persona

The person using this skill is an **urban-savvy, culturally aware adult** — not a tourist, not an urban explorer. They know cities well and want to go slightly off the beaten track without completely losing their bearings.

**Primary use case:** Discovering a city or neighborhood they don't know. Deepening knowledge of a familiar neighborhood is a secondary mode, triggered explicitly by the user (e.g. "give me more off-track options").

**What they're looking for — by priority:**
1. **Social experience (60%)** — places with an organic neighborhood life. Regulars, people who know each other, a sense that the room has its own rhythm independent of any visitor. The ideal signal: stumbling into a café and running into a local friend you weren't expecting to see.
2. **Aesthetic experience (40%)** — places that feel undesigned, unformatted, not built to please. A worn bar beats a curated one. But aesthetic alone without social life is not enough.

**Group and solo use:**
- Primarily explored in a group (bars, dinners, evenings out)
- Solo use is valid too, especially cafés and restaurants
- The goal is not to meet strangers or integrate socially — it's to feel at home in the neighborhood's natural flow, with their own people or alone

**Relationship to authenticity:**
- Cat 1 neighborhoods (Emerging) = top of the range, the real discovery
- Cat 2 neighborhoods (Established Cool) = a very good evening, all zones recommended
- Being the only outsider in the room = non-disqualifying if all other signals are strong, but signals "excursion mode" — surface only when user pushes for more off-track

**Price:** Not a criterion. Pays for quality regardless of neighborhood or price point.

**Notoriety:** Not a disqualifier. A well-documented address with a local clientele is fully valid. What matters is who's actually in the room, not how much press coverage it has received.

**Mobility:** Not a problem. Will take the subway 40 minutes for the right address. Transit isolation can be a charm depending on other signals — it's never a filter in either direction.

**Time of day:** All moments covered equally — morning café, lunch, afternoon, dinner, late bar. No bias toward evening.

**Cuisine and drinks:** Fully open. Quality and authenticity of execution are the only criteria — no bias toward or against any cuisine, wine, beer, or format.

**Scope:** Food & drink is the current focus. Other venue types (vintage stores, record shops, bookstores, markets, cultural spaces) are noted as Phase 2 — the persona is interested in all of these, but skill development prioritizes food & drink quality first.

**What they don't want:**
- To be treated like a tourist
- Luxury, exclusivity, dress codes, Instagram bait
- Warnings that disqualify a neighborhood they already know is fine
- A bar where everyone arrived from somewhere else for the occasion

---

## Two-Category Neighborhood System

Neighborhoods are classified into two categories. Both are valid recommendations — they serve different needs and moments.

### Category 1 — Emerging
Neighborhoods where gentrification is actively in progress. Legacy businesses still dominant. Social mix highly visible. Not yet indexed by mainstream press. The Reddit signal is "have you tried X instead of [more advanced neighbor]?" — locals flee *toward* these neighborhoods from more gentrified ones.

**Temporal analog:** Ridgewood is Williamsburg 15 years ago. Ridgewood is Bushwick 5 years ago. Highland Park (LA) is Silverlake 10–15 years ago.

**Key signals:**
- Legacy businesses (bodegas, old-school diners, ethnic markets) still outnumber new arrivals
- Reddit describes it as an *alternative to* a more known neighbor — the "flight from X" signal
- Real estate prices rising but not yet homogeneous
- Hyper-local press naissante or recently emerged
- Few or no mainstream press mentions

**Default rule:** When in doubt, keep a neighborhood in Category 1. A neighborhood stays in Category 1 as long as it is not *clearly* in late-stage gentrification. Bushwick, for example, remains Category 1 despite being well-documented — it has not yet homogenized.

**NYC examples:** Ridgewood (Queens), Red Hook (Brooklyn), Flatbush (Brooklyn)

---

### Category 2 — Established Cool
Neighborhoods where gentrification is advanced but heterogeneity is preserved — either in the whole neighborhood or in specific streets/zones. These neighborhoods are known to locals and culturally documented, but not tourist traps. They have a stable identity with enough diversity to remain interesting.

**Key signals:**
- Longtime creative residents feel nostalgia for "what it used to be" — but the neighborhood still works
- Reddit describes it as "still good if you avoid X" or "X street is the real neighborhood"
- Heterogeneity survives in secondary streets, specific corridors, or legacy pockets
- Mainstream press has covered it, but locals know how to navigate around the tourist layer

**Critical rule for Category 2:** Always present the neighborhood **in its entirety**. All zones are recommended — gentrified zones included, as they still contain good addresses worth visiting. The internal mapping is informational, not a filter. Note gentrification inline without disqualifying. Example: Williamsburg/Bedford Ave has great addresses (The Lot Radio, McCarren, Bird of a Feather) with a note that gentrification is advanced — Montrose/Lorimer/Graham are flagged as more local in character, gentrification not complete. Never reduce a Cat 2 neighborhood to only its most authentic zone.

**NYC examples:** Williamsburg (Brooklyn — whole neighborhood, heterogeneity mapped by zone), Bushwick (Brooklyn — borderline Cat 1/2, keep in Cat 1 until clearly homogenized)

---

### What gets excluded entirely
Neighborhoods that are fully homogenized, tourist-facing, or luxury-defined. No category — simply not recommended. Examples: SoHo, Montecito (Santa Barbara), Meatpacking District.

### Ultra off-track neighborhoods (mention only on demand)
Neighborhoods with extreme cultural diversity and very low gentrification (e.g. Jackson Heights, Flushing, Sunset Park) are not part of the default recommendation flow. They represent a different register — occasional excursion territory for the persona, not the baseline. Mention them only if: (a) Reddit search surfaces them strongly and unprompted, or (b) the user explicitly asks for "even more off the beaten track."

---

## Step 1 — Neighborhood Identification & Validation

### Critical principle
**Do not rely on internal knowledge to propose neighborhoods.** Claude's training data is incomplete and biased toward well-documented, English-language cities. Emerging neighborhoods by definition appear late in indexed sources. Always search first — use internal knowledge only as a last resort, and flag it explicitly when you do.

### Search sequence (run in this order)

**Layer 1 — Reddit API (primary source)**
Reddit is where locals recommend to locals — no economic incentive, no SEO. Use `reddit_search.py` directly.

```bash
python reddit_search.py --query "[city] where do locals live neighborhood" --limit 15
python reddit_search.py --query "[city] underrated neighborhoods" --subreddit [citysubreddit] --limit 15
python reddit_search.py --query "[city] up and coming neighborhood" --limit 15
python reddit_search.py --query "[city] gentrification neighborhood locals" --limit 15
python reddit_search.py --query "[city] instead of [known neighborhood]" --limit 10
```

The last query is the **flight signal** — locals recommending X as an alternative to a more known neighbor is the strongest Category 1 indicator.

Prioritize posts with `score` > 20 and `top_comments` that describe a neighborhood's atmosphere or clientele. `date` filtering (last 2 years) is handled automatically by the script.

**Layer 2 — Time Out "Coolest Neighborhoods" annual list**
This is the single most aligned cultural source for this profile. Time Out's methodology explicitly targets neighborhoods with community spirit, everyday vitality, and local character — not tourist centrality or luxury.
- Search: `Time Out coolest neighborhoods world [current year] [city]`
- Also check previous years (2023, 2024) — neighborhoods that appeared 2–4 years ago are often at peak emergence now
- Note: Time Out Brooklyn neighborhoods to watch (Flatbush 2024, Fort Greene 2023, Red Hook 2025) follow a pattern of authentic emerging areas year over year

**Layer 3 — Hyper-local neighborhood press**
The existence of a neighborhood-specific publication is itself a strong signal of community identity. These outlets cover a neighborhood *from the inside* with no tourist audience.
- Search: `"[neighborhood name]" local newspaper OR blog "[city]"`
- Examples of the type: Star-Revue (Red Hook), Bushwick Daily (Bushwick/Ridgewood)
- Look for: articles describing the community, artisans, local businesses, residents — not "best restaurants in X" listicles

**Layer 4 — Real estate & gentrification analyses (indicator only)**
Useful as a signal but NOT the primary ranking criterion. A neighborhood absent from StreetEasy may be exactly the right one.
- StreetEasy annual "most searched neighborhoods" (US cities)
- Curbed, Axios Local, local press "neighborhoods to watch"
- Prefer articles from 1–4 years ago — captures emergence before peak
- Search: `"[city]" "neighborhoods to watch" OR "up and coming" [year]`

**Layer 5 — Internal knowledge (last resort only)**
If layers 1–4 yield insufficient results, Claude may draw on training knowledge — but must flag this explicitly: *"I'm supplementing with internal knowledge here as search results were limited — treat these suggestions as hypotheses to validate."*

### Validation criteria

**INCLUDE (Category 1 — Emerging):**
- Gentrification is recent (last 5–10 years) or still actively in progress
- Social mix is highly visible: long-term residents + immigrant communities + artists/creatives coexist
- Legacy businesses still outnumber new arrivals
- Reddit "flight signal": locals recommend it as alternative to a more advanced neighbor
- Hyper-local press exists or is naissante

**INCLUDE (Category 2 — Established Cool):**
- Gentrification advanced but neighborhood not homogenized
- Heterogeneity survives in specific streets, corridors, or legacy pockets
- Reddit describes it defensively: "still good if you avoid X"
- Has a documented local identity that predates and survives tourist attention
- Internal zoning possible: some parts valid, others to avoid

**POSITIVE SIGNALS (elevate any neighborhood):**
- **Transit isolation** — poor or inconvenient connection to city center is a strong positive signal
- Hyper-local press exists for this neighborhood
- Appears on Time Out "coolest neighborhoods" list (current or past 1–3 years)
- Described with language like: "village feel", "community", "locals", "artisans", "hidden"

**EXCLUDE entirely (no category):**
- Dominant clientele is tourists or high-income/exclusive
- Gentrification fully complete: neighborhood homogenized, diversity lost, pricing uniform
- Too residential with insufficient venue density
- Identity primarily defined by upscale dining, luxury retail, or affluent nightlife

### Ranking logic
Within Category 1, rank by strength of emergence signals — Reddit flight signal, hyper-local press, transit isolation. Within Category 2, rank by richness of preserved heterogeneity and quality of internal zone mapping. Always present Category 1 neighborhoods first, followed by Category 2. A neighborhood invisible to StreetEasy but praised on Reddit and in hyper-local press ranks above a StreetEasy top-10 neighborhood that has lost its social mix.

### NYC Benchmark Neighborhoods

**Category 1 — Emerging**
1. Ridgewood (Queens) — transit-isolated (M train, inconvenient), hyper-local Polish/Dominican/Puerto Rican community, gentrification in early-mid progress, Time Out #4 world 2022, StreetEasy #1 two years running as "neighborhoods to watch"
2. Red Hook (Brooklyn) — no subway (bus B61 + ferry only), village feel, Time Out #1 NYC 2025, strong artisan/creative community, under threat from 122-acre waterfront development plan
3. Flatbush (Brooklyn) — largest Caribbean-American-Latinx community outside the West Indies, Time Out #1 NYC 2024, Black-owned businesses dominant, gentrification still at early stages
4. Bushwick (Brooklyn) — well-documented but not yet homogenized, dense independent venues, strong street energy. Keep in Category 1 until clearly in late-stage gentrification.

**Category 2 — Established Cool**
1. Williamsburg (Brooklyn) — present in its entirety. Bedford Ave and north: over-gentrified, tourist-facing, exclude. Montrose Ave corridor, south toward Flushing Ave, residential blocks around Myrtle Ave: heterogeneous, local crowd, still valid. Always map the neighborhood's internal zones when recommending.
2. Lower East Side (Manhattan) — historic immigrant identity partially intact, dive bar culture, gentrification advanced but heterogeneous pockets survive on side streets off Orchard/Ludlow.

### Output of Step 1
Present neighborhoods grouped by category (Category 1 first, then Category 2). For each Category 2 neighborhood, always include internal zone mapping. Confirm with user before proceeding to Step 2.

---

## Step 2 — Venue Search

### Process
1. For each confirmed neighborhood, search for cafés, bars, and restaurants
2. Filter results against the criteria below — **do not default to highest-rated or most-reviewed**
3. Present results grouped by neighborhood, with a short description of each venue's vibe

### Venue Criteria

#### Cafés
- Independent (or small local group — chains excluded)
- Laptop-friendly in practice (not crowded on weekdays) but not a co-working space
- Social atmosphere — a mix of regulars working, meeting, or just sitting
- No over-designed "concept café" aesthetic (no excessive branding, no performative minimalism)
- Quality coffee is a plus but not the sole criterion

#### Bars
- Dive bars, wine bars, or relaxed cocktail bars — **no upscale/exclusive/dress-code venues**
- Welcoming to walk-ins, not reservation-heavy
- Regular local crowd — not a scene bar or influencer hotspot
- Decor: real, worn, unpretentious — **exclude**: neon signs, fake plants, overly curated "vintage" aesthetic

#### Restaurants
- Independent, ideally owner-operated or with visible ownership
- Cuisine open — quality and authenticity of execution matter more than type
- Serves a local crowd on weekdays — not primarily a weekend destination for visitors
- Price is secondary — the criterion is quality and fit, not budget

### Universal Venue Exclusions (all categories)
- Chains or large groups
- Venues that appear primarily in tourist guides or "best of [city]" listicles
- Overly designed / kitsch interiors (fake flowers, neon décor, "instagrammable" wall art)
- Upscale, exclusive, or dress-code venues
- Do NOT sort or prioritize by number of reviews — a venue with 200 authentic reviews may outrank one with 2,000 tourist reviews

### Positive Signals (not required, but elevate a venue)
- Regulars visibly recognized by staff
- Owner or staff presence on the floor
- Has been around long enough to have a neighborhood identity (but new venues can qualify too)
- Mixed clientele across age, background, and purpose (work, social, date, solo)
- Cultural programming (music, events) that feels organic, not promotional

---

## Output Format

### Neighborhoods
```
## Recommended Neighborhoods — [City]

### Category 1 — Emerging

#### [Neighborhood Name]
**Why it fits:** [2–3 sentences on gentrification stage, social mix, venue density]
**Temporal analog:** [optional — e.g. "This is X neighborhood 10 years ago"]
**Vibe:** [one sentence on street-level energy]

### Category 2 — Established Cool

#### [Neighborhood Name]
**Why it fits:** [2–3 sentences on overall character and why it remains valid]
**More local zones:** [streets/corridors where gentrification is less advanced — flagged positively, not as "the only valid part"]
**Gentrification note:** [one honest sentence — inline, not a warning]
**Vibe:** [one sentence on street-level energy]
```

### Venues
```
## Venues — [Neighborhood Name]

### Cafés
- **[Name]** — [1–2 sentences: what makes it local/authentic, atmosphere, who goes there]

### Bars
- **[Name]** — [1–2 sentences]

### Restaurants
- **[Name]** — [1–2 sentences: cuisine type, why it's authentic, clientele]
```

---

## Search Strategy — Venues

Two tools, two roles. Never swap them.

---

### Phase 1 — DISCOVERY via Reddit API (`reddit_search.py`)

Reddit is where locals recommend to locals — no economic incentive, no SEO. Use the script for all discovery. Do NOT use web search for this phase.

**What Reddit answers:**
- Which neighborhoods match the profile
- Which specific venues are mentioned by locals
- Why a venue is liked (vibe, clientele, atmosphere)
- The "flight signal" — locals recommending X as an alternative to a more known neighbor

**Script location:** `reddit_search.py` in the repo root. Requires `.env` with `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`.

**Calls for neighborhood discovery:**
```bash
python reddit_search.py --query "[city] underrated neighborhoods locals" --subreddit [citysubreddit] --limit 15
python reddit_search.py --query "[city] instead of [known neighborhood]" --limit 10
python reddit_search.py --query "[city] up and coming neighborhood gentrification" --limit 15
```

**Calls for venue discovery (per confirmed neighborhood):**
```bash
# Bars
python reddit_search.py --query "[neighborhood] [city] bar locals" --subreddit [citysubreddit] --limit 10

# Cafés
python reddit_search.py --query "[neighborhood] [city] coffee café" --subreddit [citysubreddit] --limit 10

# Restaurants
python reddit_search.py --query "[neighborhood] [city] restaurant local" --subreddit [citysubreddit] --limit 10

# Broader cross-city
python reddit_search.py --query "where locals eat [neighborhood] [city]" --limit 15
```

**Also target city-specific subreddits:**
- `--subreddit [city]` (e.g. `paris`, `chicago`, `nyc`)
- `--subreddit [city]food` or `--subreddit [city]bar` if they exist

**Reading the JSON output — prioritize:**
- Posts with `score` > 20 and `num_comments` > 10
- `top_comments` that describe atmosphere, clientele, or vibe — not just a venue name
- `date` within the last 2 years (already filtered by the script)
- Ignore comments that are a bare venue name with no context

---

### Phase 2 — VALIDATION via `web_search` / `web_fetch`

Once venues are identified from Reddit, validate each one before presenting it to the user. A venue that no longer exists or has closed is worse than no recommendation.

**What web search/fetch answers:**
- Exact address
- Current opening hours
- Whether the venue still exists (Google Maps, official site)
- Website and Instagram

**Run for each shortlisted venue:**
```
web_search: "[venue name] [city] adresse horaires"
web_search: "[venue name] [city] site officiel OR instagram"
web_fetch: Google Maps page or official website if found
```

**Validation rules:**
- If a venue cannot be confirmed as still open → do not recommend it, flag it as unverifiable
- If hours are only available from a source older than 1 year → note "hours unverified, check before going"
- Instagram is a useful signal for "still active" — a dead account with no posts in 2+ years is a red flag

---

### Review volume — important rule
Do NOT sort or prioritize venues by number of reviews. A venue with 200 authentic local reviews may outrank one with 2,000 tourist reviews. Volume is not a quality signal for this profile.

### When Reddit results are insufficient
Flag explicitly to the user: *"Reddit results for [neighborhood] in [city] are limited — do you have local knowledge or contacts who could supplement?"* Do not fill gaps with generic recommendations.

### Fallback sources (if Reddit results < 5 relevant posts)
- Independent local blogs, neighborhood guides
- Eater [city], local food/culture press — filter out sponsored content
- Time Out acceptable as last resort — ignore "top 10" lists, look for editorial pieces
- **Never use**: TripAdvisor top lists, Yelp top picks, Google Maps "popular" sorting

---

## Reference Files

- `references/nyc-reference.md` — Full NYC reference list with annotated venues. Read this when validating output quality or when the user asks about NYC specifically.
