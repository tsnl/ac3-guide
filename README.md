# AC3 Japanese campaign guide

A linear Ace Combat 3: Electrosphere (Japanese / fan-translated release) campaign checklist. Covers all 52 missions at A rank and all five endings, using six normal in-game save slots.

- One checkbox for each of 61 mission attempts, plus six separate load-save boxes
- Only the next unfinished action is enabled; later unchecked actions are greyed out
- Each mission shows its name, target time, and where to save **after** completion; a bold highlighted Decision appears only at story forks
- Five gold ending boxes with stars
- Data Swallow-inspired ivory, black, and amber menu theme with an animated network-tunnel background, a pause control, and reduced-motion support
- A-rank requirements and source links on a separate reference page
- Browser autosave, undo, and JSON backups through Save / Load
- Four circular controls in the original menu's low–high–low–high arrangement, with segmented concentric rings
- No runtime dependencies, analytics, accounts, or server-side progress storage

Open [the published checklist](https://tsnl.github.io/ac3-guide/) or open `index.html` in a browser. The checklist starts blank. Tick actions in order as you finish them and make the listed saves. Mission names link to their detailed A-rank requirements. Saved browser progress is restored on subsequent visits.

## Minimal-replay route

From an A-rank clear of mission 02, **59 mission entries remain**, assuming mission 01 already has A. The objective is minimum mission entries using normal post-mission saves, not minimum elapsed speedrun time. Save shared system data and new results before each reload. Use the same pilot/system record throughout; emulator states can roll that record back.

| Leg | Missions and choices | Save after every mission in this leg | Reload next |
| --- | --- | --- | --- |
| 1 | A-rank 01–03 | Fresh S1 after 01, then overwrite S1 | — |
| 2 | 04 stay UPEO; A-rank 05–06 and destroy the secret base | Fresh S2 after 04, then overwrite S2 | — |
| 3 | 07 follow Rena and A-rank combat; 09 stay UPEO; A-rank 09–18 | Fresh S3 after 07, then overwrite S3; keep ending | S2 after 06 |
| 4 | 07 return to base; A-rank 08 and 09; protect Fiona in 09 | Overwrite S2 | — |
| 5 | A-rank 39, 40, 42, 43; stay Fiona; A-rank 48–52, including 49 | Fresh S4 after 39, then overwrite S4; keep ending | S2 after 09 |
| 6 | 39 leave an oil tank or radar intact; A-rank 41 and 43; follow Cynthia; A-rank 44–47 | Overwrite S2; keep ending | S1 after 03 |
| 7 | Replay 04 and follow Dision; A-rank 19 | Overwrite S1 | — |
| 8 | 20 wait for the hydrofoil and sink it in time; A-rank 20 and 21 | Fresh S5 after 20, then overwrite S5 | S1 after 19 |
| 9 | 20 finish early (or let the boat escape); A-rank 22 and 23 | Overwrite S1 | — |
| 10 | 24 save Keith; A-rank 25, 27, 28; stay Keith; A-rank 29–33, including 31 | Overwrite S5; keep ending | S1 after 23 |
| 11 | A-rank 24 and 26; A-rank 28 and follow Dision | Overwrite S1 | — |
| 12 | A-rank 34; save without playing 36 yet | Fresh S6 after 34 | S1 after 28 |
| 13 | 34 let an escaping target survive the timer; A-rank 35–38 | Overwrite S1; keep ending | — |

07, 24, 34, and 39 require a lower-grade route visit as well as an A clear. Each replay has its own checkbox and visit-specific instructions; completing a lower-grade replay does not replace the earlier A-clear checkbox. Only narrative choices use the Decision highlight. Timed route requirements stay beside the target time, and ordinary objectives such as following the spy plane remain in the full mission guidance. Checkboxes only update this browser log; make the actual saves and loads in the game.

Every mission names a save destination and explicitly says **Fresh save → Slot N** on the first use of that slot, or **Overwrite Slot N** on later uses. Saves start **1, 1, 1, 2, 2, 2, 3…**: advance to another slot to preserve a pending branch checkpoint, and reuse the previous slot on its last remaining branch. There is no dedicated temporary slot. The six slots are first used in numerical order, and all five ending saves remain intact at the end. The plan assumes these slots are available at the start.

## Scope and sources

The graph and A-rank data are paraphrased from the Japanese-version mission guides on [Ace Combat Wiki](https://acecombat.wiki.gg/wiki/List_of_missions_in_Ace_Combat_3_%28uncut%29), with individual links in `ranks.html`. Save/rank persistence is described in the [RetroAchievements author discussion](https://retroachievements.org/forums/topic/17603); [Jerrold's Japanese walkthrough](https://gamefaqs.gamespot.com/ps/196536-ace-combat-3-electrosphere/faqs/5035) corroborates route and timing details. Research checked 6 October 2026.

The minimum-entry route is a derived plan, not a quoted walkthrough. Mission 25's published 17-kill requirement does not fully reconcile with its listed enemy count; the app explicitly flags it for in-game confirmation. Aim below timer boundaries. A blank numeric timer means no separate threshold was published, not unlimited mission time.

Ordinary campaign completion and unlocks are covered. AppenDisc/deadcopy-only Night Raven availability and external achievement sets are outside scope. Mechanical route spoilers are visible, but the app does not summarize endings.

## Development

Python 3 builds the checklist and the separate rank-reference HTML. Both use local styles and no external runtime scripts. Node 22.12+ and npm are needed only for the DOM regression tests.

```sh
npm ci
npm run build
npm test
```

Edit `src/build.py` for mission data and the ordered action list. Edit `src/template.html` for checklist presentation and behavior, `src/reference.html` for the rank-reference page, `src/theme.css` for the shared menu theme, and `src/background.js` for the procedural animation. Styles and background code are inlined by the build so each output page remains self-contained. Commit regenerated `index.html` and `ranks.html` with source changes.

The background follows the network-as-tubes concept described by designer Minoru Sashida in [Namco's 1999 NOURS interview](https://www.bandainamcoent.co.jp/corporate/bnours/nours/vol24/pdf/24_32-34.pdf). Its oval cross-section, pale facets, olive center, and circular menu controls were refined against a supplied recording of the game UI; the recording itself is not included. Fixed tunnel rings advance toward the viewer at a constant speed measured in world units per second, with a stationary vanishing point. Animation time is independent of scrolling and render frequency. The canvas is pinned to the viewport and uses a stable large viewport height so mobile toolbar changes during scroll do not resize the scene. The black header extends above the document for top overscroll. The tunnel is drawn locally, capped at 30 fps, pauses while the page is hidden, and defaults to still imagery when reduced motion is requested. The pause preference is stored separately from checklist progress.

Tests exercise mission-by-mission route coverage, valid checkpoint reloads, next-action locking, JSON import/export, migration from the original tracker, stored-state restoration, untrusted imported text, and unavailable local storage.

For GitHub Pages, publish the `main` branch at `/ (root)`. `.nojekyll` keeps the self-contained file unchanged. Visitor progress is stored in localStorage under `ac3-jp-mission-tracker-v1`; JSON exports transfer it between origins, browsers, or devices.

## Progress format

Version 2 stores completed action IDs, so two visits to one mission remain distinct. Existing version 1 browser records and JSON backups migrate automatically: completed route legs map to their actions, and a best A rank marks only the first A-clear visit. Old notes, ranks, branch flags, and slot labels remain in the exported `legacy` object. Checked actions can be unchecked or undone; only the earliest unchecked action can be checked next.

The tiles use mission numbers as icons. Mission screenshots were not available from a reliable retrievable source during this update.
