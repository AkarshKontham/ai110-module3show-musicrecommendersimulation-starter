"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard taste profiles
# ---------------------------------------------------------------------------

CHILL_LISTENER = {
    "genre":          "lofi",
    "mood":           "chill",
    "energy":         0.38,
    "valence":        0.60,
    "likes_acoustic": True,
}

WORKOUT_FAN = {
    "genre":          "rock",
    "mood":           "intense",
    "energy":         0.90,
    "valence":        0.65,
    "likes_acoustic": False,
}

WEEKEND_DRIVER = {
    "genre":          "pop",
    "mood":           "happy",
    "energy":         0.78,
    "valence":        0.80,
    "likes_acoustic": False,
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
#
# CONFLICTED_SOUL  — energy=0.9 (gym-level) + mood="sad" + likes_acoustic=True.
#   Contradiction: high-energy songs are almost never acoustic or sad.
#   Expected: scorer can't satisfy all three; genre & mood mismatches pile up.
#
# GENRE_GHOST      — genre="country" does not exist in the catalog at all.
#   Expected: every song scores 0 on genre (+2.0 is always missing); the
#   energy/valence/acousticness components alone decide the ranking.
#
# THE_MAXIMIZER    — every numeric preference pushed to its ceiling.
#   energy=1.0, valence=1.0, likes_acoustic=False, genre="edm", mood="euphoric".
#   Expected: "Drop the World" should dominate; tests that the scorer doesn't
#   overflow or produce NaN at boundary values.
# ---------------------------------------------------------------------------

CONFLICTED_SOUL = {
    "genre":          "lofi",
    "mood":           "sad",
    "energy":         0.90,   # wants lofi but also gym-level intensity
    "valence":        0.20,   # very negative emotional tone
    "likes_acoustic": True,   # wants organic texture despite high energy
}

GENRE_GHOST = {
    "genre":          "country",   # absent from catalog — genre bonus always 0
    "mood":           "nostalgic",
    "energy":         0.35,
    "valence":        0.60,
    "likes_acoustic": True,
}

THE_MAXIMIZER = {
    "genre":          "edm",
    "mood":           "euphoric",
    "energy":         1.00,   # ceiling value
    "valence":        1.00,   # ceiling value
    "likes_acoustic": False,
}

# ---------------------------------------------------------------------------
# All profiles to run, in display order
# ---------------------------------------------------------------------------

PROFILES = [
    ("High-Energy Pop",       WEEKEND_DRIVER),
    ("Chill Lofi",            CHILL_LISTENER),
    ("Deep Intense Rock",     WORKOUT_FAN),
    ("Conflicted Soul",       CONFLICTED_SOUL),   # adversarial
    ("Genre Ghost",           GENRE_GHOST),        # adversarial
    ("The Maximizer",         THE_MAXIMIZER),      # adversarial
]

MAX_SCORE = 5.5
WIDTH     = 62


def _print_profile(name: str, prefs: dict, songs: list) -> None:
    print()
    print("=" * WIDTH)
    print(f"  Music Recommender  |  {name}")
    print(f"  genre: {prefs['genre']}"
          f"  |  mood: {prefs['mood']}"
          f"  |  energy: {prefs['energy']}"
          f"  |  valence: {prefs['valence']}")
    print(f"  catalog: {len(songs)} songs  |  showing top 5")
    print("=" * WIDTH)

    recommendations = recommend_songs(prefs, songs, k=5)

    print()
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        title_line = f"  #{rank}  {song['title']}  by  {song['artist']}"
        meta       = f"[{song['genre']} / {song['mood']}]"
        score_str  = f"Score: {score:.2f} / {MAX_SCORE}"

        print(title_line)
        print(f"       {meta:<28} {score_str}")
        for reason in reasons:
            print(f"       > {reason}")
        print("-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    for name, prefs in PROFILES:
        _print_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
