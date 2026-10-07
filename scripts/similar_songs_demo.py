import pandas as pd


# these are the sound details we'll compare
features = [
    "Danceability",
    "Energy",
    "Acousticness",
    "Valence",
    "Tempo",
    "Loudness",
]

df = pd.read_csv("../cleaned_dataset.csv")

# skip tracks missing one of these values
songs = df.dropna(subset=features + ["Artist", "Track"]).reset_index(drop=True)

# put each sound detail on the same scale so tempo doesn't overpower the others
scaled_features = (songs[features] - songs[features].min()) / (
    songs[features].max() - songs[features].min()
)


def recommend_songs(artist_name, track_name, number=5):
    matches = songs[
        (songs["Artist"].str.lower() == artist_name.lower())
        & (songs["Track"].str.lower() == track_name.lower())
    ]

    if matches.empty:
        print("couldn't find that song. check the artist and track name.")
        return

    # compare every track with the song we picked; a smaller distance means a closer match
    song = matches.iloc[0]
    song_number = matches.index[0]
    distances = ((scaled_features - scaled_features.iloc[song_number]) ** 2).sum(axis=1) ** 0.5

    recommendations = songs[["Artist", "Track", "Album", "Title"]].copy()
    recommendations["match_percentage"] = 100*(1-distances/distances.max())

    # don't recommend the song we started with, even if it has several artist rows
    recommendations = recommendations[
        (recommendations["Track"] != song["Track"])
        | (recommendations["Album"] != song["Album"])
        | (recommendations["Title"] != song["Title"])
    ]

    # the same song can have one row for each artist in the dataset
    recommendations = recommendations.drop_duplicates(
        subset=["Artist", "Track", "Album", "Title"]
    )
    recommendations = recommendations.groupby(
        ["Track", "Album", "Title"], as_index=False
    ).agg({"Artist": ", ".join, "match_percentage": "min"})

    return recommendations.sort_values("match_percentage", ascending=False).head(number)


if __name__ == "__main__":
    # type a song from the dataset
    artist_name = input("artist name: ").strip()
    track_name = input("song name: ").strip()
    recommendations = recommend_songs(artist_name, track_name)

    if recommendations is not None:
        print(recommendations[["Artist", "Track"]].to_string(index=False))
