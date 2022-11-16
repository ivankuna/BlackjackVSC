import random
from time import sleep
import database as db



delay = 0.1

# klasa "Cards":
# dijeli karte i ispisuje ih
class Cards:
    def __init__(self, who):
        self.who = who
        self.hand = [], []

    cards = (2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A")

    dict = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11
    }

    def deal(self, show_first_card):
        new_card = str(random.choice(self.cards))
        new_value = self.dict[new_card]

        self.hand[0].append(new_card)
        self.hand[1].append(new_value)

        if "A" in self.hand[0] and sum(self.hand[1]) > 21:
            while sum(self.hand[1]) > 21 and 11 in self.hand[1]:
                self.hand[1].remove(11)
                self.hand[1].insert(0, 1)

        if show_first_card:
            print("\n" + self.who + "s hand:\n" + ", ".join(str(e) for e in self.hand[0]) + f" ({sum(self.hand[1])})")
        else:
            if len(self.hand[0]) == 1:
                print("\n" + self.who + "s hand:\n X")
            else:
                print("\n" + self.who + "s hand:\nX, " + ", ".join(str(e) for e in self.hand[0][1:]))
    
    def show_outcome(self):
        print("\n" + self.who + "s hand:\n" + ", ".join(str(e) for e in self.hand[0]) + f" ({sum(self.hand[1])})")

    def return_outcome(self):
        return str(", ".join(str(e) for e in self.hand[0]) + f" ({sum(self.hand[1])})")

# klasa "Betting"
# računa ukupni iznos "buy in-a" i barata okladama
class Betting(Cards):
    def __init__(self, balance):
        self.balance = balance
        self.game_result = ""

    def betting(self, bet):
        self.balance -= int(bet)

    def lose(self):
        self.game_result = "Dealer win"

    def push(self, bet):
        self.game_result = "Push"
        self.balance += bet

    def win(self, bet):
        self.game_result = "Player win"
        self.balance += (bet * 2)

    def print_balance(self, temp_buy_in):
        print(f"\nOld balance is: {str(temp_buy_in)}")
        print(f"\nNew balance is: {self.balance}")
        

def blackjack():    
    # petlja za upis uloga
    while True:
        try:
            buy_in = int(input("Buy in: "))
            temp_buy_in = buy_in
            game = Betting(buy_in)
            break
        except Exception as e:
            print(e)

    # glavna petlja ruke
    while True:

        # petlja za upis "bet-a" manjeg ili jednakog balansu
        while True:

            # petlja za ispravan upis "bet-a"
            while True:
                try:
                    bet = int(input("\nTake a bet: "))
                    break
                except Exception as e:
                    print(e)

            if bet > 0:
                if int(bet) <= game.balance:
                    game.betting(bet)
                    break
                else:
                    print(f"\nCan't bet higher than balance!\nPlayer balance is: {game.balance}")
            else:
                print("Bet must be larger than zero!")

        # kreiraju se objekti "player" i "dealer"
        player = Cards("Player")
        dealer = Cards("Dealer")

        # dijele se prve dvije karte
        for i in range(2):
            player.deal(True)
            sleep(delay)
            dealer.deal(False)
            sleep(delay)

        # provjerava se "BlackJack"
        if sum(player.hand[1]) == 21 and sum(dealer.hand[1]) == 21:
            sleep(delay)
            print("\nBoth the dealer and the player have Blackjack! Player is pushed!")
            game.push(bet)
        elif sum(player.hand[1]) == 21:
            sleep(delay)
            print("\nBlackjack!")
            game.win(bet)
        elif sum(dealer.hand[1]) == 21:
            sleep(delay)
            print("\nThe dealer has Blackjack! You lose!")
            game.lose()
        else:
            # igra player
            # petlja samo za ruku koja se igra
            while True:  
                sleep(delay)
                print("\n1 - Hit"
                    "\n2 - Stand\n")

                play = input("> ")

                if play == "1":
                    sleep(delay)
                    player.deal(True)
                    if sum(player.hand[1]) > 21:
                        sleep(delay)
                        print("\nBust!\n")
                        game.lose()
                        break
                elif play == "2":
                    sleep(delay)
                    print(f"\nStand. Your hands total is: {sum(player.hand[1])}\n")
                    break

            if sum(player.hand[1]) <= 21:
                # ispisuju prve dvije karte dealera
                sleep(delay)
                print("\n" + "Dealers hand:\n" + ", ".join(str(e) for e in dealer.hand[0]) + f" ({sum(dealer.hand[1])})")
                # igra dealer
                while True:
                    if sum(dealer.hand[1]) < 17:
                        sleep(delay)
                        dealer.deal(True)
                    elif 17 <= sum(dealer.hand[1]) <= 21:
                        if sum(dealer.hand[1]) < sum(player.hand[1]):
                            sleep(delay)
                            print(f"\nThe dealer has {sum(dealer.hand[1])}. You win!")
                            game.win(bet)
                            break
                        elif sum(dealer.hand[1]) > sum(player.hand[1]):
                            sleep(delay)
                            print(f"\nThe dealer has {sum(dealer.hand[1])}. You lose!")
                            game.lose()
                            break
                        elif sum(dealer.hand[1]) == sum(player.hand[1]):
                            sleep(delay)
                            print(f"\nThe dealer has {sum(dealer.hand[1])}. Player is pushed!")
                            game.push(bet)
                            break
                    elif sum(dealer.hand[1]) > 21:
                        sleep(delay)
                        print("\nThe dealer has bust. You win!")
                        game.win(bet)
                        break
            elif sum(player.hand[1]) == 21:
                print("")

        print("\n")
        player.show_outcome()
        dealer.show_outcome()        
        print(f"\n{game.game_result}")
        game.print_balance(temp_buy_in)
        
        # upis zapisa u bazu podataka (povijest)
        game_record = ("Blak Jack",  player.return_outcome(), dealer.return_outcome(), game.game_result, temp_buy_in, bet, game.balance)
        db.insert_record(game_record)
        
        # reset originalnog ukupnog iznosa
        temp_buy_in = game.balance

        # ako je ukupni iznos ("balance") = nula
        if game.balance == 0:
            print("\nOut of funds!")
            break
        else:
            kraj_igre = False
            vrti_se = True
            while vrti_se:
                print("\n1 - Bet"
                    "\n2 - Quit\n")
                play = input("> ")

                if play == "1":
                    vrti_se = False
                elif play == "2":
                    kraj_igre = True
                    break
                else:
                    print("Invalid input!")
        if kraj_igre:
            break

    print("\nGame over!")
