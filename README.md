# Spotifind

Spotifind is a music recommendation project. Its Streamlit app recommends songs by audio features, lets users save tracks, and uses saved tracks to estimate which recommendations fit a user's taste.

## Project files

- `cleaned_dataset.csv` contains track metadata, audio features, and Spotify and YouTube engagement data.
- `Spotifind.ipynb` is the group's main project notebook.
- `notebooks/data_audit.ipynb` checks missing values and duplicate tracks and creates charts.
- `scripts/` contains the Streamlit app, recommendation logic, and demo.
- `docs/possible project questions.md` lists project question ideas.
- `docs/similar songs app.md` describes the song picker and recommender.

## Run the app

Install the Python dependencies:

```sh
python -m pip install pandas streamlit scikit-learn sqlalchemy werkzeug
```

From the project folder, start the app from `scripts` so its relative paths can find the dataset:

```sh
cd scripts
streamlit run main.py
```

Create an account or log in, choose an artist and track on the Recommender page, then save tracks you like. Saved tracks are stored per username in the local SQLite database `scripts/my_database.db`. The Saved Songs page lets you remove tracks, and the User Likes page compares a preference model with a random-ranking baseline after at least six saved tracks are available.

## How recommendations work

The recommender drops tracks missing any of nine audio features: danceability, energy, acousticness, valence, tempo, loudness, speechiness, instrumentalness, and liveness. It clips extreme feature values at the 1st and 99th percentiles, z-scores the features, and applies smaller weights to tempo and liveness and a larger weight to loudness. It also adds artist genre tags from `cache.json`, weighted more heavily than individual audio features. The nearest tracks by Euclidean distance are returned, with duplicate track rows combined. The displayed match percentage is a distance-based ranking aid, not a probability that someone will like a song.

The app also scores recommendations against a user's saved tracks with a one-class SVM. The User Likes page repeatedly holds out part of the saved set, ranks the held-out tracks among candidates, and compares their average percentile rank with a random baseline. This is a small-data evaluation, not proof that the model predicts listening preferences reliably.

The current repository does not include `cache.json`; the recommender needs that artist-to-tags JSON file alongside `cleaned_dataset.csv` to start.

## Run the command-line demo

With the same dependencies and `cache.json` in place, run from `scripts`:

```sh
python similar_songs_demo.py
```

Enter an artist and track name as they appear in the dataset. The demo prints the closest tracks.

## Data notes

The CSV appears to be based on the [Spotify and YouTube dataset on Kaggle](https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube). Check the dataset notes for original sources and cite them in the final project. The file includes only the tracks in this dataset, so findings may not generalize to all music.
