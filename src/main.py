"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Taste profiles
# Each dict maps to the keys score_song() recognises:
#   genre, mood, energy, valence, likes_acoustic
#
# Three contrasting profiles are defined so the recommender's ability to
# differentiate is easy to observe:
#
#   CHILL_LISTENER  — low energy, acoustic, chill mood
#   WORKOUT_FAN     — high energy, electronic, intense mood
#   WEEKEND_DRIVER  — mid-high energy, upbeat, no strong acoustic preference
#
# CHILL_LISTENER and WORKOUT_FAN should produce near-inverted rankings for
# extreme songs like "Library Rain" vs "Shatter the Glass".
# ---------------------------------------------------------------------------

CHILL_LISTENER = {
    "genre":         "lofi",
    "mood":          "chill",
    "energy":        0.38,   # targets the lofi cluster (0.35–0.42)
    "valence":       0.60,   # neutral-to-warm; not seeking euphoria
    "likes_acoustic": True,  # prefers organic, unplugged texture
}

WORKOUT_FAN = {
    "genre":         "rock",
    "mood":          "intense",
    "energy":        0.90,   # targets the high-energy cluster (0.91–0.97)
    "valence":       0.65,   # pumped up but not melancholic
    "likes_acoustic": False, # prefers polished, high-production sound
}

WEEKEND_DRIVER = {
    "genre":         "pop",
    "mood":          "happy",
    "energy":        0.78,   # upbeat but not gym-level
    "valence":       0.80,   # bright and positive
    "likes_acoustic": False,
}

ACTIVE_PROFILE = WEEKEND_DRIVER   # ← swap this to test different profiles

MAX_SCORE = 5.5
WIDTH     = 62


def main() -> None:
    songs = load_songs("data/songs.csv")

    profile_name = {
        id(CHILL_LISTENER):  "Late Night Chill",
        id(WORKOUT_FAN):     "Workout Intensity",
        id(WEEKEND_DRIVER):  "Weekend Driver",
    }.get(id(ACTIVE_PROFILE), "Custom Profile")

    # ── header ──────────────────────────────────────────────
    print()
    print("=" * WIDTH)
    print(f"  Music Recommender  |  {profile_name}")
    print(f"  genre: {ACTIVE_PROFILE['genre']}"
          f"  |  mood: {ACTIVE_PROFILE['mood']}"
          f"  |  energy: {ACTIVE_PROFILE['energy']}"
          f"  |  valence: {ACTIVE_PROFILE['valence']}")
    print(f"  catalog: {len(songs)} songs  |  showing top 5")
    print("=" * WIDTH)

    recommendations = recommend_songs(ACTIVE_PROFILE, songs, k=5)

    # ── results ─────────────────────────────────────────────
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


if __name__ == "__main__":
    main()
