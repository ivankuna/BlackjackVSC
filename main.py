import os
import blackJack as bj
import database as db

os.system('cls')
db.open_database()
bj.blackjack() 
db.show_database()

