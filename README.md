# Relational Database Fundamentals: Tournament Results
Project 2 of the Full Stack Development Nanodegree of Udacity
 
 In this repository you will find the scripts developed during the fantastic Udacity training 
[Relational Databases Fundamentals](https://www.udacity.com/course/viewer#!/c-ud197-nd)


* **Project Tournament Results**: You will develop a database schema to store the game matches between players. You will then write code to query this data and determine the winners of various games.
* 

Launch the Vagrant VM

```
vagrant up
vagrant ssh
```

Create the database:
```
psql create database tournament
```

Create the tables in the database:
```
psql \i tournament.sql
```

To test the code, run:

```
python tournament_test.py
```

