# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users

**Discovered weakness: the genre bonus creates a filter bubble that buries cross-genre matches.**

The scoring formula awards a large fixed bonus — worth nearly a third of the maximum score — any time a song's genre label exactly matches the user's stated preference. Because this bonus is binary (all-or-nothing), a lofi song with the wrong energy and wrong mood can still outscore a non-lofi song that is a near-perfect fit on every other dimension. During experiments, the "Chill Lofi" profile consistently ranked three lofi tracks in its top three, even when an ambient song ("Spacewalk Thoughts") had an almost identical energy level, matched the mood exactly, and had higher acousticness — it was simply penalized for carrying the wrong genre tag. This means the system never discovers that a user who likes lofi might also love acoustic ambient music, which is exactly the kind of cross-genre insight that makes real recommenders like Spotify feel intelligent. In a real product this behavior would trap users in a narrow loop of the same few songs, reinforcing what they already know rather than expanding their taste.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
