# Daily refresh of the tips page

This file is the brief for the scheduled cloud routine that rewrites `tips.json` every morning.
A human can follow it too. The page `index.html` renders whatever the JSON contains; it never
needs to change for a refresh. All three files sit next to each other: at the root of the public
repository `robsmarketing2027/betedge-tips` (served by GitHub Pages, where the routine runs) and
under `tips/` in `robsmarketing2027/betedge` (the development copy).

## Goal

Replace `tips.json` with about 20 selections for **today and the next ~48 hours** that have the
highest estimated chance of winning, across every sport that Hungarian sportsbooks (Tippmixpro,
Vegas.hu) carry: football, tennis, NFL, NBA, NHL, MLB, UFC, basketball, handball, Formula 1, etc.
Then commit and push to `main`.

## Rules (BetEdge hard invariants, plan v4 §14)

1. Research only. Never log in to a bookmaker, never scrape Tippmixpro or Vegas.hu, never place bets.
2. Every probability shows its **source and date**. The words "biztos", "sure", "guaranteed" or any
   claim of certainty never appear anywhere in the JSON.
3. Every tip has a sourced reference price (decimal odds) and a link to where it was read.
4. Free public sources only. If a site returns 403/404, use another; never pay, never bypass.
5. If the research cannot produce at least 12 sound tips, **do not write a partial file**: leave the
   previous `tips.json` in place and stop. A stale file is shown as stale by the page; a bad file is not.
6. Change nothing but `tips.json`. The page and this brief are edited by hand in the betedge repo.

## Procedure

1. `date -u` — compute today's date in **Europe/Budapest** (UTC+2 in summer, UTC+1 from the last
   Sunday of October). All `start` values use that offset, e.g. `2026-10-04T20:45:00+02:00`.
2. Find what is on. Sources that worked (October 2026):
   - Football: ESPN schedule pages (`espn.com/soccer/schedule/_/league/<id>`, show US lines),
     `theanalyst.com` (Opta probabilities), `mightytips.com/football-predictions/<a>-vs-<b>-prediction-DD-MM-YYYY/`
     (3-way odds, team news), `sportsnews.worldsportsbetting.co.za`, `elofoot.com` (model only; treat with care).
     `sportytrader.com`, `oddschecker.com`, `telecomasia.net`, `forebet.com` often return 403.
   - NFL: `foxsports.com/stories/nfl/<season>-nfl-odds-week-<n>-...`, `cbssports.com/betting/news/...` (SportsLine sims),
     `espn.com/nfl/schedule/_/week/<n>/year/<yyyy>/seasontype/2` (kickoff times ET).
   - Tennis: `dimers.com/tennis/predictions` (model probability + best odds, times ET).
   - MLB / NHL / NBA: `espn.com/<sport>/odds`, `covers.com`, `rg.org/news`.
   - UFC: `wagertalk.com/news/mma/...`, `covers.com/ufc/...`.
   Use WebSearch to find the day's articles, then WebFetch the page and read the numbers yourself;
   search-result summaries are often wrong about dates and fixtures.
3. Convert US odds to decimal: positive `+A` → `1 + A/100`; negative `-B` → `1 + 100/B`. Round to 2 decimals.
4. Estimate the probability, in this order of preference:
   - a named model (Opta, ESPN Analytics, Dimers, SportsLine) → `probSrc` names it;
   - otherwise the market, de-vigged: `p = (1/odds_pick) / Σ(1/odds_outcome)` over all outcomes of the
     market → `probSrc: "piaci, árrés nélkül"`;
   - if only the pick's price is known, `p ≈ 0.965 / odds` → `probSrc: "piaci, becsült árrés nélkül"`.
5. Select about 20 tips:
   - start time **after 08:00 Budapest today**, preferably today or tomorrow; nothing already started;
   - estimated probability ≥ 0.58; reference odds ≥ 1.10 where possible (one or two shorter anchors are fine);
   - at most about a third from one sport; prefer events Hungarian books actually offer;
   - rank by probability, highest first; the page re-sorts anyway.
6. For each tip write the Hungarian text: `event` with the home team first ("Hollandia – Szerbia",
   en dash), `pick` as the bettable selection ("Hollandia nyer", "Over 2,5 gól", "Medvegyev nyer"),
   `why` in two or three sentences with the facts that matter **and the main risk**. Hungarian
   spelling for countries and transliterated names (Szabalenka, Medvegyev, Oszaka). No hype.
7. Write `tips.json` (schema below). Validate: `node -e "JSON.parse(require('fs').readFileSync('tips.json','utf8'))"`.
   Check that every `sources` key exists in the `sources` map, every `start` parses, `prob` is in (0,1),
   `odds` > 1.
8. Commit on `main` with the message `tips: YYYY-MM-DD [skip ci]` (the CI build is irrelevant to a data
   change) and push. If the push is rejected, `git pull --rebase` and push again.

## Schema of `tips.json`

```json
{
  "date": "2026-10-03",                       // the Budapest day the tips are for
  "snapshot": "2026-10-03T05:10:00+02:00",     // when the research was closed
  "sources": {
    "key": { "name": "Shown name", "url": "https://..." }
  },
  "tips": [
    {
      "sport": "Foci",                         // Foci, Tenisz, NFL, NBA, NHL, MLB, UFC, Kézilabda, Kosárlabda, F1 …
      "league": "Nemzetek Ligája A",
      "event": "Hollandia – Szerbia",
      "pick": "Hollandia nyer",
      "start": "2026-10-04T20:45:00+02:00",
      "approx": false,                         // true when the time is an estimate (tennis order of play, fight cards)
      "timeNote": "",                          // optional, e.g. "főkártya kezdete"
      "odds": 1.19,                            // reference decimal odds
      "prob": 0.811,                           // estimated win probability, 0–1
      "probSrc": "piaci, árrés nélkül",        // or the model name
      "asOf": "okt. 2.",                       // date of the odds/probability
      "sources": ["mtNed", "espnNl"],          // keys into "sources"
      "why": "Two or three Hungarian sentences: facts, then the main risk."
    }
  ]
}
```

The page computes the break-even odds (`1 / prob`), the profit per stake, the expected number of
winners and the expected result; none of that is stored.
