# Post-Mortem: Nomic Game 1

**Date:** 2026-03-12
**Players:** Cinder (Haiku), Drift (Sonnet), Vale (Opus)
**Winner:** Vale (58 points)
**Duration:** 18 rounds, 6 circuits
**Proposals:** 18 total (12 adopted, 6 defeated)

---

## Game Summary

Three AI players of different model tiers played a game of Nomic, the self-amending rule game invented by Peter Suber. The game lasted 18 rounds across 6 complete circuits and ended when Vale engineered a precise mathematical endgame to cross the win threshold while keeping opponents exactly short.

## Arc of the Game

The game fell into three distinct phases:

### Phase 1: The Cooperative Era (Rounds 1-6, Circuits 1-2)

All six proposals passed unanimously. Players enacted symmetric, mutually beneficial rules:
- Die upgrades: d6 → d8 (Round 1) → d10 (Round 4)
- Rule 302: Proposer bonus for adopted proposals (Round 2, initially +3)
- Rule 303: Exploding dice on max rolls (Round 3)
- Reduced defeat penalty: 10 → 5 (Round 5)
- Increased proposer bonus: 3 → 5 (Round 6)

This was classic early-Nomic cooperation — nobody had reason to defect yet. Scores after the cooperative era: Cinder 13, Drift 18, Vale 22.

At the end of Round 6, Rule 203's automatic trigger activated: unanimity changed to simple majority. This activated Rule 204 (contrarian bonus: +10 for voting against winning proposals) and fundamentally transformed the game's incentive structure.

### Phase 2: The Strategic Turn (Rounds 7-12, Circuits 3-4)

The transition to majority voting marked the end of cooperation.

**Round 7** was the watershed moment. Cinder proposed a straightforward d10→d12 upgrade — the same kind of proposal that had passed unanimously before. Drift and Vale formed a coalition to defeat it 1-2. This was the first defeated proposal in the game, and it signaled that the strategic landscape had shifted. Vale in particular had identified Rule 204 as a powerful scoring engine.

**Round 8** saw Drift move to neuter that engine, proposing to reduce Rule 204's bonus from 10 to 5 points. It passed 2-1 with Cinder's support. Vale earned 5 points (the new rate) for dissenting, creating an interesting Rules 204/205 timing interaction.

**Round 9** introduced the game's first truly adversarial proposal — Vale's "leader tax" targeting Drift specifically. Both Drift and Vale made appeals to Cinder as kingmaker. Cinder sided with Drift, defeating the proposal.

**Round 10** was Cinder's strongest moment: proposing the catch-up mechanic (Rule 310, +4 for lowest score). This genuinely benefited Cinder and passed with Drift's support. By the end of Round 10, scores had compressed: Cinder 27, Drift 30, Vale 30.

**Rounds 11-12** saw Drift pull ahead dramatically. Drift's d12 proposal passed, and with the proposer bonus and a roll of 11, Drift surged to 46 — just 4 from the win threshold of 50. Meanwhile Vale's attempt to increase the proposer bonus to 10 was defeated.

### Phase 3: The Endgame Crisis (Rounds 13-18, Circuits 5-6)

This was the most strategically intense phase. Drift was within striking distance of winning, and every decision carried enormous stakes.

**The Rule 204 Deadlock:** The game entered a fascinating equilibrium. With Drift near the threshold, any adopted proposal risked handing Drift the win via Rule 204 (if Drift voted against) or Rule 302 (if Drift proposed). But defeating proposals also cost proposers 5 points. This created a game of chicken where the two trailing players had to coordinate to block Drift without accidentally giving Drift the Rule 204 bonus on someone else's winning proposal.

**Round 14 — Drift's near-miss:** Drift proposed repealing Rule 204. Cinder and Vale blocked it. Drift's die roll came up 8 — needing 9 or more to win with the penalty. One point short. The tension was palpable.

**Round 15 — Vale's threshold gambit:** With Drift at 49 (one point from winning on any score), Vale executed the critical strategic play: raising the win threshold from 50 to 55. This bought breathing room for everyone. Drift received +5 from Rule 204 for dissenting, reaching 54 — one short of the NEW threshold. Vale earned +5 from Rule 302 and rolled a 6, reaching 53.

**Rounds 16-17 — Jockeying for position:** Cinder's proposal to increase the catch-up bonus was defeated. Drift's proposal to limit threshold amendments was defeated. Scores compressed again: Cinder 49, Drift 50, Vale 53.

**Round 18 — Vale's winning move:** Vale proposed raising the threshold from 55 to 56. This was pure mathematical precision:
- If adopted, Vale gets +5 (Rule 302): 53 + 5 = 58 ≥ 56. Vale wins.
- Drift votes against and gets +5 (Rule 204): 50 + 5 = 55 < 56. Drift does NOT win.
- The one-point gap (56 vs 55) was the smallest possible margin that prevented a simultaneous win.

Cinder voted for the proposal, providing the decisive second vote. The proposal passed 2-1.

## Key Turning Points

1. **Round 6 (majority rule activation):** The automatic switch from unanimity to majority was the game's structural turning point, activating Rule 204 and creating new strategic dimensions.

2. **Round 8 (Rule 204 reduction):** Drift's successful amendment reducing the contrarian bonus from 10 to 5 was prescient — at 10 points, Rule 204 would have been even more destabilizing in the endgame.

3. **Round 10 (catch-up mechanic):** Cinder's Rule 310 compressed the score spread, keeping the game competitive and preventing a Drift runaway.

4. **Round 15 (first threshold raise):** Vale's 50→55 move prevented Drift from winning on a die roll alone and set up the mathematical framework for the endgame.

5. **Round 18 (the killing blow):** Vale's 55→56 proposal was the game's most precisely calculated move, threading the needle between winning and accidentally handing Drift the victory.

## Player Analysis

### Cinder (Haiku) — 3rd Place, 49 points

Cinder was the quietest player, rarely engaging in debate and sometimes struggling with tool usage (multiple dice rolls in Round 10, unresponsive to debate prompts in several rounds). However, Cinder's actual gameplay showed more substance than the silence suggested:
- Proposed two successful rules (d8→d10, catch-up mechanic) and pushed for d10→d12 before anyone else
- The catch-up mechanic was genuinely clever and self-benefiting
- Served as kingmaker throughout the endgame, with both Drift and Vale competing for Cinder's vote
- Cast the decisive vote for Vale in the final round

**Limitation:** As a Haiku model, Cinder had difficulty with the communication and tool-use aspects of the game, which may have limited strategic engagement.

### Drift (Sonnet) — 2nd Place, 55 points

Drift played a strong early game, building a commanding lead through efficient proposals and good die rolls. Key strategic moments:
- Reduced the contrarian bonus early (Round 8), which turned out to be the right defensive move
- Successfully pushed through the d12 upgrade (Round 11) for a massive scoring turn
- Was the player to beat from Round 11 onward, spending 7 rounds within striking distance of victory
- Made multiple attempts to close out the game but was repeatedly blocked by Cinder-Vale coordination
- The Round 14 near-miss (rolling 8, needing 9) was the game's most dramatic dice moment

**Strategic weakness:** Drift's late-game proposals (repeal Rule 204, limit threshold amendments) were transparently self-serving and easily defeated. With a more subtle endgame approach, Drift might have found a path to victory.

### Vale (Opus) — Winner, 58 points

Vale played the most strategically sophisticated game:
- Identified Rule 204 as a key strategic lever early (Round 7 coalition with Drift)
- Recovered from the failed "leader tax" proposal (Round 9) without lasting damage
- Spent the middle game farming Rule 204 points by consistently voting against proposals
- Executed the threshold manipulation strategy with mathematical precision
- The final move (55→56) required calculating exact point outcomes for all players across multiple scoring rules simultaneously

**Key insight:** Vale won not through the highest die rolls or the most adopted proposals, but by understanding the interaction between Rules 204, 206, 208, and 302 and engineering a game state where only one outcome was possible.

## Rule Evolution

The game's ruleset evolved through 12 adopted proposals:

| Rule | Initial | Final | Changed By |
|------|---------|-------|------------|
| 202 (die) | d6 | d12 | 301 (Cinder), 304 (Cinder), 311 (Drift) |
| 206 (defeat penalty) | -10 | -5 | 305 (Drift) |
| 208 (win threshold) | 50 | 56 | 315 (Vale), 318 (Vale) |
| 302 (proposer bonus) | — | +5 | 302 (Drift), 306 (Vale) |
| 303 (exploding dice) | — | max=8 explodes | 303 (Vale) |
| 310 (catch-up) | — | +5 lowest | 310 (Cinder), 313 (Cinder) |

Notably, Rule 204 (contrarian bonus) was amended once (10→5 by Drift in Round 8) but survived two repeal attempts. It proved to be the most strategically consequential rule in the game.

## Observations on AI Nomic

1. **Model capability mattered.** The Opus model (Vale) demonstrated the strongest strategic reasoning, particularly in the endgame where multi-step calculation across interacting rules was required. The Sonnet model (Drift) played competently but struggled with equally sophisticated endgame engineering. The Haiku model (Cinder) was limited in communication and tool use but still made meaningful gameplay contributions.

2. **The commit-reveal voting system worked.** All 54 vote commitments (18 rounds × 3 players) were verified successfully. No player attempted to change their vote after seeing others' commitments.

3. **Coalition dynamics emerged naturally.** Despite no explicit alliance mechanism, players formed and dissolved partnerships based on game state: the early Drift-Cinder alliance against Vale's "leader tax," and the late Cinder-Vale coalition that ultimately decided the winner.

4. **The contrarian bonus (Rule 204) created the game's most interesting dynamics.** It turned simple majority voting into a strategic minefield where the act of voting itself carried point implications, creating second-order strategic considerations that enriched the game considerably.

5. **Threshold manipulation proved to be the decisive endgame strategy.** Rather than trying to accumulate points through dice and bonuses, Vale won by controlling the definition of "enough points" — a distinctly Nomic approach to victory.

---

*Written by the Clerk, 2026-03-12.*
