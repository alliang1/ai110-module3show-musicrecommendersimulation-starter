# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a basic content-based music recommender. It represents
songs and a user "taste profile" as data, scores every song in the catalog
against that profile, and returns the top-ranked matches with plain-language
explanations for why each song was chosen.

---

## How The System Works

Real platforms like Spotify and YouTube blend two main approaches:
**collaborative filtering** (recommending based on what similar users liked
or listened to) and **content-based filtering** (recommending based on the
actual attributes of the content itself — genre, tempo, mood, etc.). This
project implements a simplified content-based system.

- **Input features**: each `Song` has `genre`, `mood`, `energy`,
  `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
- **User preferences**: each `UserProfile` stores a `favorite_genre`,
  `favorite_mood`, `target_energy`, and a `likes_acoustic` flag.
- **Scoring**: `score_song()` compares a song to the user profile and awards
  points — +2.0 for a genre match, +1.0 for a mood match, and up to +2.0 for
  how close the song's energy is to the user's target energy (closer =
  more points, using `2.0 * (1 - |energy_gap|)`).
- **Ranking**: `recommend_songs()` scores every song in the catalog, then
  sorts the results from highest to lowest score and returns the top `k`.

Data flow: **Input (User Prefs) → Process (score every song in the CSV) →
Output (top K ranked recommendations with reasons)**.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

```
Loaded songs: 20

=== Profile: High-Energy Pop ({'genre': 'pop', 'mood': 'happy', 'energy': 0.85}) ===

Sunrise City - Score: 4.94
Because: genre match (pop) +2.0; mood match (happy) +1.0; energy closeness (target 0.85) +1.94

Gym Hero - Score: 3.84
Because: genre match (pop) +2.0; energy closeness (target 0.85) +1.84

City Lights Run - Score: 2.90
Because: mood match (happy) +1.0; energy closeness (target 0.85) +1.9

=== Profile: Chill Lofi ({'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}) ===

Library Rain - Score: 5.00
Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy closeness (target 0.35) +2.0

Lofi Sunset - Score: 4.94
Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy closeness (target 0.35) +1.94

=== Profile: Deep Intense Rock ({'genre': 'rock', 'mood': 'intense', 'energy': 0.9}) ===

Storm Runner - Score: 4.98
Because: genre match (rock) +2.0; mood match (intense) +1.0; energy closeness (target 0.9) +1.98

Warrior Anthem - Score: 4.96
Because: genre match (rock) +2.0; mood match (intense) +1.0; energy closeness (target 0.9) +1.96
```

(Full output for all three profiles and all five recommendations is in
`model_card.md` under Evaluation.)

---

## Experiments You Tried

- **Weight shift**: doubling the energy weight (from 2.0 max to 4.0 max)
  while halving the genre weight (from 2.0 to 1.0) made energy the dominant
  signal — songs with the right vibe but wrong genre started outranking
  genre-correct songs with mismatched energy. This showed how sensitive the
  final ranking is to weight choices, not just to the underlying data.
- **Feature removal**: temporarily removing the mood check collapsed ties
  between songs that only differed by mood, meaning genre + energy alone
  weren't always enough to separate similar songs in the same genre.

---

## Limitations and Risks

- The catalog only has 20 songs, so recommendations for niche profiles
  (e.g., "sad country") have very few real candidates to draw from.
- The system has no concept of lyrics, cultural context, or listening
  history — it only reasons about numeric/categorical attributes.
- It may over-favor genres that are better represented in the dataset
  (pop, lofi, and synthwave each have more entries than jazz or country).

See `model_card.md` for a deeper breakdown of bias and evaluation.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made it clear how much a recommender's "personality" is just
the weights a designer chose — the same catalog can feel very different
depending on whether genre or energy is prioritized. It also showed how
easily a system can develop blind spots for underrepresented categories in
its dataset, without ever being explicitly programmed to be "unfair."