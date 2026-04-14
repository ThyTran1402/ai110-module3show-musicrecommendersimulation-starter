# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest 5 songs from a small curated catalog based on a user's preferred genre, mood, and energy level. It is intended for classroom exploration of how content-based recommendation systems work. It is **not** designed for deployment with real users, real listening data, or large-scale catalogs. It should not be used to make editorial or business decisions about music.

---

## 3. How the Model Works

Every song in the catalog carries a set of tags and numbers describing its musical character — things like whether it's "pop" or "metal," whether it feels "happy" or "intense," and a number from 0 to 1 indicating how energetic it is.

A user tells the system their favorite genre, favorite mood, and ideal energy level. The system then goes through every single song in the catalog and gives it a score:

- If the song's genre matches the user's favorite, it gets 2 points.
- If the mood matches, it gets 1 point.
- It gets an energy bonus from 0 to 1 depending on how close its energy is to the user's target — a perfect match gives a full point, while a song at the opposite extreme gives close to zero.
- If the user prefers acoustic music and the song is highly acoustic, it gets a small bonus.

After all songs are scored, the list is sorted from highest to lowest score and the top five are shown along with the reasons they ranked where they did.

---

## 4. Data

- **Catalog size**: 18 songs (10 original starter songs + 8 added during development).
- **Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, R&B, country, metal, classical, EDM, folk, reggaeton.
- **Moods represented**: happy, chill, intense, relaxed, focused, moody, hype, romantic, peaceful, euphoric, melancholy.
- **Numerical features**: energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), acousticness (0–1).
- **Limitations of the data**: The catalog was hand-crafted for this simulation. It is not drawn from real listener behavior or any streaming platform's database. Tastes and genre boundaries reflected here are one person's interpretation and may not generalize.

---

## 5. Strengths

- **Transparent scoring**: every recommendation comes with a plain-language reason list, so users can understand exactly why a song was suggested.
- **Works well for clear, consistent profiles**: users with a single strong preference (e.g., "I only listen to lofi chill music") get intuitive results — the top songs are exactly what you would expect.
- **No data privacy concerns**: the system uses only the preferences the user explicitly provides; it stores no listening history.

---

## 6. Limitations and Bias

- **Genre dominance creates a filter bubble**: the +2.0 genre bonus means a mediocre genre match will almost always outrank a great cross-genre match. A user who loves pop will rarely see a jazz song even if it matches their energy and mood perfectly.
- **Binary attribute matching**: "indie pop" never matches "pop." Two moods that feel nearly identical — "relaxed" and "chill" — score zero against each other. The system has no concept of semantic similarity.
- **Small catalog amplifies bias**: with only 18 songs, some genres appear once. The metal listener will always see Iron Curtain at #1 because there is no competition. In a real catalog of millions, this effect is diluted.
- **Energy gap formula treats all distances equally**: whether a song is 0.1 or 0.8 away from the user's target, the penalty is proportional but there is no threshold — a song 0.3 away still gets 0.7 points, which may feel misleadingly high.
- **No diversity enforcement**: the top 5 results can all come from the same genre if the catalog is small and one genre dominates, which mirrors the "filter bubble" problem in real recommenders.

---

## 7. Evaluation

Three user profiles were tested:

**Profile 1 — Happy Pop Fan** (`genre=pop, mood=happy, energy=0.8`)
*Sunrise City* ranked first with a score of 3.98. This felt correct — it is a pop song with a happy mood and energy of 0.82. The second result, *Gym Hero*, scored 2.87 because it matched genre and energy but not mood ("intense" ≠ "happy"). The system correctly penalized the mood mismatch.

**Profile 2 — Chill Lofi Listener** (`genre=lofi, mood=chill, energy=0.35`)
*Library Rain* ranked first with a perfect score of 4.00 because its energy (0.35) exactly matched the target. This showed that energy similarity can act as a tiebreaker within the same genre/mood group. Results felt very natural for this profile.

**Profile 3 — High-Energy Metal Head** (`genre=metal, mood=intense, energy=0.95`)
*Iron Curtain* ranked first (3.98), but it was the only metal song in the catalog. The #2 and #3 spots went to pop and rock songs with matching mood but different genres — this is the genre-scarcity bias in action.

**Experiment** — halving the genre weight from +2.0 to +1.0 caused cross-genre songs with good energy alignment to climb the rankings, demonstrating how sensitive the output is to weight choices.

---

## 8. Future Work

1. **Fuzzy genre/mood matching**: use a similarity lookup table (e.g., "indie pop" → similar to "pop") so related categories can earn partial credit instead of zero.
2. **Diversity penalty**: after ranking, apply a rule that reduces the score of any song whose genre is already represented in the top results, preventing one genre from monopolizing every slot.
3. **Weighted feature configuration**: let users specify their own weights at runtime rather than hardcoding them, so a mood-first listener can tell the system "mood matters most to me."
4. **Collaborative signal layer**: add a simple "users who liked X also liked Y" lookup table to complement the content-based score, capturing the social dimension that content-alone systems miss.

---

## 9. Personal Reflection

Building VibeFinder made the invisible visible. Every streaming platform I have ever used makes decisions like "how much should genre matter versus mood?" — they just make them at a scale of millions of users and billions of data points, where the consequences of getting it wrong are harder to see. Writing the +2.0 and +1.0 weights myself forced me to own those choices explicitly.

The most surprising moment was discovering how quickly a simple scoring system creates filter bubbles. With only 18 songs and a genre bonus that's twice any other signal, a pop listener almost never escapes the pop section — even when there are jazz songs with nearly identical energy and mood profiles. That's a miniature version of what happens on real platforms, and it was unsettling to produce it so easily.

AI tools helped most during brainstorming — generating edge-case profiles and suggesting how to structure the scoring math. But they also produced suggestions I had to verify carefully; at one point a suggestion used `.sort()` in a way that would have mutated the catalog list mid-loop. Human judgment on correctness, not just syntax, still matters a lot.

If I continued this project, I would focus on diversity: making the system intentionally recommend songs from at least two or three different genres in every top-5 list, which is closer to how a thoughtful human playlist curator would operate.
