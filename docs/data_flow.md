# Music Recommender — Data Flow

```mermaid
flowchart TD
    A["User Profile\ngenre · mood · energy · valence · likes_acoustic"]
    B[("songs.csv\n20 rows")]

    B --> LOAD["load_songs()"]
    LOAD --> SONGS["List of song dicts"]
    A --> RS
    SONGS --> RS["recommend_songs(user_prefs, songs, k=5)"]

    RS --> LOOP(["For each song in list"])

    LOOP --> SCORE["score_song(user_prefs, song)"]

    SCORE --> G{"genre match?"}
    G -- yes --> G2["+ 2.0"]
    G -- no  --> G3["+ 0.0"]

    G2 & G3 --> M{"mood match?"}
    M -- yes --> M2["+ 1.5"]
    M -- no  --> M3["+ 0.0"]

    M2 & M3 --> E["energy similarity\n(1 − |target − song|) × 1.0\n→ +0.0 to +1.0"]

    E --> V["valence similarity\n(1 − |target − song|) × 0.5\n→ +0.0 to +0.5"]

    V --> AC{"likes_acoustic\naligns with acousticness?"}
    AC -- yes --> AC2["+ 0.5"]
    AC -- no  --> AC3["+ 0.0"]

    AC2 & AC3 --> SUM["total score\n(max 5.5)"]

    SUM --> NEXT{"more songs?"}
    NEXT -- yes --> LOOP
    NEXT -- no  --> SORT["sort all scored songs\ndescending by score"]

    SORT --> TOPK["slice top k = 5"]
    TOPK --> OUT["Output\ntitle · artist · score · explanation"]
```

## Scoring weights

| Feature | Points | Type |
|---|---|---|
| Genre match | +2.0 | fixed bonus |
| Mood match | +1.5 | fixed bonus |
| Energy similarity | +0.0 – 1.0 | `(1 − \|target − song\|) × 1.0` |
| Valence similarity | +0.0 – 0.5 | `(1 − \|target − song\|) × 0.5` |
| Acousticness alignment | +0.5 | fixed bonus |
| **Max total** | **5.5** | |
