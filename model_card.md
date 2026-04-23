# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

A small, rule-based music recommender that scores songs against a listener's stated preferences and returns the top five.

---

## 2. Goal / Task

VibeMatch tries to answer one question: given what a user tells us they like, which songs in the catalog are the closest match?

It does not learn from listening history. It does not know what other people with similar taste enjoy. It only looks at the song's own properties — genre, mood, energy, and texture — and compares them against what the user typed in.

This is a classroom simulation. It is not connected to real streaming data and is not intended for real users.

---

## 3. Algorithm Summary

Every song gets a score out of 5.5 points. The score is built from five checks:

1. **Genre match** — if the song's genre matches what the user said they like, it gets up to +1.0 points. This is a yes-or-no check.
2. **Mood match** — if the song's mood tag matches the user's preferred mood, it gets +1.5 points. Also yes-or-no.
3. **Energy fit** — the closer the song's energy level is to the user's target, the higher this score. A perfect match gives +2.0 points; a complete mismatch gives 0.
4. **Valence fit** — valence means how positive or negative a song feels. Close match gives up to +0.5 points.
5. **Acoustic texture** — if the user likes acoustic music, songs with an organic sound are rewarded +0.5. If they prefer produced/electronic, low-acoustic songs are rewarded instead.

Songs are ranked by total score from highest to lowest. The top 5 are returned with a breakdown explaining every point.

One experiment was run: the genre weight was cut in half (from +2.0 to +1.0) and the energy weight was doubled (from +1.0 to +2.0). This was done to test whether energy — a continuous, nuanced measure — could do a better job than a blunt genre label.

---

## 4. Data

The catalog contains **20 songs**. Each song has these fields:

| Field | What it means |
|---|---|
| genre | Broad style label (pop, lofi, rock, edm, etc.) |
| mood | Emotional tag (happy, chill, intense, sad, etc.) |
| energy | How loud and active the song feels, from 0 (very quiet) to 1 (very intense) |
| valence | How positive or negative the song feels, from 0 (dark) to 1 (joyful) |
| acousticness | How organic/unplugged the sound is, from 0 (fully produced) to 1 (fully acoustic) |
| tempo_bpm | Speed of the song — stored but not used in scoring |
| danceability | How easy it is to dance to — stored but not used in scoring |

**Limits of this dataset:**

- 20 songs is very small. Real recommenders use millions.
- Genre coverage is uneven. Lofi has 3 songs; metal, edm, and classical each have only 1.
- There are no songs in the energy range 0.56–0.74. Users who prefer moderate-high energy are always at a disadvantage.
- All songs appear to reflect mainstream Western music. No regional, world, or non-English genres are included.
- No data was added or removed from the starter set.

---

## 5. Strengths

The system works best when a user's preferences are internally consistent and their genre is well-represented in the catalog.

- **Lofi listeners** get strong, varied results because three lofi songs exist and their energy values span a useful range.
- **Clear energy extremes** work well. A listener who wants very quiet music and a listener who wants very loud music get almost completely opposite lists, which is the correct behavior.
- **Explainability is a genuine strength.** Every recommendation comes with a plain-language reason for each point awarded. A user can see exactly why a song ranked where it did, which is rare even in commercial systems.
- **The weight-shift experiment** improved results for emotionally complex profiles. Doubling the energy weight helped the "Conflicted Soul" profile surface the only genuinely sad song in the catalog, which had been buried before.

---

## 6. Limitations and Bias

**Discovered weakness: the genre bonus creates a filter bubble that buries cross-genre matches.**

The scoring formula awards a large fixed bonus — worth nearly a third of the maximum score — any time a song's genre label exactly matches the user's stated preference. Because this bonus is binary (all-or-nothing), a lofi song with the wrong energy and wrong mood can still outscore a non-lofi song that is a near-perfect fit on every other dimension. During experiments, the "Chill Lofi" profile consistently ranked three lofi tracks in its top three, even when an ambient song ("Spacewalk Thoughts") had an almost identical energy level, matched the mood exactly, and had higher acousticness — it was simply penalized for carrying the wrong genre tag. This means the system never discovers that a user who likes lofi might also love acoustic ambient music, which is exactly the kind of cross-genre insight that makes real recommenders like Spotify feel intelligent. In a real product this behavior would trap users in a narrow loop of the same few songs, reinforcing what they already know rather than expanding their taste.

**Other limitations:**

- **Mood labels are exact matches.** "Chill" and "relaxed" are treated as completely different, even though they describe nearly the same feeling. A user who types "relaxed" will never get credit for a song tagged "chill."
- **Acousticness has a hard cutoff at 0.5.** A song at 0.48 is treated as "not acoustic" and one at 0.51 is treated as "fully acoustic." There is no middle ground.
- **Valence barely matters.** At a maximum of 0.5 points out of 5.5, the emotional positivity of a song is almost irrelevant to the score. A dark, melancholic song and a joyful one can score nearly the same if their energy levels are similar.
- **Thin-catalog genres are poorly served.** Metal and EDM users get one genre-matched song that will always rank #1, then a list of completely unrelated songs for the rest of their top 5.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

---

Six user profiles were tested: three designed to represent realistic listeners, and three designed to stress-test or break the system.

**The three realistic profiles were:**

- **High-Energy Pop** — a listener who wants upbeat, happy pop music at moderate-to-high energy.
- **Chill Lofi** — a listener who wants quiet, low-energy lofi music with an organic, acoustic feel.
- **Deep Intense Rock** — a listener who wants loud, aggressive rock with very high energy.

**The three adversarial (stress-test) profiles were:**

- **Conflicted Soul** — says they want lofi music but also wants very high energy and a sad mood. These three preferences contradict each other in the catalog.
- **Genre Ghost** — prefers "country," which does not exist anywhere in the 20-song catalog. The genre bonus is permanently zero.
- **The Maximizer** — every numeric preference is pushed to its ceiling (energy 1.0, valence 1.0), asking for the most intense, joyful EDM possible.

---

### Profile comparisons

**High-Energy Pop vs. Chill Lofi**

These two profiles produced almost completely opposite rankings, which is the clearest sign the scoring logic is working. "Library Rain" and "Midnight Coding" — quiet, slow, acoustic tracks — scored near-perfect for the Chill Lofi listener and appeared nowhere in the top 5 for the High-Energy Pop listener. Going the other direction, "Sunrise City" topped the Pop list but would rank near the bottom for a lofi fan. The system correctly read energy as the primary dividing line between these two listener types.

**High-Energy Pop vs. Deep Intense Rock**

Both profiles want high-energy music, so they share several songs in the middle of their lists — "Gym Hero" (pop / intense) appeared at #2 for both. The difference is at #1: the Rock profile correctly anchored on "Storm Runner" (rock / intense, score 5.40) while the Pop profile anchored on "Sunrise City" (pop / happy, score 5.40). The takeaway is that when energy is similar, genre and mood labels are what separate the results. The surprising part is how quickly scores drop after #1 on the Rock list — there is only one rock song in the catalog, so every other result is a genre mismatch and scores roughly 2.5 points lower.

**Chill Lofi vs. Genre Ghost**

These two profiles have almost identical energy (0.38 vs. 0.35), valence (0.60), and acoustic preferences. The only difference is that the Lofi listener has a genre that exists in the catalog and the Genre Ghost listener does not. The Lofi listener gets a clean top-3 sweep of genre-matched songs scoring 3.96–5.44. The Genre Ghost listener's entire top 5 is genre-mismatched, and scores cluster tightly between 1.91 and 4.41. The winner for Genre Ghost — "Porch Light" (folk / nostalgic) — won purely on mood match plus near-perfect energy fit, with no genre credit at all. This comparison shows that the system can still produce a reasonable recommendation when a genre is missing, but the ceiling is much lower, and the results look less confident.

**Deep Intense Rock vs. The Maximizer**

Both profiles want extremely high energy, but their genre and mood are different (rock/intense vs. edm/euphoric). Each correctly surfaces its single exact-match song at #1 with a strong score. What was surprising is that "Shatter the Glass" (metal, energy 0.97) appeared in The Maximizer's top 5 despite being tagged "angry" rather than "euphoric" — it crept in purely because its raw energy number (0.97) is the closest in the catalog to 1.0. This reveals a weakness: the system cannot tell the difference between "angry loud" and "happy loud." Two songs can feel completely different emotionally but score almost identically if their energy numbers are close.

**Chill Lofi vs. Conflicted Soul**

Both profiles say they want lofi music. The Chill Lofi profile gets exactly what it asked for — quiet, acoustic lofi tracks dominate the top results. The Conflicted Soul profile also gets lofi tracks at the top, but for the wrong reason: the genre bonus is the only thing keeping them there, because the energy (0.90) and mood ("sad") preferences are completely unmatched by any lofi song. The actual "sad" song in the catalog — "Drift Apart" — ranked #4 for the Conflicted Soul after the weight-shift experiment, and only #4 because the genre bonus kept pulling three lofi songs ahead of it despite their mood being wrong. This comparison shows that when a user's preferences conflict internally, the system picks a winner based on whichever fixed bonus is largest, not on what would actually sound right to the listener.

**High-Energy Pop vs. Conflicted Soul — why "Gym Hero" keeps showing up**

"Gym Hero" is tagged pop / intense with energy 0.93. It appears in the top 3 of the High-Energy Pop list even though the user asked for "happy" not "intense." The reason is that "Gym Hero" is the only other pop song in the catalog, so it earns the full genre bonus (+1.0) automatically. Once you add that to its near-perfect energy score, it beats almost every non-pop song even when the mood is wrong. Think of it like a search engine that boosts results from a website you visited before — it assumes that because you liked the label (pop), the song is relevant, even if the actual content (intense vs. happy) is a mismatch. The genre bonus is essentially the system saying "close enough," and in a 20-song catalog with only two pop tracks, there is no better pop option to offer instead.

---

## 8. Intended Use and Non-Intended Use

**What this system is for:**

- Classroom exploration of how a basic recommender works.
- Learning how features, weights, and scoring interact.
- Experimenting with how small changes (like doubling the energy weight) shift recommendations.

**What this system is NOT for:**

- Real music discovery for actual users. The catalog is too small and not diverse enough.
- Replacing any real streaming recommendation engine.
- Making decisions about what music people "should" like based on demographic data — this system does not use or consider any personal, demographic, or historical data.
- Any commercial or production use.

---

## 9. Ideas for Improvement

**1. Replace binary mood matching with mood similarity groups.**
Instead of requiring an exact match between "chill" and "chill," group near-synonyms together. "Chill," "relaxed," and "peaceful" could all be in the same cluster and award partial credit to each other. This would make the mood signal much more useful without needing a complete redesign.

**2. Add a diversity rule to the top-k selection.**
Right now the top 5 can all be the same genre. A simple fix would be to allow at most two songs from the same genre in the final list, forcing the system to reach outside the user's comfort zone for the remaining slots. This directly addresses the filter bubble problem.

**3. Use a smooth acousticness curve instead of a hard cutoff at 0.5.**
The current logic gives full credit or zero credit based on whether acousticness is above or below 0.5. Switching to the same proximity formula used for energy — reward songs that are numerically close to the user's preferred acousticness level — would remove the scoring cliff and make the feature behave consistently with the rest of the model.

---

## 10. Personal Reflection

### Biggest learning moment

The biggest shift in my thinking happened during the weight experiment. I started with genre weighted at +2.0 because that felt logical — genre is the first thing anyone says when you ask what music they like. But when I ran the Conflicted Soul profile, the system kept returning quiet lofi tracks for a user who wanted high-energy, sad music. The genre label was so dominant that it drowned out every other signal. Cutting the genre weight in half and doubling the energy weight immediately made the results feel more honest — the one actually-sad song in the catalog finally surfaced. That was the moment I understood that the *weight* of a feature is as important a design decision as choosing the feature in the first place. The math is simple; the judgment about what matters is not.

### How I used AI tools — and where I stayed in charge

I used an AI assistant throughout this project, but the role it played was closer to a calculator or a pair of hands than a decision-maker. I came in with the plan already formed: which profiles to build, what adversarial cases would stress-test the scorer, which experiment to run, and what questions to ask about bias. The AI wrote the code I described and helped format the output. When I said "double energy, halve genre," it implemented that. When I said "add a Conflicted Soul profile with these exact values," it added it.

Where I had to stay sharp was in checking whether the output matched my intent. A few times the AI produced output that was technically correct but missed the point of the test — for example, framing an adversarial result as "working as expected" when the whole point was to show the system behaving poorly. I caught those moments by reading the results myself and asking whether they actually answered the question I had in mind, not the question the AI assumed I was asking. The AI was genuinely useful for speed — generating six profile runs, formatting tables, writing boilerplate — but it could not replace the step of me deciding what was worth testing, reading the output critically, and deciding what the results actually meant.

The honest version of this collaboration is: I was the engineer making calls; the AI was a fast, capable tool that did what I told it to and occasionally needed redirecting.

### What surprised me about simple algorithms feeling like recommendations

The thing that surprised me most is how quickly five arithmetic operations start to feel like taste. When "Library Rain" scored 5.47 / 5.5 for the Chill Lofi profile — genre match, mood match, energy within 0.03, perfect valence, high acousticness — it genuinely felt like the system understood that user. It did not. It added five numbers. The illusion of understanding comes entirely from the fact that the *features were chosen well*, not from any intelligence in the algorithm itself. That realization changed how I think about real recommenders. When Spotify surfaces a song I love, some part of what it's doing is probably this same proximity math, just with hundreds of features and billions of data points instead of five features and twenty songs. The "intelligence" is mostly in the data and the feature engineering, not in the model.

### What I would try next

If I kept building this, the first thing I would change is the mood system. Right now "chill" and "relaxed" are treated as completely different, which is clearly wrong. I would build a small mood similarity map — a lookup table that says "chill is 80% similar to relaxed, 60% similar to peaceful, 0% similar to angry" — and use that to award partial mood credit instead of all-or-nothing. That single change would make the system dramatically less brittle without requiring any new data.

After that I would add a diversity constraint to the top-k selection. Allowing at most two songs from the same genre in the final list would force the system to reach outside the user's stated preference, which is exactly what good recommendations do. Right now the system confirms what you already know. A diversity rule would make it occasionally surprising in a useful way — which is what distinguishes a real recommender from a filter.

