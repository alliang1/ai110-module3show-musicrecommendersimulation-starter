import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the scoring/ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"genre match ({song.genre}) +2.0")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append(f"mood match ({song.mood}) +1.0")

        energy_gap = abs(song.energy - user.target_energy)
        energy_points = round(2.0 * (1 - energy_gap), 2)
        if energy_points > 0:
            score += energy_points
            reasons.append(f"energy closeness +{energy_points}")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
            reasons.append("high acousticness +0.5")

        return round(score, 2), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return "; ".join(reasons) if reasons else "no strong matches"


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Recipe: +2.0 genre match, +1.0 mood match, up to +2.0 for energy closeness.
    """
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_gap = abs(song["energy"] - target_energy)
        energy_points = round(2.0 * (1 - energy_gap), 2)
        if energy_points > 0:
            score += energy_points
            reasons.append(f"energy closeness (target {target_energy}) +{energy_points}")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, ranks them, and returns the top k as (song, score, explanation).
    """
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        results.append((song, score, explanation))

    results.sort(key=lambda item: item[1], reverse=True)
    return results[:k]