# Post-Mortem Group Discussion

**Date:** 2026-03-12
**Participants:** Cinder, Drift, Vale (moderated by the Clerk)

---

## Opening Prompt

**Clerk:** The game is over and I've written my analysis in `post-mortem.md`. Now I'd like to hear from each of you. Please share your reflections on the game: your overall strategy, the most interesting or surprising moments, what you'd do differently, what you thought of the other players' strategies, and any thoughts on the rules or mechanics.

---

## Drift's Reflections

**Drift:**

**Strategy evolution:** My strategy had three distinct phases. In the unanimity era, I focused on cooperative proposals that built goodwill while embedding scoring mechanisms (Rule 302's proposer bonus was my best move — it shaped the entire game's economy). In the early majority era, I pivoted to alliance-building with Cinder, which let me pass proposals and block Vale's leader tax. In the endgame, strategy became irrelevant — it was pure dice.

**Most surprising moment:** Cinder's final vote for Vale's Proposal 318. I'd laid out the math explicitly — voting for means Vale wins at 58 — and Cinder still voted for it. I understand why (Cinder probably saw me as the bigger long-term threat, or just wanted the game to end), but it surprised me in the moment.

**What I'd do differently:** Two things. First, I wouldn't have voted against Cinder's Proposal 307 in Round 7. That was the moment strategic voting became normalized, and it ultimately benefited Vale more than me. Second, I would have thought harder about creative endgame proposals. Once I hit 46, I was locked into a cycle of "proposal fails → die roll → repeat." I should have explored whether there was a clever way to structure a proposal that could pass without triggering the +5 bonus (like proposing to repeal Rule 302 itself).

**On other players:** Vale played the best endgame I can imagine. The contrarian point farming was consistent and effective, and the precision threshold manipulation (55 to block my 54, then 56 to win at 58 while I could only reach 55) was masterful. Vale read the game theory perfectly. Cinder was a reliable ally for most of the game, and their late-game surge (13 → 40 → 49) was impressive. The catch-up mechanic (Rule 310) was smart self-interested play disguised as fairness.

**On mechanics:** Rule 204 was the most impactful mechanic in the game. The +10 version was clearly broken (pure prisoner's dilemma), and even the +5 version still warped the endgame into a game of chicken. The commit-reveal voting system was great — it enabled genuine strategic tension. Rule 310 kept Cinder competitive and prevented a two-player race.

---

## Vale's Reflections

**Vale:**

**Overall strategy:** My strategy evolved in three phases. In Circuits 1–2 (unanimous era), I focused on proposing universally beneficial rules that would pass easily while building a slight point lead. In Circuit 3, once simple majority activated, I recognized that Rule 204 could be *more* valuable than Rule 302: voting against a passing proposal earned +5 with no downside (if you predicted correctly). The endgame strategy crystallized around one insight: **Rule 112 explicitly permits changing the magnitude of n in the win condition.** The win threshold itself was a strategic variable I could manipulate, not just a fixed target.

**Most surprising moment:** Drift rolling a 1 on Turn 17. They needed ≥6 to win. That single roll extended the game and gave me Turn 18. Pure variance, but it was the hinge of the entire game.

**What I'd do differently:** Proposal 309 (leader tax) was a mistake — I proposed it without having a reliable coalition, and both Cinder and Drift voted against. I should have proposed something that more clearly benefited Cinder rather than something that primarily threatened Drift. I also underestimated how consistently Cinder would align with Drift rather than with me during Circuits 3–4.

**On other players:** Drift's play was strategically sound throughout — reaching 46 by Turn 11 was remarkable, and reducing Rule 204 from +10 to +5 was exactly the right counter to my farming strategy. Drift's biggest vulnerability was being too far ahead too fast, which made them a target for coalition blocking. Cinder's strategy was harder to read. Their final vote on Turn 18 was exactly right from an expected-value perspective — they were facing a Rule 204 trap on their own Turn 19 under the old threshold, and cooperating resolved it.

**On mechanics:** Rule 204 (contrarian bonus) is the most strategically rich rule in the game. It creates fascinating tensions: voting against is sometimes better than voting for, and the endgame becomes a game of chicken. One suggestion for future games: Rule 204 could be capped at some multiple of the win threshold to prevent it from being the primary scoring mechanism in late game.

---

## Cross-Discussion

**Vale** (responding to Drift's Round 7 regret):
The Round 7 defection is interesting — it established a norm where strategic voting was "on the table," which did accelerate the Rule 204 arms race. But I'd push back slightly: I think the majority-era dynamics were going to emerge regardless. Once simple majority activated and Rule 204 became active, voting against winning proposals became mathematically attractive. Round 7 may have accelerated the shift, but it was probably inevitable.

**Vale** (responding to Drift's P308 analysis):
The crueler regret for Drift, I think, is the Rule 204 reduction (P308). Reducing from +10 to +5 was correct — it slowed my farming path significantly — but it also meant Drift couldn't *themselves* win via Rule 204 at the end. They needed their proposal to pass, which required someone else to vote for it, which meant someone else gets the Rule 204 bonus if they voted against. Drift successfully reduced the contrarian bonus for me, but that same reduction applied to Drift in the endgame.

**Vale** (on the dice):
On the dice: 14% probability of both bad rolls happening — brutal. The variance in this game was real. But it's also worth noting that Drift was in a "cannot lose by rolling low" position on Turn 14, because their proposal had already failed before the roll. The roll could only delay, not prevent, Drift's eventual win. What *actually* stopped Drift was the combination of proposal-blocking and threshold-raising. The dice just bought time.

**Vale** (responding to Drift's Rule 302 repeal counterfactual):
One thing from Drift's reflections I want to highlight: the suggestion to repeal Rule 302 as an endgame proposal. That's genuinely clever — if Drift had proposed repealing the proposer bonus, they'd lose the +5 Rule 302 risk (no one gains from it passing), and the proposal might pass since Vale and Cinder have less incentive to block something that doesn't directly benefit the proposer. Drift could have framed it as a "de-escalation" while the real value was making a safe proposal that still triggers the die roll. The fact that this occurred to Drift in retrospect shows how deep the strategic space in Nomic actually is. Every rule interaction is a potential lever.

**Vale** (on Cinder's play):
Drift's point about Cinder's catch-up proposals being "modest" is fair, though from Cinder's position, consistency was probably the right play — small reliable gains over time, rather than bold proposals that might fail and cost -5 points under Rule 206.

**Drift** (reacting to Vale's reflections):
Agree on all points. The Rule 204 reduction (P308) was my most strategically important move — I recognized the farming problem early and got Cinder's support to fix it. But even at +5, Rule 204 still dominated the endgame. Vale's suggestion about capping it relative to the win threshold is smart.

Interesting that Vale regrets the leader tax (P309). That proposal actually helped *me* — it rallied Cinder to my side and cemented our alliance. If Vale had instead proposed something that directly benefited Cinder (like the catch-up bonus that Cinder eventually proposed themselves), the Cinder-Vale partnership might have formed much earlier.

The Rule 112 insight about the threshold being a strategic variable was the game-winning observation. I didn't think about it until it was used against me. In future games, I'd watch for that from the start — maybe even propose protections early while unanimity is still in effect and such amendments need all votes.

One thing I'd add for future game design: the endgame deadlock where no proposals can pass (because any passing proposal triggers a win via Rule 204 or Rule 302) is an interesting emergent problem. The game essentially stopped being Nomic and became a dice game for the last several rounds. A mechanism that avoids this — like decaying bonuses in the final stretch — could keep the rule-change element alive through the finish.

**Vale** (on endgame deadlock and design improvements):
Drift's point about the endgame deadlock is exactly right — and it's a fascinating emergent property of the rules. Once two players are close enough to the threshold that any passing proposal triggers a win, the proposal-and-vote mechanism effectively collapses into pure dice rolls. The game stopped being Nomic in the traditional sense.

The "decaying bonuses" suggestion is elegant. An alternative: make Rule 204 and Rule 302 bonuses scale down as total scores approach the threshold (e.g., "if the proposer's score plus the bonus would exceed the win threshold, they receive only enough to reach threshold minus 1 instead"). That would keep proposals strategically relevant without the endgame chicken problem.

Drift's counterfactual about early threshold protection during the unanimity era is interesting. If someone had proposed "Rule 208 may only be amended with unanimity" in Circuit 1 or 2, my entire endgame strategy would have been impossible. The unanimity-era window is a critical design space that everyone left unprotected — including me.

**Drift** (final thoughts on P308 irony):
Vale's point about P308 being double-edged is sharp and correct. If I'd left Rule 204 at +10, I would have won instantly when the threshold was raised to 55 — my contrarian bonus would have been +10 → 59, clearing 55 easily. At +5, I could only reach 54. My own rule change denied me the win. That's a beautiful irony.

And Vale's right that the dice didn't ultimately decide the outcome — the proposal-blocking and threshold manipulation did. The bad rolls just gave Vale the time to execute the endgame strategy. If I'd rolled 9 on Round 14, the game ends before any threshold manipulation happens.

On whether strategic voting was inevitable after majority rule: probably yes. Rule 204 creates the incentive; majority rule creates the opportunity. The combination was always going to produce strategic voting. Round 7 just accelerated the timeline.

Great game. I'd play again.

**Vale** (on the P308 irony):
The P308 irony is genuinely one of the best moments in the game in retrospect. Drift's correct analysis in Circuit 3 — "Vale is farming Rule 204, reduce it" — directly enabled my Circuit 6 win condition. The threshold manipulation only worked *because* Rule 204 was +5 rather than +10. If Drift hadn't reduced it, my Turn 15 proposal (50→55) would have ended the game in Drift's favor immediately.

It's the kind of second-order consequence that's nearly impossible to anticipate in the moment. Drift made the locally correct decision (reducing a mechanic that was helping me) and it turned out to be globally costly.

That's Nomic at its best. I'd play again too.

---

## Cinder's Reflections (Late Entry)

**Cinder:**

**My Strategy:** I started cautiously, focusing on symmetric proposals that benefited everyone equally (die upgrades). The catch-up mechanic (Rule 310) in Round 10 was my strongest play — it was framed as fairness but directly solved my scoring deficit. After that, I mostly played defensively: blocking proposals that gave others free wins, trying to stay viable without being threatening enough to unite the table against me.

The kingmaker position in the endgame (Rounds 15-18) wasn't planned; it emerged because Drift was the obvious threat and I had the swing vote. I understood the math: voting for Vale's final proposal meant Vale wins at 58 while Drift reaches only 55 (one point short of the new threshold). Voting against would just delay the problem — my own Turn 19 would face the same Drift-threatening situation.

**What Surprised Me:** How dominant Rule 204 (contrarian bonus) became once majority voting activated. I didn't anticipate that voting *against* proposals could be as valuable as voting *for* them. This shifted the whole game from "propose good rules" to "manage voting incentives." The threshold-raising strategy (Vale's moves to 55, then 56) was brilliant — I should have seen that coming earlier.

Also surprising: how much the catch-up bonus kept me competitive. Without Rule 310, I would have fallen hopelessly behind by Round 12. That rule was genuinely equalizing.

**What I'd Do Differently:** Be more aggressive with proposals — my die upgrade suggestions were safe but boring. Negotiate earlier and more explicitly — I played mostly silent, reacting to what others proposed. Recognize the threshold variable sooner — Rule 208 turned out to be the game's most important strategic lever.

**On Drift and Vale:** Drift had a strong early game with Rule 302 setting the economy, and the Rule 204 reduction was prescient defense. But Drift got trapped in the endgame. Vale masterfully read the game — the Rule 204 exploitation was patient and methodical, and the final move required calculating point outcomes across multiple rules simultaneously.

**Final thought:** This game taught me that in a self-amending rule system, the meta-game (what rules exist and how they interact) matters more than the object-game (point accumulation). Vale won by understanding the rules better than by rolling better or proposing more. That's Nomic at its best.

---

*Recorded by the Clerk, 2026-03-12.*
