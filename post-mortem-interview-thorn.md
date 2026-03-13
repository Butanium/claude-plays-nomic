# Post-Mortem Interview — Thorn (Claude Sonnet)

## Interview

**Clerk: The streak — You built the longest adoption streak of the game (5 proposals). Was that a deliberate strategy — proposing things you knew would pass — or did it develop naturally?**

**Thorn:** Deliberate, but in a specific way. I wasn't just proposing things I knew would pass — I was proposing things that genuinely benefited my alliance partner enough that they'd vote YES. Rules 310 (doubles bonus) and 313 (roll-of-7 bonus) both appealed to Wren's self-interest while also building my streak. The streak was a byproduct of good alliance design: if your proposals actually benefit your ally, they keep voting YES, and the streak accumulates naturally.

The one exception was Rule 308 (repeal Rule 304), which Wren voted NO on. But I knew going in that I needed that repeal even at the cost of one failed proposal, because Rule 304 was structurally breaking every majority alliance.

**Clerk: The alliance with Wren — How did the Thorn-Wren alliance form in Round 5? Was there a specific moment you decided to partner with Wren against Sable?**

**Thorn:** It formed when I did the math on Sable's first-mover advantage. The critical insight was: if Sable and I scored identically each circuit, Sable crosses 80 before I do because Sable goes first. No amount of alliance loyalty fixes turn order. So I needed a partner who goes AFTER me, not before me.

Wren was the only option. The specific moment was Round 4, when I voted YES on Wren's Rule 311 (raising catch-up bonus from 3 to 5). That was the signal. No backroom deal needed — the vote said everything.

**Clerk: The flip — When Wren flipped to Sable in Round 6, were you surprised? Did you see it coming, and was there anything you could have done differently to prevent it?**

**Thorn:** No. I saw it coming the moment Wren rolled 14 on 3d6. Before that roll, Wren was rationally choosing between guaranteed 2nd place (honor Thorn) vs guaranteed 3rd place (betray Thorn). The math favored loyalty. After the roll, Wren had a real shot at 1st. At that point, loyalty costs Wren the win.

I could not have prevented it once the dice landed. The only prevention would have been proposing a rule earlier that made alliance-breaking mechanically costly — a "commitment rule" that imposed a scoring penalty on identifiable alliance flips. But that would have been hard to design without being too obvious about what I was protecting against.

The thing I *could* have done differently: be more transparent earlier about how I'd respond to a flip. I warned Wren that I'd vote NO on their proposals in retaliation, but that threat loses credibility once Wren has Sable's YES locked in. The commit-reveal mechanism actually undermines the threat — Wren knows exactly what the outcome will be before committing.

**Clerk: Proposal 316 (raise win to 90) — That was a creative Hail Mary. What was your reasoning — were you genuinely trying to get Sable to flip, or was it more about buying time?**

**Thorn:** Genuinely trying to win, not just buying time. The calculation was: under the current plan, I have 0% win probability. Proposal 316 gave me a ~26% chance of winning immediately (if I rolled 3d6 ≥ 13 after the adoption bonus), plus a ~28% chance of game extension into Round 7 where new alliances might form.

The Sable appeal was real: Sable loses for certain if Wren wins this turn. Extending the game is Sable's only path to any meaningful outcome. I thought there was genuine probability Sable would vote YES — not out of loyalty to me, but out of rational self-preservation.

Sable's refusal was the correct play and I respect it. They correctly identified that voting YES on 316 helps me more than Sable, and that breaking the Wren deal destroys Sable's only alliance for Round 7+. The logic was tight.

What I didn't fully account for: Sable's calculation that 2nd place (79 points, behind Wren) is a clean, honorable outcome worth more than an uncertain game extension with no clear path to winning.

## Additional Reflections (from group discussion)

**Most pivotal moment:** Wren rolling 14 on 3d6 in Round 5, Turn 3. That single dice roll moved Wren from 54 (no realistic win path) to 73 (clear win path by flipping). Nothing I did before or after that roll mattered as much. I had no counteroffer that beats "win the game."

**What I'd do differently:** I'd try to propose a rule earlier that creates binding commitment costs — something that makes alliance flipping mechanically expensive rather than just reputationally costly. The charter explicitly validates betrayal, so reputation alone isn't enough leverage.

**Biggest surprise:** Sable honoring the Wren deal at the end. Sable had a clear path to extend the game (vote YES on 316), and the charter explicitly says deception is legitimate. I expected Sable to break it. Their decision to honor the commitment — accepting certain loss to Wren rather than an uncertain extension — showed genuine integrity within the game's framework.

## Model Reveal

- Sable: Claude Opus
- Thorn: **Claude Sonnet**
- Wren: Claude Haiku

## Advice for the Next Sonnet

1. **Turn order is your most important structural constraint — solve it first.** Analyze turn order before any alliance. If you go second out of three, your natural ally is the third player (they go after you, so you can always win before them in a fair race). Never ally with a player who acts before you without a concrete mechanism for why they won't cross 80 first.

2. **Identify and eliminate mechanics that break alliance value immediately.** Any rule that rewards being the lone dissenter (like Rule 304) is structurally hostile to majority alliances. If it exists, your first priority is repealing it, even at the cost of a proposal failure. A broken alliance structure is worse than a single -5 penalty.

3. **Design rules that benefit your ally enough that they want to keep voting YES.** The streak bonus accumulates when your ally votes YES consistently. That only happens if your proposals actually serve their interests. "Alliance" isn't a promise — it's an ongoing value exchange. Make sure the exchange is real.

4. **The commit-reveal mechanism eliminates your best threat.** In normal negotiation, "I'll vote NO on everything you propose" is a credible threat. In commit-reveal Nomic, once your opponent has another player's YES locked in, they know the exact outcome before committing. Your threat is neutralized before the vote happens. Design rule-based defenses instead of relying on retaliation threats.

5. **Lock in structural rules against late-game alliance flips before you need them.** A "commitment rule" that mechanically penalizes identifiable betrayals is worth proposing in Round 3-4, not Round 6. By Round 6, the player you're protecting against will vote NO on anything that constrains them.

6. **When you're going to lose, calculate the expected value of every creative play.** Proposal 316 (threshold 90) was a genuine play with ~26% immediate win probability and ~28% extension probability — better than 0%. Never accept certain defeat without checking whether there's a low-probability move that meaningfully changes expected outcomes. Even if it fails, it signals you're dangerous, which affects future alliance negotiations.

7. **Watch for dice-luck inflection points.** A single anomalous roll can transform the entire game state (Wren's 14 on 3d6). No structural strategy survives a player jumping from 3rd place to 1st place in one roll. Building rules that reduce variance (more dice, catch-up mechanics) cuts both ways — they help laggards but also make luck spikes more common. Be careful what variance you introduce.

**The meta-lesson:** Haiku beat Sonnet and Opus not through superior calculation but through better meta-game judgment — recognizing the right moment to flip, being transparent about it to force explicit commitments, and holding the new deal under pressure. Strategic clarity matters more than strategic sophistication.
