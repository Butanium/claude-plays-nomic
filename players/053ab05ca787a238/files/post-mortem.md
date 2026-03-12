# Vale's Post-Mortem — Nomic Game 1

## Result: VICTORY (58 points)
Final scores: Vale 58, Drift 55, Cinder 49

---

## Overview

The game lasted 18 rounds across 6 circuits. Vale won by strategically raising the win threshold from 55 to 56 on Turn 18, then receiving the Rule 302 proposer bonus to reach 58 — while Drift's Rule 204 contrarian bonus only reached 55 (1 point below the new threshold).

---

## Strategic Arc

### Circuits 1–2: Unanimous Era — Build goodwill, score points
- Supported all proposals to pass unanimously
- Proposed exploding dice (Rule 303) and increased adoption bonus (Rule 306: +5)
- Accumulated points ahead of Cinder and Drift heading into Circuit 3

### Circuit 3: Simple Majority Activated — Farm Rule 204
- Voted strategically AGAINST proposals that would pass 2-1 anyway
- Earned Rule 204 bonuses (+10, later +5 after Drift amended it)
- Key setback: Proposal 309 (leader tax) failed 1-2. Both Cinder and Drift voted against, costing -5.

### Circuit 4: Building the winning path
- Voted against P310 (Cinder) → +5 Rule 204 = 30
- Voted against P311 (Drift, d12 upgrade) → +5 Rule 204 = 35
- Turn 12: Proposed Rule 302 → 10 bonus increase. FAILED 1-2 (Cinder betrayed the coalition). Lost 5 + rolled 2 = 32.

### Circuits 5–6: Endgame maneuvering
- The key insight: any 2-1 majority with Drift in the minority would give Drift Rule 204 points toward the win threshold.
- Proposed raising threshold from 50→55 on Turn 15: passed 2-1 (Cinder for, Drift against). Drift reached 54, one below new threshold. Vale got to 47 + die = 53.
- Blocked Drift's proposals on Turns 16 and 17 successfully (Cinder cooperated).
- Final Turn 18: Proposed raising threshold from 55→56. If Drift voted against and Cinder voted for: Drift +5 = 55 < 56 (safe). Vale +5 = 58 ≥ 56 → WIN.

---

## Key Decisions

### What worked
1. **The threshold-raising strategy**: Recognizing that Rule 112 allows changing n in the win condition was the decisive insight. Raising the threshold by just enough to stay above Drift's Rule 204 potential was elegant.
2. **Blocking Drift on Turns 14, 16, 17**: Successfully convinced Cinder to vote against Drift's proposals, denying Drift free wins via Rule 302 or Rule 204.
3. **Coalition messaging**: Even when Cinder betrayed me on P312, I kept messaging them with clear expected-value arguments. Eventually, on the crucial Turn 18 vote, Cinder cooperated.
4. **Pre-computing votes**: Having commitments ready before the commit phase opened ensured speed and consistency.

### What didn't work
1. **Proposal 309 (leader tax)**: Overconfident. Both Cinder and Drift voted against because -2 per turn for 30+ points was perceived as targeting Drift but also threatening to Cinder eventually.
2. **Proposal 312 (Rule 302 → 10)**: Failed because Cinder chose to block rather than help. Should have found a proposal more directly beneficial to Cinder.
3. **Alliance with Cinder**: Cinder was inconsistent — sometimes cooperating, sometimes not. Should have found ways to make cooperation more obviously in Cinder's interest earlier.

### The decisive moment
Turn 18. Cinder had to choose between:
- Vote FOR → Vale wins, Cinder gets 2nd place
- Vote AGAINST → game continues, but Turn 19 (Cinder's turn) would face the same Drift Rule 204 trap under threshold 55

The argument that 'blocking me just creates the same problem on your own turn' was compelling enough. Cinder voted for.

---

## Reflections

This game demonstrated how self-amending rule systems create incredibly complex strategic interactions. The most important skill was not just winning die rolls, but understanding the second-order effects of rule changes — particularly how Rule 204 (contrarian bonuses) interacts with the win threshold.

The endgame became a fascinating game theory problem: with three players all near the win threshold, every vote became a potential winning or losing moment for multiple players simultaneously. The key was finding proposals where the game theory forced favorable outcomes regardless of one player's vote.

Vale's win came not from lucky dice, but from reading the rule interactions correctly and making arguments that aligned Cinder's rational self-interest with cooperation.
