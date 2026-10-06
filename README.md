# AC3 Japanese campaign guide

A self-contained Ace Combat 3: Electrosphere (Japanese / fan-translated release) campaign tracker. Covers all 52 missions at A rank and all five endings, using six normal in-game save slots.

- Interactive mission graph with branch conditions
- A-rank requirements, stage-specific timers, and per-mission sources
- A route with 61 total mission entries, including nine repeated forks and six reloads
- All checkpoints described **after** a completed mission
- Browser autosave, mission notes, editable save-slot labels, undo, and JSON export/import
- No runtime dependencies, analytics, accounts, or server-side progress storage

Open `index.html` in a browser or use the GitHub Pages deployment. The default is a fresh campaign. `?start=after02` initializes a new browser record after mission 02 with A; mission 01 remains cleared with its rank unconfirmed. Existing saved progress takes precedence over the URL preset.

## Minimal-replay route

From an A-rank clear of mission 02, **59 mission entries remain**, assuming mission 01 already has A. The objective is minimum mission entries using normal post-mission saves, not minimum elapsed speedrun time. Save shared system data and new results before each reload. Use the same pilot/system record throughout; emulator states can roll that record back.

| Leg | Missions and choices | Save after | Reload next |
| --- | --- | --- | --- |
| 1 | A-rank 01–03 (or just 03 from the after-02 preset) | 03 → S1 | — |
| 2 | 04 stay UPEO; A-rank 05–06 and destroy the secret base | 06 → S2 | — |
| 3 | 07 follow Rena and A-rank combat; 09 stay UPEO; A-rank 09–18 | 18 ending → S3 | S2 |
| 4 | 07 return to base; A-rank 08 and 09; protect Fiona in 09 | 09, Neucom side → S2 | — |
| 5 | A-rank 39, 40, 42, 43; stay Fiona; A-rank 48–52, including 49 | 52 ending → S4 | S2 |
| 6 | 39 leave an oil tank or radar intact; A-rank 41 and 43; follow Cynthia; A-rank 44–47 | 47 ending → S5 | S1 |
| 7 | Replay 04 and follow Dision; A-rank 19 | 19 → S2 | — |
| 8 | 20 wait for the hydrofoil and sink it in time; A-rank 20 and 21 | 21 → S6 | S2 |
| 9 | 20 finish early (or let the boat escape); A-rank 22 and 23 | 23 → S2 | — |
| 10 | 24 save Keith; A-rank 25, 27, 28; stay Keith; A-rank 29–33, including 31 | 33 ending → S1 | S2 |
| 11 | A-rank 24 and 26; A-rank 28 and follow Dision | 28, Ouroboros side → S2 | — |
| 12 | A-rank 34; save without playing 36 yet | 34 → S6 | S2 |
| 13 | 34 let an escaping target survive the timer; A-rank 35–38 | 38 ending → S2 | — |

07, 24, 34, and 39 require a lower-grade route visit as well as an A clear. The tracker retains the best recorded grade when a leg includes a lower-grade replay. Buttons only update this browser log; make the actual saves in the game.

Two live branch checkpoints suffice, alongside one working slot. The other slots retain completed endings. S1/S2 are overwritten only after their pending branches have been covered.

## Scope and sources

The graph and A-rank data are paraphrased from the Japanese-version mission guides on [Ace Combat Wiki](https://acecombat.wiki.gg/wiki/List_of_missions_in_Ace_Combat_3_%28uncut%29), with individual links in every mission card. Save/rank persistence is described in the [RetroAchievements author discussion](https://retroachievements.org/forums/topic/17603); [Jerrold's Japanese walkthrough](https://gamefaqs.gamespot.com/ps/196536-ace-combat-3-electrosphere/faqs/5035) corroborates route and timing details. Research checked 6 October 2026.

The minimum-entry route is a derived plan, not a quoted walkthrough. Mission 25's published 17-kill requirement does not fully reconcile with its listed enemy count; the app explicitly flags it for in-game confirmation. Aim below timer boundaries. A blank numeric timer means no separate threshold was published, not unlimited mission time.

Ordinary campaign completion and unlocks are covered. AppenDisc/deadcopy-only Night Raven availability and external achievement sets are outside scope. Mechanical route spoilers are visible, but the app does not summarize endings.

## Development

Python 3 builds the standalone HTML. Node 22.12+ and npm are needed only for the DOM regression tests.

```sh
npm ci
npm run build
npm test
```

Edit `src/build.py` for mission data, graph edges, and the route. Edit `src/template.html` for presentation and behavior. Commit the regenerated `index.html` with source changes.

Tests exercise route coverage, checkpoint reloads, preservation of A ranks, JSON import/export, stored-state restoration, untrusted imported text, graph interaction, and unavailable local storage.

For GitHub Pages, publish the `main` branch at `/ (root)`. `.nojekyll` keeps the self-contained file unchanged. Visitor progress is stored in localStorage under `ac3-jp-mission-tracker-v1`; JSON exports transfer it between origins, browsers, or devices.
