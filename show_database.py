import sqlite3
import os

os.system('cls')


connection = sqlite3.connect("games.db")
cursor = connection.cursor()

# game history
print("select * from table:\n")
records = cursor.execute("select * from game_history")
names = [description[0] for description in cursor.description]
print(names)
for row in records:
    print(row)

# statistics
print("\n")
print("statistika:\n")
record = []
for row in cursor.execute("select gameresult,count(*) from game_history group by gameresult order by count(*)"):
    record.append(row)
    print(row)

print("\n")
print("lista:\n")
print(record)
print("\n")

connection.close()