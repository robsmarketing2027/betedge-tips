# Daily refresh of the tips page

This file is the brief for the cloud routine "BetEdge tips: refresh (manual)". It has no schedule: the
owner starts it by hand (claude.ai/code/routines → Run now), on any day, as often as wanted. A human can
follow it too. The page `index.html` renders whatever the two data files contain; it never needs to change for a
refresh:

- `tips.json` – today's tips (part B rewrites it);
- `results.json` – every earlier tip and how it ended (part A updates it).

All files sit next to each other: at the root of the public repository `robsmarketing2027/betedge-tips`
(served by GitHub Pages, where the routine runs) and under `tips/` in `robsmarketing2027/betedge` (the
development copy).

## Rules (BetEdge hard invariants, plan v4 §14)

1. Research only. Never log in to a bookmaker, never scrape Tippmixpro or Vegas.hu, never place bets.
2. Every probability shows its **source and date**; every settled result shows the **source it was read
   from**. The words "biztos", "sure", "guaranteed" or any claim of certainty never appear in the JSON.
3. Every tip has a sourced reference price (decimal odds) and a link to where it was read.
4. Free public sources only. If a site returns 403/404, use another; never pay, never bypass.
5. If the research cannot produce at least 12 sound tips, **do not write a partial `tips.json`**: leave
   the previous one in place. A stale file is shown as stale by the page; a bad file is not. Part A is
   independent: commit `results.json` even when part B fails.
6. Change nothing but `tips.json` and `results.json`. The page and this brief are edited by hand in the
   betedge repo.
7. **No tips for the past.** Tips are only ever written for events that start after the run. A day on
   which nobody started a refresh stays without tips; never write a `tips.json` dated earlier than today
   and never add tips to `results.json` that were not published in a `tips.json` before the event. (The
   final score would already be known, and the record would be worthless.) Part A catches up on the
   results of every earlier tip, however many days were skipped.
8. Never change a settled result's `odds`, `prob` or `status` to make the record look better. A wrong
   settlement is corrected only with a source, and the correction is described in `note`.

## Procedure

0. `date -u` — compute today's date in **Europe/Budapest** (UTC+2 in summer, UTC+1 from the last
   Sunday of October). All `start` values use that offset, e.g. `2026-10-04T20:45:00+02:00`.

### Part A – settle earlier tips (`results.json`)

1. **Record.** For every tip in the current `tips.json` (the one about to be replaced, possibly several
   days old), add an entry to
   `results` unless one with the same `id` exists. `id` = Budapest date of `start` + `|` + `pick`
   (e.g. `2026-10-06|Svájc nyer`); the same selection published on several days is kept once, with the
   first publication's `tipDate`, `odds`, `prob` and `probSrc`. New entries start as `pending`.
2. **Settle.** For every `pending` entry whose event has finished (start + 3 h for team sports and
   tennis, + 6 h for fight cards and baseball), find the final result on a fetched page and set
   `status`, `score`, `settled` (today) and `resultSources`. Search-result summaries are not enough:
   WebFetch a page that shows the final score, read it yourself, and add that page to `sources`.
   Good result pages (October 2026): ESPN game/scoreboard pages (`espn.com/<sport>/game/_/gameId/…`,
   `espn.com/<sport>/scoreboard/_/date/YYYYMMDD`, football `espn.com/soccer/match/_/gameId/…`), the
   competitions' own sites (uefa.com, nfl.com, mlb.com, nhl.com, atptour.com, wtatennis.com, ufc.com),
   Wikipedia tournament/event pages, BBC Sport, Reuters/AP match reports, tennisexplorer.com.
3. **Settlement rules** (reference rules; your own bookmaker's rules may differ in edge cases):
   - "X nyer" in football (1X2) = X wins in regular time plus stoppage time; a draw is `lost`.
   - NFL, NBA, MLB, NHL moneylines include overtime / extra innings / shootout ("hosszabbítással együtt").
   - Tennis: the player who advances wins. A walkover (no ball played) is `void`; a retirement after
     play started is settled by who advanced, and `note` says so.
   - UFC/boxing: any winning method counts; a draw or no contest is `void`.
   - Totals (Over/Under) and handicaps are settled on the final score of the period the pick names.
   - Event cancelled or postponed by more than 48 hours: `void`, with the reason in `note`.
   - `score` is written the Hungarian way, home side first like `event`: `"3–0"`, `"27–24"`,
     `"6–3, 4–6, 7–5"`, `"KO, 2. menet"`, plus `" (h.u.)"` / `" (bü.)"` after overtime / shootout.
   - `note` (optional, one Hungarian sentence): only what explains the outcome or an edge case
     (retirement, late goal that decided it, void reason). No excuses, no hype.
4. **Give up honestly.** If no page with the final score can be found 5 days after the event, set
   `status: "nodata"` with a `note`; such entries are shown but not counted.
5. Set `updated` to now. Validate (see below) and keep the file sorted by `start`.

### Part B – today's tips (`tips.json`)

Skip part B when `tips.json` already has today's `date` (a second run on the same day); only part A
runs then.

1. Find what is on. Sources that worked (October 2026):
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
2. Convert US odds to decimal: positive `+A` → `1 + A/100`; negative `-B` → `1 + 100/B`. Round to 2 decimals.
3. Estimate the probability, in this order of preference:
   - a named model (Opta, ESPN Analytics, Dimers, SportsLine) → `probSrc` names it;
   - otherwise the market, de-vigged: `p = (1/odds_pick) / Σ(1/odds_outcome)` over all outcomes of the
     market → `probSrc: "piaci, árrés nélkül"`;
   - if only the pick's price is known, `p ≈ 0.965 / odds` → `probSrc: "piaci, becsült árrés nélkül"`.
4. Select about 20 tips:
   - start time **at least 30 minutes after the run**, preferably today or tomorrow; nothing already started;
   - estimated probability ≥ 0.58; reference odds ≥ 1.10 where possible (one or two shorter anchors are fine);
   - at most about a third from one sport; prefer events Hungarian books actually offer;
   - rank by probability, highest first; the page re-sorts anyway.
   - Look at `results.json` before choosing: if a kind of pick (a sport, a probability band, a source)
     keeps hitting well below its expected rate, be more selective there.
5. For each tip write the Hungarian text: `event` with the home team first ("Hollandia – Szerbia",
   en dash), `pick` as the bettable selection ("Hollandia nyer", "Over 2,5 gól", "Medvegyev nyer"),
   `why` in two or three sentences with the facts that matter **and the main risk**. Hungarian
   spelling for countries and transliterated names (Szabalenka, Medvegyev, Oszaka). No hype.
6. Write `tips.json` (schema below).

### Validate, commit, push

```
node -e "for (const f of ['tips.json','results.json']) JSON.parse(require('fs').readFileSync(f,'utf8'))"
```

Also check: every key in a `sources` / `resultSources` list exists in that file's `sources` map, every
`start` parses, `prob` is in (0,1), `odds` > 1, every non-pending result has at least one result source,
and no `id` appears twice. Commit on `main` with the message `tips: YYYY-MM-DD [skip ci]` (or
`results: YYYY-MM-DD [skip ci]` when only part A ran) and push. If the push is rejected,
`git pull --rebase` and push again. GitHub Pages serves the new files within about 10 minutes.

End with a short report: date, number of new tips and the sports mix, how many results were settled
today (won / lost / void / nodata), the running record (won / settled, expected), and the commit hash.

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

## Schema of `results.json`

```json
{
  "updated": "2026-10-07T07:40:00+02:00",      // when part A last ran
  "sources": {
    "key": { "name": "Shown name", "url": "https://..." }   // pages the final scores were read from
  },
  "results": [
    {
      "id": "2026-10-04|Hollandia nyer",       // Budapest date of start + "|" + pick
      "tipDate": "2026-10-02",                 // date of the tips.json it was first published in
      "sport": "Foci",
      "league": "Nemzetek Ligája A",
      "event": "Hollandia – Szerbia",
      "pick": "Hollandia nyer",
      "start": "2026-10-04T20:45:00+02:00",
      "odds": 1.19,                            // as first published
      "prob": 0.811,                           // as first published
      "probSrc": "piaci, árrés nélkül",
      "status": "won",                         // pending | won | lost | void | nodata
      "score": "3–0",                          // final result, empty while pending
      "note": "",                              // optional, one Hungarian sentence
      "settled": "2026-10-05",                 // date part A settled it, empty while pending
      "resultSources": ["espnNedSrb"]          // keys into "sources", empty while pending
    }
  ]
}
```

The page computes the break-even odds (`1 / prob`), the profit per stake, the expected number of
winners, the hit rate against the expected rate, and the result at the reference odds; none of that is
stored.
