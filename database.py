import os
import sqlite3


def open_database(): 
    if os.path.exists("games.db"):
        connection = sqlite3.connect("games.db")
        cursor = connection.cursor()
    else:
        connection = sqlite3.connect("games.db")
        cursor = connection.cursor()
        cursor.execute(
            "create table game_history (Game text, PlayerHand text, DealerHand text, GameResult text, OldBalance integer, Bet integer, NewBalance integer)")
        connection.commit()


def insert_record(record_list):
    connection = sqlite3.connect("games.db")
    cursor = connection.cursor()
    cursor.execute("insert into game_history values (?,?,?,?,?,?,?)", record_list)
    connection.commit()


def show_database():
    connection = sqlite3.connect("games.db")
    cursor = connection.cursor()
    for row in cursor.execute("select * from game_history"):
        print(row)
