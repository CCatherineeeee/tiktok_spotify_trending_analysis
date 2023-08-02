#!/bin/sh
python3 ~/song_ranking/spotify_ingestion.py
sleep 10
dt=$(date '+%Y%m%d')
aws s3 cp ~/song_ranking/output_df/spotify_trending.csv s3://spotify-billboard-try/data/ranking_database/spotify_csv/dataload=$dt/spotify_trending.csv
aws s3 cp ~/song_ranking/output_df/billboard_hot_100.csv s3://spotify-billboard-try/data/ranking_database/billboard_csv/dataload=$dt/billboard_hot_100.csv