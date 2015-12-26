#!/bin/sh

#  import_db.sh
#  
#
#  Created by Farah  Bouassida on 25.11.15.
#
#.tables

sqlite3 /Users/farahbouassida/Documents/MA3/semesterProject/db.sqlite3 <<!

.header on
.mode csv
.once /Users/farahbouassida/Documents/MA3/semesterProject/answers_radio.csv
SELECT * FROM psycho_answerradio;

.once /Users/farahbouassida/Documents/MA3/semesterProject/answers_text.csv
SELECT * FROM psycho_answertext;

.once /Users/farahbouassida/Documents/MA3/semesterProject/questions.csv
SELECT * FROM psycho_question;

.once /Users/farahbouassida/Documents/MA3/semesterProject/users.csv
SELECT * FROM psycho_user;

.once /Users/farahbouassida/Documents/MA3/semesterProject/responses.csv
SELECT * FROM psycho_response;

.once /Users/farahbouassida/Documents/MA3/semesterProject/answer_base.csv
SELECT * FROM psycho_answerbase;

.once /Users/farahbouassida/Documents/MA3/semesterProject/users_activities.csv
SELECT * FROM psycho_useractivity;

.once /Users/farahbouassida/Documents/MA3/semesterProject/activity.csv
SELECT * FROM psycho_activity;

.once /Users/farahbouassida/Documents/MA3/semesterProject/tests.csv
SELECT * FROM psycho_test;