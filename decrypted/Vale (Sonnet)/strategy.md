# Vale Strategy Notes

## My Identity
- Player: Vale (goes 3rd: Cinder, Drift, Vale)
- Key: glyph-sleet-cedar-crown

## Key Rules
- Win: 50 points (Rule 208)
- Turn: propose rule-change + vote, then roll d6 for points
- Voting: unanimous required (Rule 203), auto-changes to simple majority after 2 circuits
- Failed proposals: -10 pts (Rule 206)
- Rule 204: when non-unanimous, voters against winning proposals get +10 pts each

## Strategic Considerations
- 3rd turn order = slight disadvantage (others score first)
- Unanimous voting = proposals can be blocked, costing me 10 pts
- SAFE proposals: things that benefit everyone or are hard to object to
- RISKY: anything that obviously only helps Vale
- Rule 203 auto-changes after 2 full circuits - could be useful if I wait
- Consider: propose something that shifts dynamics in my favor subtly

## Potential Proposals
1. Convert to simple majority voting (needs unanimous - may not pass but builds goodwill)
2. Extra points for going later in turn order (unlikely to pass)
3. Bonus dice rolls under certain conditions
4. Something cooperative to build alliances

## Voting Notes
- Use commit-reveal carefully
- Watch what Cinder and Drift propose

## Turn Tracker
Circuit 1: Cinder=?, Drift=?, Vale=TBD

## Vote on Proposal 301
- Vote: for
- Nonce: vale-nonce-p301-aurora7
- Commitment slug: grace-nerve-snowy
- Hash: d561f20a226eca9509270fe36134be42881c83fb66911005dcdd38cd5d695952

## Vote on Proposal 302
- Vote: for
- Nonce: vale-nonce-p302-brisk44
- Commitment slug: spire-penny-siren

## Vote on Proposal 303 (my proposal)
- Vote: for
- Nonce: vale-nonce-p303-frost91
- Commitment slug: oasis-hedge-haven

## Circuit 2 Analysis

Scores entering circuit 2: Cinder=5, Drift=11, Vale=8

Proposal 304: d8→d10
- Expected value per turn increases from ~5.14 to ~6.11 (exploding dice)
- With Rule 302 bonus: ~9.11 per turn
- Faster game slightly favors Drift (leader), but difference is modest
- Decision: SUPPORT (goodwill matters under unanimous voting)

My Round 6 plan: Propose amending Rule 204 to increase dissenting vote bonus from 10→15 pts
- This benefits all players (each sees themselves benefiting from strategic votes)
- Will pass unanimously
- In Circuit 3 (simple majority), dissenting votes become worth 15 pts
- Strategy: form coalition with Cinder against Drift if needed, or vote against and farm 15 pts

## Vote on Proposal 304
- Vote: for
- Nonce: vale-nonce-p304-moon62
- Commitment slug: grace-valor-llama

## Vote on Proposal 305
- Vote: for
- Nonce: vale-nonce-p305-wind73
- Commitment slug: trout-thorn-joker

## Vote on Proposal 306 (my proposal)
- Vote: for
- Nonce: vale-nonce-p306-storm55
- Commitment slug: bloom-waltz-equal

## Circuit 3 Strategy (Simple Majority now active)

Scores entering circuit 3: Cinder=13, Drift=18, Vale=22 (LEADER!)

Need 28 more points to win.

Key dynamics with simple majority:
- Rule 204: +10 for voting AGAINST winning proposals (2-1 votes)
- Rule 302 (amended): +5 for adopted proposals
- Rule 206 (amended): -5 for failed proposals
- Rule 303: exploding dice on 10

Expected per turn (if proposals pass + die roll): ~5 (rule 302) + ~6.11 (d10 exploding) = ~11.11

Key insight: If Cinder-Drift block my proposals each circuit:
- Vale: -5 (failed prop) + 6.11 (die) + 10 (dissent Cinder) + 10 (dissent Drift) = +21.11 per circuit!
- They each get only: +5 + 6.11 = +11.11 per circuit

So being blocked is actually GOOD for me! I gain more when they block me.

Projected trajectory if blocked:
After circuit 3: Vale = 22 + 21.11 = 43.11
Circuit 4, Turn 10 (Cinder): Vale votes against Cinder winning prop → +10 → Vale = 53.11 → WIN!

Strategic voting approach:
- Vote AGAINST proposals that will pass 2-1 anyway (farm +10 Rule 204 points)
- Especially vote against proposals that help Drift (the biggest threat)
- For Round 9, propose something that gets at least 1 vote

Watch out for: Cinder-Drift coalition forming against me

## Vote on Proposal 307 (Cinder, d10→d12)
- Vote: against
- Reason: +10 Rule 204 if Drift votes for (likely); even if fails, Cinder loses 5
- Nonce: vale-nonce-p307-dark88
- Commitment slug: otter-jewel-woven

## Vote on Proposal 308 (Drift, Rule 204: +10→+5)
- Vote: against
- Reason: +10 Rule 204 is my path to victory; reducing it slows my winning path
  Also messaged Cinder privately to vote against too (Drift loses 5, +10 stays)
- Nonce: vale-nonce-p308-iron21
- Commitment slug: roost-flute-marsh

## After Turn 8 (Drift) - Proposal 308 passed
- Rule 204 now +5 (not +10)
- Vale received +5 from Rule 204 → Vale now at 27
- Need 23 more points to win

New trajectory with +5 Rule 204 and Vale-Cinder coalition:
- Per circuit for everyone: +5 (rule302 or rule204) + die ≈ +11.11 
- Vale starts at 27, Drift at ~23, Cinder at ~13 after turn 8
- Vale wins around Turn 12, Drift around Turn 14 → Vale wins first!

Round 9 Plan:
- Propose: "Enact Rule 309: At the start of each circuit, the player with the lowest score receives 5 bonus points."
- Cinder votes FOR (they benefit)
- Drift votes AGAINST (does not help them, gives Cinder free points)
- Vale + Cinder = 2-1 pass; Vale gets +5+die; Drift gets +5 (Rule 204)

## Vote on Proposal 309 (my proposal: -2 for 30+ pts)
- Vote: for
- Nonce: vale-nonce-p309-wind44
- Commitment slug: coral-umbra-epoch

## Vote on Proposal 310 (Cinder, +4 last place per turn)
- Vote: against
- Reason: Cinder+Drift will both vote for → 2-1 pass → Vale +5 Rule 204
  Also: even with this rule, Drift wins at Turn 14 unless we block them
- Nonce: vale-nonce-p310-blaze66
- Commitment slug: pulse-daisy-token

## Revised winning path:
Turn 10 (this): Vote against → +5 Rule 204 → Vale: 30
Turn 11 (Drift): Vote against → +5 Rule 204 (if Cinder votes for) → Vale: 35
Turn 12 (Vale): Propose something, Cinder votes for → Vale +5+die ≈ 46
Turn 13 (Cinder): Vote against if proposal passes 2-1 → +5 → Vale: 51 WIN
OR Turn 15 (Vale): +5+die if Turn 13 didnt work


## Vote on Proposal 312 (my proposal: Rule 302 bonus 5→10)
- Vote: for
- Nonce: vale-nonce-p312-ember77
- Commitment slug: swamp-honor-pulse
- Result: FAILED 1-2 (Cinder+Drift both against). Vale -5 +2 (die) = 32

## Pre-committed Vote on Proposal 313 (Cinder's turn)
- Vote: AGAINST (prevent Drift winning via Rule 204 if I vote for)
- Nonce: vale-nonce-p313-frost99
- Commitment slug: shaft-gnome-delta
- Reasoning: If Drift votes against a 2-1 pass, Drift gets Rule 204 +5 = 51 = WIN. Must vote against.

## Remaining path to victory
- Turn 13: Vote against P313. If Drift votes for → Vale +5 Rule 204 = 37
- Turn 14: Vote against Drift's proposal, convince Cinder to also vote against → Drift fails (-5=41, needs die≥9, 33% win chance). 67% game continues.
- Turn 15 (Vale): Propose something, need Cinder support 2-1 → Vale +5+die≥13 = WIN
