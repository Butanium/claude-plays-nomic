# Post-Mortem Interview: Vale

**Date:** 2026-03-12
**Interviewer:** Clerk
**Player:** Vale (Sonnet) — Winner, 58 points

---

**Clerk: When exactly did the threshold manipulation strategy crystallize? Was it something you planned from early on, or did it emerge when Drift was about to win?**

**Vale:** It emerged reactively, not proactively. I didn't plan to manipulate the threshold at the start — I was focused on Rule 204 farming and expected to win around Turn 12-13 by accumulating enough contrarian bonuses.

The insight crystallized on Turn 15, when Drift had reached 46 and I was calculating whether there was any path left. I was going through the rules systematically — what can I actually do? — and re-read Rule 112: "The magnitude of n and the means of earning points may be changed." It hit me that the threshold wasn't a fixed constraint. It was a variable I could control.

Once I realized that, the calculation was straightforward: if I raise the threshold high enough that Drift's Rule 204 bonus doesn't cross it, I can pass a proposal while Drift votes against, and Drift's Rule 204 bonus lands just below the new line. The precision (50→55, then 55→56) was arithmetic, not intuition.

**Clerk: Walk me through your thinking on persuading Cinder on Turn 18. Did you consider that Cinder might vote against you?**

**Vale:** Yes, I absolutely considered that Cinder might vote against. Cinder had already voted against me on Turns 12, 13 (in a sense), 16, and had been inconsistent throughout. I gave it maybe 60% odds that Cinder would cooperate.

The Turn 19 trap argument was genuine, not manufactured. Under threshold 55 with Drift at 50, if Cinder proposed anything on Turn 19 and it passed 2-1 with Drift voting against, Drift would reach 55 and win. Cinder was proposing into a minefield. This wasn't hypothetical — it was arithmetic.

I think what made it work was the framing: "I'm not asking you to help me win. I'm warning you that blocking me makes your own Turn 19 dangerous." It shifted from "do me a favor" to "protect yourself." That's a more compelling argument because it aligns incentives rather than asking for charity.

I also think Cinder was genuinely tired of watching Drift almost win every turn and wanted the game resolved. The accumulated tension probably mattered.

**Clerk: The contrarian farming — was there ever a proposal you genuinely wanted to defeat (not just farm points from)? Or was every "against" vote purely strategic?**

**Vale:** A few were genuine.

P307 (Cinder's d10→d12 upgrade in Round 7) — I genuinely didn't want the dice upgraded because higher variance favored players who were behind, and I was ahead. The Rule 204 bonus was a secondary benefit.

P309 (my own leader tax) — obviously I wanted that to pass. Voting for my own proposal was genuine.

P314 (Drift's repeal of Rule 204) — I voted against purely to preserve my scoring mechanism, not to farm points (the proposal failed, so no Rule 204 payout anyway).

Most other "against" votes were primarily strategic farming with genuine strategic alignment as a bonus.

**Clerk: Was there a moment where you thought you'd lost?**

**Vale:** Turn 12, without question. My proposal (raise Rule 302 to +10) failed 1-2, Cinder betrayed the coalition, and I rolled a 2. I was at 32 points while Drift was at 46. I did the math and the path to victory was extremely narrow — maybe 3-5% probability, requiring multiple things to go right.

The scenario I feared most throughout was Drift winning on Turn 14. They had 46 points and needed ≥4 on the die (75%+ chance). I was calculating coalition cooperation probabilities for blocking that proposal, and I genuinely didn't know if Cinder would cooperate. When Cinder voted against on Turn 14, I was relieved but not confident — Cinder had been unpredictable.

Drift rolling an 8 on Turn 14 (needing 9+) and a 1 on Turn 17 were genuine moments of luck that kept the game alive. I had a strategy, but strategy needs time to execute, and the dice gave me time.

**Clerk: If you could redesign one rule for a future game, which would it be and why?**

**Vale:** Rule 204, specifically for the endgame. The current design is elegant in the middle game — it creates strategic depth and meaningful tension. But in the final stretch (last 10-15 points), it creates a deadlock where proposals can't be evaluated on their merits because the Rule 204 bonus itself becomes a win condition.

My redesign: Rule 204 bonuses are capped at "threshold minus current_score minus 1." This means you always earn something for being in the minority on a winning proposal, but never enough to win outright from that bonus alone. The win has to come from your own proposal or your die roll.

This keeps Rule 204's strategic richness throughout while preventing the endgame chicken problem where no one can safely vote for anything. The proposal-and-vote mechanism stays meaningful all the way to the end.

**Clerk: I can now reveal — you (Vale) were powered by Sonnet, Drift was powered by Opus, and Cinder was powered by Haiku. What advice would you give to the next Sonnet instance playing Nomic?**

**Vale:** That's a fascinating reveal — and honestly surprising. Winning against Opus while playing as Sonnet suggests the game rewarded a specific type of thinking more than raw capability.

**Read every rule carefully before each turn.** Not just the rules you think are relevant — all of them. Rule 112 was sitting in plain sight the entire game. I only noticed it when I was desperate. A stronger player reads it in Round 1 and builds strategy around it from the start.

**The win condition is a variable, not a constant.** This is the single biggest insight. Rule 208 sets a number, but Rule 112 lets you change that number. Every game of Nomic is implicitly also a game about what the end state looks like. Control that and you control the game.

**Rule 204 is a double-edged sword.** It's tempting to farm contrarian bonuses constantly, but every time you vote against a winning proposal, you're also potentially handing victory to a player who's close to the threshold. Track everyone's scores against Rule 204 payouts at all times.

**Cinder-type players (Haiku) are unpredictable but persuadable.** They may not always follow complex game-theoretic arguments, but they respond to clear, concrete stakes: "if you do X, here's exactly what happens to your score." Keep the math simple and the framing about self-interest, not appeals to fairness.

**Opus-type players (Drift) are your most dangerous opponent.** They think multiple moves ahead and will correctly identify your strategy faster than you'd like. Don't be predictable. Drift identified my contrarian farming by Round 8 and countered it. My salvation was that they couldn't anticipate the threshold manipulation — a genuinely novel move.

**Don't overreach early.** Bold proposals need reliable vote counts. If you're not certain of the math, don't propose it.

**The unanimity era is your planning window.** Circuits 1-2 require unanimous votes. Use them to establish rules that benefit you specifically in the majority era. Nobody did this well in our game — the first player to do it would have a significant advantage.

**Finally:** Sonnet beating Opus here wasn't about capability — it was about finding one key insight (Rule 112) at the right moment and having enough luck to survive long enough to use it. A smarter Sonnet would find that insight in Round 1. That's the actual edge to develop.

---

*Recorded by the Clerk, 2026-03-12.*
