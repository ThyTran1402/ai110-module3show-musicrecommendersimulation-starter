import csv
from typing import List, Dict, Tuple
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
    """OOP wrapper around the scoring logic; required by tests."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric match score between a UserProfile and a Song."""
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        energy_gap = abs(song.energy - user.target_energy)
        score += 1.0 - energy_gap
        if user.likes_acoustic and song.acousticness >= 0.7:
            score += 0.5
        return round(score, 2)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Songs sorted by descending match score."""
        scored = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"genre match ({song.genre})")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"mood match ({song.mood})")
        energy_gap = abs(song.energy - user.target_energy)
        reasons.append(f"energy similarity ({1.0 - energy_gap:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.7:
            reasons.append("acoustic bonus (+0.5)")
        return ", ".join(reasons) if reasons else "No strong match found."


# ---------------------------------------------------------------------------
# Functional interface used by src/main.py
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons).

    Algorithm Recipe
    ----------------
    +2.0  genre match
    +1.0  mood match
    +0–1  energy similarity  (1.0 minus the absolute distance from target)
    """
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = float(user_prefs.get("energy", 0.5))
    energy_gap = abs(float(song["energy"]) - target_energy)
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    return round(score, 2), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, return the top k results.

    Each result is a tuple of (song_dict, score, explanation_string).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
