# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder generates song recommendations for a single user based on a
stated taste profile (favorite genre, favorite mood, and a target energy
level). It assumes the user already knows roughly what they want ("I want
something chill and low-energy") rather than trying to infer taste from
listening history. This is a classroom simulation, not a production system —
it's meant to illustrate how content-based recommenders work, not to
recommend real music to real users at scale.

---

## 3. How the Model Works

Every song in the catalog is compared against the user's profile and given
points for how well it matches:

- A matching genre is worth the most points, since genre is usually the
  strongest signal of "this is my kind of music."
- A matching mood adds a smaller bonus.
- Energy is scored on a sliding scale — the closer a song's energy is to
  what the user asked for, the more points it earns, even if the genre or
  mood don't match exactly.

All songs get scored this way, then they're sorted from highest to lowest
score, and the top 5 are shown to the user along with a plain-language
reason for each one's score (e.g., "genre match +2.0; energy closeness
+1.9").

---

## 4. Data

- **Catalog size**: 20 songs.
- **Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie
  pop, folk, edm, and country.
- **Moods represented**: happy, chill, intense, relaxed, moody, focused,
  sad.
- **Attributes per song**: genre, mood, energy, tempo_bpm, valence,
  danceability, acousticness.
- The original starter set had 10 songs; 10 more were added to broaden
  genre and mood coverage (adding sad, relaxed, and edm songs that weren't
  present before).
- Missing from the dataset: any notion of lyrics, language, artist
  popularity, or release year — all things real platforms often use.

---

## 5. Strengths

- Performs well for users with a clear, singular taste — e.g., a
  "Chill Lofi" profile reliably surfaces the three lofi tracks in the
  catalog at the top of the list.
- The reason strings make the scoring transparent — a user can see exactly
  why a song was picked, not just that it was picked.
- Handles partial matches gracefully: a song that only matches on energy
  still gets a reasonable score instead of being excluded entirely.

---

## 6. Limitations and Bias

The system currently over-relies on genre as the single strongest signal,
which means it can miss songs that would actually suit a user's mood or
energy needs just because the genre label doesn't match exactly (e.g., a
high-energy synthwave track might genuinely fit an "intense rock" listener
better than a low-energy rock track does, but the rock track still outranks
it). The dataset is also small and unevenly distributed across genres —
pop, lofi, and synthwave each have more entries than jazz, folk, or
country — so recommendations for underrepresented genres have fewer real
candidates to draw from and may feel repetitive. Because the scoring is
purely additive, a song can also rack up a high score from mood and energy
alone even with zero genre relevance, which can occasionally push a
tangential song ("Gym Hero," a pop/intense track) into the top results for
very different profiles just because it's high-energy.

---

## 7. Evaluation

Three profiles were tested:

**High-Energy Pop** (`genre=pop, mood=happy, energy=0.85`)
```
Sunrise City - Score: 4.94
Because: genre match (pop) +2.0; mood match (happy) +1.0; energy closeness (target 0.85) +1.94

Gym Hero - Score: 3.84
Because: genre match (pop) +2.0; energy closeness (target 0.85) +1.84

City Lights Run - Score: 2.90
Because: mood match (happy) +1.0; energy closeness (target 0.85) +1.9

Rooftop Lights - Score: 2.82
Because: mood match (happy) +1.0; energy closeness (target 0.85) +1.82

Golden Hour - Score: 2.66
Because: mood match (happy) +1.0; energy closeness (target 0.85) +1.66
```

**Chill Lofi** (`genre=lofi, mood=chill, energy=0.35`)
```
Library Rain - Score: 5.00
Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy closeness (target 0.35) +2.0

Lofi Sunset - Score: 4.94
Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy closeness (target 0.35) +1.94

Midnight Coding - Score: 4.86
Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy closeness (target 0.35) +1.86

Focus Flow - Score: 3.90
Because: genre match (lofi) +2.0; energy closeness (target 0.35) +1.9

Spacewalk Thoughts - Score: 2.86
Because: mood match (chill) +1.0; energy closeness (target 0.35) +1.86
```

**Deep Intense Rock** (`genre=rock, mood=intense, energy=0.9`)
```
Storm Runner - Score: 4.98
Because: genre match (rock) +2.0; mood match (intense) +1.0; energy closeness (target 0.9) +1.98

Warrior Anthem - Score: 4.96
Because: genre match (rock) +2.0; mood match (intense) +1.0; energy closeness (target 0.9) +1.96

Gym Hero - Score: 2.94
Because: mood match (intense) +1.0; energy closeness (target 0.9) +1.94

Bass Drop Riot - Score: 2.86
Because: mood match (intense) +1.0; energy closeness (target 0.9) +1.86

Sunrise City - Score: 1.84
Because: energy closeness (target 0.9) +1.84
```

**Comparing the profiles**: the Pop and Rock profiles both put "Gym Hero"
in their top 5, even though it's a pop song, not a rock song — its very
high energy (0.93) and intense mood are enough to overcome the missing
genre match. The EDM-adjacent high-energy tracks tend to surface for any
high-energy profile regardless of genre, while the Chill Lofi profile is
much more genre-locked — its top 3 results are all literally tagged
"lofi," showing that when a user's target energy is low, energy and genre
tend to agree more often in this dataset (most low-energy songs happen to
already be lofi/ambient/jazz).

What surprised us: the additive scoring means a song never fully drops out
just for missing one criterion — it just falls lower in the ranking. This
is different from a filter (which would exclude non-matches entirely) and
explains why songs like "Gym Hero" or "Sunrise City" can appear across
very different profiles.

---

## 8. Future Work

- Add a **diversity penalty** so the same artist or genre can't dominate
  the top 5 (e.g., "Gym Hero" repeatedly appearing across unrelated
  profiles).
- Weight genre and mood adaptively based on how "specific" a user's stated
  preferences are, instead of using fixed point values for everyone.
- Incorporate more attributes (popularity, release decade, detailed mood
  tags) to reduce reliance on the single genre/mood fields.

---

## 9. Personal Reflection

The biggest learning moment was seeing how much a recommender's behavior
comes down to a handful of weight choices — genre worth 2.0 vs. energy
worth up to 2.0 isn't a "correct" answer, it's a design decision, and
changing it visibly reshaped the rankings during the weight-shift
experiment. Using an AI assistant helped speed up boilerplate like CSV
loading and let me focus on the scoring logic itself, but I had to
double-check the energy-closeness formula by hand to make sure it actually
rewarded closeness rather than just penalizing distance in a confusing way.
What surprised me most is how "smart" a purely additive point system can
feel even though there's no learning or personalization happening at
all — it's just arithmetic over labeled data, which is a useful reminder
that a recommendation "feeling right" doesn't always mean the system
understands anything about music.