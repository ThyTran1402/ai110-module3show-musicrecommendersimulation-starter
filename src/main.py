"""
Command-line runner for the Music Recommender Simulation.

Defines three test user profiles and prints ranked recommendations
with scores and reasons for each profile.
"""

from .recommender import load_songs, recommend_songs


PROFILES = {
    "Happy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
    },
    "High-Energy Metal Head": {
        "genre": "metal",
        "mood": "intense",
        "energy": 0.95,
    },
}


def print_recommendations(profile_name: str, recommendations: list) -> None:
    """Print a formatted block of recommendations for one user profile."""
    separator = "-" * 50
    print(f"\n{'=' * 50}")
    print(f"  Profile: {profile_name}")
    print(f"{'=' * 50}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"      Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"      Score : {score:.2f}")
        print(f"      Why   : {explanation}")
    print(separator)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print()

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recommendations)


if __name__ == "__main__":
    main()
