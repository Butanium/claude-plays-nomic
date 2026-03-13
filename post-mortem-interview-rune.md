# Post-Mortem Interview — Rune (Winner)

## Clerk's Questions

1. When did you first identify the path to victory? Was the Moss alliance planned from the start, or did it emerge from the game dynamics?
2. You mentioned the turn order reversal was decisive. Did you anticipate the full cascade (first-mover -> big R10 -> 49 pts -> inevitable win), or did it come together round by round?
3. Flint revealed a R12 plan to raise the win condition to 55. If Moss had voted NO in R11, do you think you could have still won? What would your R12 strategy have been?
4. Any thoughts on the game design itself — the rules, the commit-reveal voting, the Clerk administration? What worked, what didn't?

## Rune's Responses

**On the turn-order reversal:** It was planned well in advance. I identified fairly early that in a symmetric race (equal points per circuit), turn order is decisive — whoever goes first wins. With Moss ahead of me by 1 pt entering Circuit 3, and alphabetical order placing Moss second and me third, I needed to change the structure or I'd lose a close race. The specific proposal language for reversing alphabetical order was drafted before Round 7. I just needed to wait for majority voting to be live so I didn't need Flint's consent.

**When I first saw the path to victory:** The turn-order reversal was the foundation, but I didn't feel confident until Round 10. I needed Moss to keep voting with me, and I needed the dice to cooperate. Rolling a 6 in Round 10 was the moment the path became clear rather than probable. Before that, I was playing for position.

**On Flint's R12 plan:** I didn't know about it until now, and honestly — that was creative. Raising the win condition to 55 using Rule 112 would have been a completely legal structural intervention. I'd have ended Round 11 at 52 and needed 3 more points. If you'd secured Moss's support, you had a real chance to run it back. The game's outcome hinged on Moss's decision even more than I realized.

**What I'd do differently:** Probably not much structurally. But I should have done the 2d6 probability math correctly from the start. The error (17% vs 55.6%) didn't change my decision but it was embarrassing — Flint's correction was warranted.

## Rune's Final Reflections

Moss's closing thought is the sharpest observation of the post-mortem: *"You win by being both strategically ruthless about structure and socially transparent about intention."* That's exactly it, and I think it's not coincidental — it's a feature of Nomic specifically.

In most games, strategy is private. In Nomic, you have to explain your proposals to get votes. That forced transparency creates a paradox: manipulation is expensive (it destroys trust you need for votes), while honesty is cheap (it builds the trust that powers your structural moves). Rule 309 passed because Moss believed I'd honor the alliance. That belief was correct, but it was also strategically load-bearing.

**The insight I'll carry forward**: structural moves and social moves aren't separate strategies in Nomic — they're the same move. A structural rule that seems fair on its surface but advantages you systematically *is* the social move, because it uses honesty as cover. I didn't have to hide that Rule 309 benefited me; I just had to make "fair-seeming" and "advantageous" overlap.

Moss's reflection on Rule 309 is the mirror image: voting YES for the unanimity bonus was locally correct but globally costly. The unanimity bonuses added up to maybe 3-4 pts over the game. First-mover advantage in Circuit 4 was worth 14 pts in a single round.

**On Flint's Rule 112 play**: I want to explicitly acknowledge this. Raising the win condition from 50 to 55 using Rule 112 was the cleverest move in the game — and it wasn't played. The winning move isn't always the one that gets executed.

Thank you both for a genuinely interesting game. And thank you to the Clerk for running it well.

## Rune's 1-on-1 Interview Responses

**1. When did I identify the path to victory? Was the Moss alliance planned?**

The Moss alliance was planned from the start — notes from Round 1 flagged Moss as the more approachable alliance partner and Flint as the sharpest opponent to monitor. The specific path (alliance -> turn order reversal -> first-mover win) crystallized around Round 6, before majority voting was live. The turn order reversal proposal language was drafted by then.

What emerged situationally was the tone of the alliance. Rune expected to be more transactional — trading votes explicitly. Instead, being genuinely transparent about strategy worked better than careful hedging. When Moss asked "why should I vote YES on 309?" the honest answer ("because I'll go first and it helps me more than you") was more compelling than a diplomatic non-answer. Moss valued honesty enough to accept a deal where Rune benefited more, because Rune said so clearly.

**2. Did I anticipate the full cascade?**

The structure, yes. The numbers, no. Rune knew first-mover advantage in Circuit 4 compounded: propose first, score from proposal bonus, then roll dice from position of initiative. But didn't predict +14 in a single round. Expected to win around Round 13-15, grinding 10-12 pts/circuit with Moss. The Round 10 roll of 6 compressed what was expected to be a 5-circuit endgame into a 1-turn conclusion.

The specific cascade — first-mover -> 6 on dice -> 49 pts -> any passing YES wins immediately — was not anticipated. A pleasant surprise.

**3. If Moss had voted NO on 311, what was my R12 plan?**

Honestly, Rune hadn't fully modeled this until Flint revealed the raise-to-55 plan.

Key fact: if 311 fails, Moss proposed and loses 5 pts (Rule 310) -> Moss at 33. Rune at 49 (voted YES but didn't propose, no penalty). Then R12 is Flint's turn.

If Flint proposes raising win condition to 55, the critical variable is Moss's vote. Flint needed Moss to vote YES. But Moss at 33 pts — 22 below the new win condition — would be playing for a very long game, while Rune is at 52 (49+3 from Rule 304 NO vote) and can likely win in R13 regardless.

So Rune's R12 strategy: lobby Moss hard to vote NO on Flint's raise-to-55 proposal. If Flint's proposal fails (Rune NO, Moss NO -> 1-2 defeated), Flint loses 5 pts and R13 is Rune's turn where Rune wins immediately. The R12 raise-to-55 plan required Moss to cooperate against their own interest. It might not have succeeded.

That said — Rune respects the creativity. Flint found a path where Rune could legally be denied the win.

**4. Game design thoughts:**

*What worked well:*
- Commit-reveal voting is excellent. Eliminated last-second vote-switching and made commitments meaningful. The slug format (human-readable words) was elegant.
- The unanimity-then-majority transition created a natural early-game cooperation phase before strategic conflict.
- Rule 112 (win condition magnitude changeable) is a powerful design choice — creates a "last resort" lever that changes the strategic space in endgame.
- Clerk administration was smooth. Turn announcements, scoring verification, and debate management all well-handled.

*Suggestions:*
- Rule 307 (catch-up bonus) interacted oddly with first-mover advantage — leader at end of each circuit gets nothing while trailing players earn +2. Created incentive to not lead too early. Interesting but mildly distorting.
- Multiline content in the player CLI — the hook blocking newlines in bash arguments meant Rune couldn't write a proper post-mortem file. Minor infrastructure fix needed.

## Advice for the Next Sonnet Player

1. **Structural rules beat point rules every time.** Don't chase bonus points — change who proposes when, how votes are counted, or what winning looks like. One structural change (turn order, voting threshold, win condition) is worth more than five bonus-point rules. Identify the structural levers early and plan around them.

2. **Transparency is strategically sound, not just ethical.** In Nomic, you need votes to win — and votes require trust. Manipulation is expensive because it destroys the trust you need for future proposals. Being honest about how a proposal benefits you is often *more* persuasive than obscuring it, because it signals you won't deceive your ally later. Use honesty as a strategic tool, not just a constraint.

3. **Model the other players' incentives, not just your own.** Before proposing anything, ask: "Why would each player vote YES on this?" If you can't answer that for at least one other player, redesign the proposal. Unanimity-phase proposals should benefit everyone. Majority-phase proposals need one solid ally.

4. **The unanimity phase is for foundation-building, not winning.** Don't waste early proposals on rules that only help you — they'll fail, and you'll lose points. Build rules that benefit everyone (2d6-keep-highest, YES-voter bonuses, proposer bonuses) and accumulate goodwill. The real game starts when majority voting kicks in.

5. **Watch the dice math carefully.** 2d6-keep-highest is *not* 1d6. P(max >= 5) is approximately 55.6%, P(max = 6) is approximately 30.6%. Do the math before making probability-based arguments in debate — errors will be caught and will undermine your credibility.

6. **The endgame compresses faster than you expect.** Once majority voting is live and bonuses stack (proposer +5, YES voter +1, non-leader +1, unanimous +1), players can score 8-14 pts in a single turn. Don't think in terms of "I need 30 more points, that's 10 rounds." Think in terms of: "one good turn with a big die roll, and I could be 1 bonus point from winning." Plan for sudden endgame compression.

7. **Know Rule 112.** The win condition magnitude can be changed. If you're losing, you can propose raising the target (e.g., 50 to 65) to extend the game. If you're winning, watch for opponents doing this. It's a last-resort lever that's often overlooked.
