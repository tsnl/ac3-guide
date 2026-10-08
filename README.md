# AC3 Japanese campaign guide

A linear Ace Combat 3: Electrosphere (Japanese / fan-translated release) campaign checklist. Covers all 52 missions and all five endings, using six normal in-game save slots. The checklist focuses on timing and route objectives; the separate rank reference covers the extra requirements for all A ranks.

- Top-level Instructions explain mission order, A-rank exceptions, route choices, post-mission saves, checkboxes, and load steps
- One checkbox for each of 61 mission attempts, plus six separate load-save boxes labeled with the next mission's name, matching the game's load menu
- The next unfinished action is highlighted; later actions stay muted and clickable
- Checking a later action asks for confirmation before checking everything before it; unchecking clears that action and everything after it, including load actions
- Each mission shows its name, a **Time / Requirements** milestone table, and where to save **after** completion; a bold highlighted Decision appears only at story forks and uses a character name, except Scylla and Charybdis: **SHOOT FIONA** / **SHOOT R101U**
- Guidebook map thumbnails for all 52 missions; exact briefing-menu replacements are pending source images. Artwork, scan, and research attribution is in a separate Credits section
- Five gold ending boxes with stars
- Data Swallow-inspired ivory, black, and amber menu theme with an animated network-tunnel background that follows the device’s reduced-motion setting
- A-rank requirements and source links on a separate reference page
- Browser autosave and JSON backups through Save / Load
- Four circular controls—Save, Load, Feedback, Credits—in the original menu's low–high–low–high arrangement, with segmented concentric rings. Feedback opens a new GitHub issue; Credits links to the source attributions
- No runtime dependencies, analytics, accounts, or server-side progress storage

Open [the published checklist](https://tsnl.github.io/ac3-guide/) or open `index.html` in a browser with its `assets` directory alongside it. The checklist starts blank. Tick actions in order as you finish them and make the listed saves. Mission names link to their detailed A-rank requirements. Saved browser progress is restored on subsequent visits.

## Minimal-replay route

From an A-rank clear of mission 02, **59 mission entries remain**, assuming mission 01 already has A. The objective is minimum mission entries using normal post-mission saves, not minimum elapsed speedrun time. Save shared system data and new results before each reload. Use the same pilot/system record throughout; emulator states can roll that record back.

| Leg | Missions and choices | Save after every mission in this leg | Reload next |
| --- | --- | --- | --- |
| 1 | A-rank 01–03 | Fresh S1 after 01, then overwrite S1 | — |
| 2 | 04 stay UPEO; A-rank 05–06 and destroy the secret base | Fresh S2 after 04, then overwrite S2 | — |
| 3 | 07 follow Rena and A-rank combat; 09 stay UPEO; A-rank 09–18 | Fresh S3 after 07, then overwrite S3; keep ending | S2 · No Clearance |
| 4 | 07 return to base; A-rank 08; replay 09 and protect Fiona | Overwrite S2 | — |
| 5 | A-rank 39, 40, 42, 43; stay Fiona; A-rank 48–52, including 49 | Fresh S4 after 39, then overwrite S4; keep ending | S2 · Power for Life |
| 6 | 39 leave an oil tank or radar intact; A-rank 41; replay 43 and follow Cynthia; A-rank 44–47 | Overwrite S2; keep ending | S1 · Paper Tiger |
| 7 | Replay 04 and follow Dision; A-rank 19 | Overwrite S1 | — |
| 8 | 20 wait for the hydrofoil and sink it in time; A-rank 20 and 21 | Fresh S5 after 20, then overwrite S5 | S1 · Megafloat |
| 9 | 20 finish early (or let the boat escape); A-rank 22 and 23 | Overwrite S1 | — |
| 10 | 24 save Keith; A-rank 25, 27, 28; stay Keith; A-rank 29–33, including 31 | Overwrite S5; keep ending | S1 · Stratosphere |
| 11 | A-rank 24 and 26; Replay 28 and follow Dision | Overwrite S1 | — |
| 12 | A-rank 34; save without playing 36 yet | Fresh S6 after 34 | S1 · The Orientation |
| 13 | 34 let an escaping target survive the timer; A-rank 35–38 | Overwrite S1; keep ending | — |

Repeat visits carry a compact label: **Repeat · A not needed** when an earlier visit already called for A, or **Repeat · Get A this time** for Stratosphere’s second visit, because its first visit deliberately takes the D route. These labels assume the earlier A was actually earned. Visits that do not require A omit the time/requirements table; a short route note retains any essential branch condition, and story decisions and saves remain visible.

07, 24, 34, and 39 require a lower-grade route visit as well as an A clear. Each replay has its own checkbox and visit-specific instructions; completing a lower-grade replay does not replace the earlier A-clear checkbox. Only narrative choices use the Decision highlight. Timed route requirements and ordinary objectives such as following the spy plane appear in the milestone table. Each row gives a timing goal and a short essential objective. Optional-kill totals and score requirements are kept on the linked A-rank reference page; meeting a time alone does not guarantee A. Deliberate lower-grade visits retain their distinct route requirements. Checkboxes only update this browser log; make the actual saves and loads in the game.

Every mission shows six numbered, rounded save-slot icons. The destination is highlighted **green with +** for a fresh save, or **amber with ↻** for an overwrite. Unused slots are grey; occupied slots are filled, with a star on preserved endings. Hover text and accessible labels identify the mission in each file. Each diagram shows the planned slot contents after that step, including the highlighted save destination. Saves start **1, 1, 1, 2, 2, 2, 3…**: advance to another slot to preserve a pending branch checkpoint, and reuse the previous slot on its last remaining branch. There is no dedicated temporary slot. The six slots are first used in numerical order, and all five ending saves remain intact at the end. The plan assumes these slots are available at the start.

## Scope and sources

The graph and A-rank data are paraphrased from the Japanese-version mission guides on [Ace Combat Wiki](https://acecombat.wiki.gg/wiki/List_of_missions_in_Ace_Combat_3_%28uncut%29), with individual links in `ranks.html`. Save/rank persistence is described in the [RetroAchievements author discussion](https://retroachievements.org/forums/topic/17603); [Jerrold's Japanese walkthrough](https://gamefaqs.gamespot.com/ps/196536-ace-combat-3-electrosphere/faqs/5035) corroborates route and timing details. Research checked 6 October 2026.

The minimum-entry route is a derived all-A plan, not a quoted walkthrough. The checklist itself tracks actions, not achieved ranks; use the full reference if pursuing every A rank. Mission 25's published 17-kill requirement does not fully reconcile with its listed enemy count; the rank reference flags it for in-game confirmation. Reaching for Stars is also checked against Mission & World View, p. 86: the 13 required kills give C; A needs at least five optional kills too. Aim below timer boundaries. A blank numeric timer means no separate threshold was published, not unlimited mission time.

Ordinary campaign completion and unlocks are covered. AppenDisc/deadcopy-only Night Raven availability and external achievement sets are outside scope. Mechanical route spoilers are visible, but the app does not summarize endings.

## Development

Python 3 builds the checklist and the separate rank-reference HTML. Both use local styles and no external runtime scripts. Node 22.12+ and npm are needed only for the DOM regression tests.

```sh
npm ci
npm run build
npm test
```

Edit `src/build.py` for mission data and the ordered action list, and `src/milestones.py` for time/requirements pairs and visit-specific overrides. Edit `src/template.html` for checklist presentation and behavior, `src/reference.html` for the rank-reference page, and `src/theme.css` for the shared menu theme and CSS tunnel animation. `src/tunnel.py` generates static wall markup. Styles and background markup are inlined by the build. Mission maps are local assets under `assets/maps`; their source pages and crop coordinates are recorded in that directory. Commit regenerated `index.html` and `ranks.html` with source changes.

The background follows the network-as-tubes concept described by designer Minoru Sashida in [Namco's 1999 NOURS interview](https://www.bandainamcoent.co.jp/corporate/bnours/nours/vol24/pdf/24_32-34.pdf). Its oval cross-section, pale facets, olive center, and circular menu controls were refined against a supplied recording of the game UI; the recording itself is not included. The tunnel uses 24 static HTML wall panels, CSS perspective, repeating gradients, and a linear `translateZ()` animation. Four repeating bays advance 50 CSS pixels every two-thirds of a second, preserving the previous 7.5-world-unit/second flight speed. Rendering and motion require no canvas, JavaScript drawing loop, or external assets. The scene is pinned to the viewport with a stationary vanishing point and stable large viewport height, independent of scrolling and mobile toolbar changes. The black header extends above the document for top overscroll. The CSS `prefers-reduced-motion` media query is the only motion control: the tunnel animates by default and becomes still when the device requests reduced motion. Changes to that setting apply automatically. There is no background JavaScript, in-app motion switch, or saved motion preference; any preference stored by older versions is ignored.

Tests exercise mission-by-mission route coverage, valid checkpoint reloads, contiguous progress when moving forward or backward, JSON import/export, migration from the original tracker, stored-state restoration, untrusted imported text, and unavailable local storage.

For GitHub Pages, publish the `main` branch at `/ (root)`. `.nojekyll` serves the generated HTML and map assets directly. Visitor progress is stored in localStorage under `ac3-jp-mission-tracker-v1`; JSON exports transfer it between origins, browsers, or devices.

## Progress format

Version 2 stores completed action IDs, so two visits to one mission remain distinct. Checking any action marks the route complete through that action; skipping unfinished actions requires confirmation, and cancelling leaves progress unchanged. Checking the next action needs no confirmation. Unchecking moves progress back to immediately before that action. These rules include load actions and repeated mission visits. Existing records and JSON backups with gaps resume at the first unchecked action, clearing later checks instead of assuming missing actions were completed. Version 1 records first map completed route legs and first A-clear visits to action IDs, then apply the same gap repair. Old notes, ranks, branch flags, and slot labels remain in the exported `legacy` object.

See the public [Credits section](https://tsnl.github.io/ac3-guide/ranks.html#credits) for research and design sources, and [map image credits](assets/maps/SOURCES.md) for the original Namco guidebook, archive provenance, and a per-mission crop index. Original game and guidebook artwork remains © NAMCO LTD.
