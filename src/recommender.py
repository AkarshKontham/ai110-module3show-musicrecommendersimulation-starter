from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects ranked by score for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language string explaining why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id']           = int(row['id'])
            row['energy']       = float(row['energy'])
            row['tempo_bpm']    = int(row['tempo_bpm'])
            row['valence']      = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (total_score, reason_strings)."""
    score = 0.0
    reasons = []

    # EXPERIMENT: Weight Shift — genre halved (+1.0), energy doubled (up to +2.0).
    # Max score stays 5.5 (1.0 + 1.5 + 2.0 + 0.5 + 0.5).
    # Hypothesis: continuous energy proximity should surface cross-genre songs
    # whose vibe matches better than a genre label alone would predict.

    # Genre match: +1.0 (halved from +2.0)
    if song['genre'] == user_prefs['genre']:
        score += 1.0
        reasons.append("genre match (+1.0)")
    else:
        reasons.append(f"no genre match  (song: {song['genre']}, want: {user_prefs['genre']}) (+0.0)")

    # Mood match: +1.5 (unchanged)
    if song['mood'] == user_prefs['mood']:
        score += 1.5
        reasons.append("mood match (+1.5)")
    else:
        reasons.append(f"no mood match  (song: {song['mood']}, want: {user_prefs['mood']}) (+0.0)")

    # Energy similarity: up to +2.0 (doubled from +1.0)
    # Both values are in [0, 1], so difference is at most 1.0
    energy_points = (1.0 - abs(user_prefs['energy'] - song['energy'])) * 2.0
    score += energy_points
    reasons.append(f"energy similarity  {song['energy']:.2f} vs {user_prefs['energy']:.2f} (+{energy_points:.2f})")

    # Valence similarity: up to +0.5
    valence_points = (1.0 - abs(user_prefs['valence'] - song['valence'])) * 0.5
    score += valence_points
    reasons.append(f"valence similarity  {song['valence']:.2f} vs {user_prefs['valence']:.2f} (+{valence_points:.2f})")

    # Acousticness fit: +0.5
    # likes_acoustic=True rewards high acousticness (>= 0.5); False rewards low (< 0.5)
    acoustic_match = (user_prefs['likes_acoustic'] and song['acousticness'] >= 0.5) or \
                     (not user_prefs['likes_acoustic'] and song['acousticness'] < 0.5)
    if acoustic_match:
        score += 0.5
        reasons.append(f"acousticness fit  {song['acousticness']:.2f} (+0.5)")
    else:
        reasons.append(f"acousticness mismatch  {song['acousticness']:.2f} (+0.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, sort descending, and return the top-k (song, score, reasons) tuples."""
    return sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: item[1],
        reverse=True,
    )[:k]
