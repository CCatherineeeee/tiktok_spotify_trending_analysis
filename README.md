# Spotify & Billboard ranking Correlation Analysis with AWS Glue

## Objective
- Build a ETL pipeline to automatically collect daily song ranking on Spotify and Billboard
- Compare the difference of rankings on two different board
- Provide Business Insights: Whether promoting on Spotify could effectively raise billboard ranking

## Description / Functionality of Files
### spotify_ingestion.py:
- Create Spotify API connection and create access token
- Spotify Ingestion Class:
  - Since the project needs to retrieve data from two playlists, create and utilize this class to avoid duplicate coding.
  - Instance variable include playlist_id, market, fields, limit, offset, which are required by Spotify API to retrieve data from corresponding playlists
  - Check the credibility of data: if no data is collected, if there exist Null entry, if song_id (primary key) has duplicatation, etc
  - After collecting data, store them into csv with Pandas library
- Create Spotify Ingestion Class objects in order to collect data from two different playlists
### billboard_hot_100.csv & spotify_trending.csv
- CSV file format of data collected from spotify_ingestion.py (demonstration purpose)
### ec2_shell.sh
- The Bash shell script to run on EC2 instance for automated data collection and S3 upload of the two csv file
- Need to SSH + SCP spotify_ingestion.py python file (and this shell script of course) onto EC2 instance
  - *SSH + SCP process requires AWS key pair for credential, for security purpose they are not stored in this github repo*

## ETL Pipeline Layer
- After the data collection step, use AWS Glue (Data Catalog, Glue crawler, Glue job) to build the ETL pipeline
- Store output result in different S3 bucket
