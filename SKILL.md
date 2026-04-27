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
Neighborhoods that are fully gentrified and emerged — already on the radar as cool, mainstream among culturally-aware locals — but not chic, not luxury, not exclusive. They have a stable identity with preserved heterogeneity, either across the whole neighborhood or in specific corridors.

**Key signals:**
- Already established as "cool" or "hip" in editorial sources — present in "best/coolest neighborhoods [city]" guides, not "emerging" or "to watch" lists
- Described with language like: hip, eclectic, artsy, indie, creative, vibrant — never luxury, exclusive, or high-end
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

**Layer 1 — web_search (primary discovery)**
Start with editorial sources — fast, efficient, and sufficient to build a candidate list. Broad Reddit subreddits (AskNYC, AskSF, FoodNYC, etc.) are explicitly excluded from this layer: too noisy, dominated by news/politics/lifestyle posts, and returned near-zero useful signal in practice.

**Cat 1 and Cat 2 require different query intent — run both tracks in parallel.**

```
# Cat 1 discovery — emerging neighborhoods
web_search: "Time Out coolest neighborhoods world [current year] [city]"
web_search: "[city] neighborhoods to watch [year] StreetEasy"
web_search: "[city] up and coming neighborhood [year]"
```

- Time Out global ranking targets community spirit, everyday vitality, local character — most aligned source for Cat 1
- Neighborhoods that appeared 2–4 years ago in Time Out are often at peak emergence now
- StreetEasy search trends are a reliable Cat 1 proxy (search interest = flight demand, not yet price inflation)
- Cat 2 neighborhoods are past their emergence phase and will never appear in these results

```
# Cat 2 discovery — established cool neighborhoods
web_search: "[city] coolest neighborhoods locals guide [year]"
web_fetch: Time Out [city] neighborhoods guide  (full guide, not the global ranking)
web_fetch: Infatuation [city] neighborhood guide
```

- Cat 2 neighborhoods appear in "best/coolest neighborhoods [city]" guides — not in "emerging" or "to watch" lists
- Editorial fingerprint: described as hip, cool, eclectic, artsy, indie, creative — never luxury, exclusive, or high-end
- This language cluster is the key signal: same words used for Williamsburg ("made Brooklyn cool", "hip", "eclectic culinary destination") and LES ("artsy", "laid-back and irreverent", "alternative bars") but never for excluded neighborhoods (SoHo = luxury boutiques, Meatpacking = exclusive)
- Google sometimes surfaces real Reddit threads in results — fetch them via `web_fetch` if accessible

**Layer 2 — Reddit MCP (targeted validation, not discovery)**
Once Layer 1 has produced a candidate list, use Reddit MCP on the specific neighborhood subreddit to validate each candidate and detect the flight signal. **Do not use broad city subreddits (Ask[City], [City]food) — they produced no useful neighborhood signal in testing.**

Two complementary MCP tools:

| MCP | Tools | Source | Rate limit | Role |
|-----|-------|--------|------------|------|
| `pullpush` | `search_submissions`, `search_comments` | PullPush archive (up to May 2025) | 15 req/min | Historical depth, older threads |
| `reddit-buddy` | `search_reddit`, `get_post_details` | Reddit real-time | 10 req/min | Recent validation, 2024–2025 posts |

```
# Validate each candidate on its own subreddit
pullpush/search_submissions: subreddit=[neighborhood] limit=20 sort_type=num_comments
reddit-buddy/search_reddit: query="neighborhood vibe locals" subreddit=[neighborhood]
```

**Note on PullPush scores:** All scores are archived as 1 — useless. Use `num_comments` as engagement proxy. **Skip posts with 0 comments entirely.**

**Reading for the flight signal:**
The flight signal does NOT appear as a literal phrase. It surfaces *in the comments* of neighborhood advice threads. Fetch high-comment threads and read for patterns like: "check X, it's like the old Y", "X is what Y used to be 5 years ago".
```
pullpush/search_comments: link_id=[post_id] limit=50
reddit-buddy/get_post_details: post_id=[post_id]
```

**When to skip Layers 1 and 2 entirely:** If the user has already specified the neighborhood (e.g. "find venues in Bernal Heights"), skip neighborhood identification entirely and go directly to **Step 2 — Venue Search**.

**Layer 3 — Hyper-local neighborhood press** → `web_search` + `web_fetch`
The existence of a neighborhood-specific publication is itself a strong signal of community identity. These outlets cover a neighborhood *from the inside* with no tourist audience.
```
web_search: "[neighborhood name] local newspaper OR blog [city]"
web_fetch: the publication's homepage if found
```
- Examples of the type: Star-Revue (Red Hook), Bushwick Daily (Bushwick/Ridgewood)
- Look for: articles describing the community, artisans, local businesses, residents — not "best restaurants in X" listicles

**Layer 4 — Real estate & gentrification analyses (indicator only)** → `web_search`
Useful as a signal but NOT the primary ranking criterion. A neighborhood absent from StreetEasy may be exactly the right one.
```
web_search: "[city] neighborhoods to watch [year]"
web_search: "[city] up and coming neighborhood [year]"
```
- Curbed, Axios Local, local press preferred
- Prefer articles from 1–4 years ago — captures emergence before peak

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

### Phase 1 — DISCOVERY via Reddit MCP

Reddit is where locals recommend to locals — no economic incentive, no SEO. Neighborhood confirmed → search venues per category on the neighborhood's own subreddit first.

**MCP tools:**

| MCP | Tool | Source | Rate limit | Role |
|-----|------|--------|------------|------|
| `pullpush` | `search_submissions`, `search_comments` | PullPush archive (up to May 2025) | 15 req/min | Historical depth, older threads |
| `reddit-buddy` | `search_reddit`, `get_post_details` | Reddit real-time | 10 req/min | Recent posts, 2024–2025 validation |

**Subreddit priority for venue discovery:**
1. `r/[neighborhood]` (e.g. `r/Ridgewood`, `r/Bushwick`, `r/InnerRichmond`) — strongest local signal
2. `r/[City]food` / `r/Food[City]` (e.g. `r/FoodNYC`) with neighborhood name
3. `r/Ask[City]` — venue threads surface occasionally

**Search each category separately** — combining terms reduces results:

```
# Bars
pullpush/search_submissions: subreddit=[neighborhood] q="bar" limit=20
pullpush/search_submissions: subreddit=[city]food q="[neighborhood] bar" limit=15
reddit-buddy/search_reddit: query="[neighborhood] bar" subreddit=[neighborhood]

# Cafés
pullpush/search_submissions: subreddit=[neighborhood] q="coffee" limit=20
pullpush/search_submissions: subreddit=[city]food q="[neighborhood] coffee café" limit=15

# Restaurants
pullpush/search_submissions: subreddit=[neighborhood] q="restaurant" limit=20
pullpush/search_submissions: subreddit=[city]food q="[neighborhood] restaurant" limit=15
reddit-buddy/search_reddit: query="[neighborhood] restaurant" subreddit=[neighborhood]
```

**Getting full thread content:**
```
pullpush/search_comments: link_id=[post_id] limit=50
reddit-buddy/get_post_details: post_id=[post_id]
```

**Reading results — prioritize:**
- **Skip posts with 0 comments entirely**
- Comments describing atmosphere, clientele, or vibe — not just a bare venue name
- Posts dated within the last 3 years
- reddit-buddy for anything post-May 2025

---

### Phase 2 — VALIDATION via `web_search` / `web_fetch`

Once venues are identified from Reddit, use web search to fill in the practical details before presenting to the user.

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
- If address or hours are found → include them in the output
- If info is not available → recommend the venue anyway, note "adresse et horaires à vérifier" without disqualifying it
- Instagram is a useful signal for "still active" — note a dead account as a caveat, not a disqualifier

---

### Review volume — important rule
Do NOT sort or prioritize venues by number of reviews. A venue with 200 authentic local reviews may outrank one with 2,000 tourist reviews. Volume is not a quality signal for this profile.

### When Reddit MCP results are insufficient
Flag explicitly to the user: *"Reddit results for [neighborhood] in [city] are limited — do you have local knowledge or contacts who could supplement?"* Do not fill gaps with generic recommendations.

### Fallback — web_search (when both MCPs are unavailable)

**Structural limitation:** Reddit deliberately blocks Google indexing (post-June 2023). `site:reddit.com` is not supported by web_search, and reddit.com cannot be fetched. This means web_search is **structurally insufficient for Cat 1** (emerging, underdocumented neighborhoods) — the flight signal simply doesn't surface this way.

**What web_search can do:**
- Cat 2 validation: established cool neighborhoods have editorial coverage (Eater, local press, food blogs)
- Venue validation: address, hours, whether it still exists
- Supplement sparse MCP results with non-Reddit editorial sources

**Queries that work for Cat 2:**
```
web_search: "best [category] [neighborhood] [city]"
web_search: "local [category] [neighborhood] [city] guide"
web_search: "[city] [neighborhood] underrated [category] 2024"
web_fetch: Eater [city] neighborhood guide, local food blog articles
```

**What doesn't work (do not attempt):**
- `site:reddit.com` — operator not supported
- Fetching reddit.com or old.reddit.com — blocked
- Fetching Redlib/Libreddit frontends — dead or bot-protected
- Searching "best X [city] reddit" and expecting actual Reddit thread content — Google returns aggregator pages, not Reddit posts

**If MCP is unavailable and web_search is insufficient for Cat 1:**
Tell the user explicitly: *"Je ne peux pas accéder à Reddit en ce moment. Les résultats pour les quartiers émergents (Cat 1) seront limités — les sources web couvrent mieux les quartiers déjà établis."*

### Fallback editorial sources (if Reddit results < 5 relevant posts)
- Independent local blogs, neighborhood guides
- Eater [city], local food/culture press — filter out sponsored content
- Time Out acceptable as last resort — ignore "top 10" lists, look for editorial pieces
- **Never use**: TripAdvisor top lists, Yelp top picks, Google Maps "popular" sorting

---

## Reference Files

- `references/nyc-reference.md` — Full NYC reference list with annotated venues. Read this when validating output quality or when the user asks about NYC specifically.
