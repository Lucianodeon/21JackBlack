import random
print("WELCOME TO JACK BLACK... I MEAN BlackJack!")
class Card:                                                                                                  #card class

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def __repr__(self):
        return " of ".join((self.value, self.suit))

class Deck:                                                                                                 #Deck class with the 52 cards

    def __init__(self):
        self.cards = [Card(suit,value)
         for suit in ["Clubs","Diamonds", "Hearts", "Spades"]
         for value in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
         ]

    def shuffle(self):                                                                                   #Shuffle mixes the array deck with the random function
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):                                                                                      #Takes the cards from the deck and at the end of the game does not go back.... we can count the cards!
        if len(self.cards) > 1:
            return self.cards.pop(0)

class Hand:                                                                                              #The cards on hand, I decided to not hide the dealer's hand for more easiness, so we can follow the game quickly
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "Ace":
                    has_ace = True
                    self.value += 11
                else:                                                                                   #if is a figure
                    self.value+= 10

        if has_ace and self.value > 21:
            self.value -=10                                                                             #The ace can be 1 or 11, so if the value of the ace being 11 surpass 21 will become 1

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):                                                                                  #show the cards we have on hand
        for card in self.cards:
            print(card)
        print("Value:", self.get_value())

class Game:
    def __init__(self):
        self.win = 0
        self.lost = 0
        self.tie = 0

    def play(self):
        playing = True

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for i in range(2):          #picks the first 2 cards
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display()
            print()

            game_over = False

            while not game_over:                                                                                              #checks for black jack in the first 2 cards
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results( player_has_blackjack, dealer_has_blackjack)
                    continue

                choice = input("Please choose [Hit/ Stick]").lower()                                                    #Ask you if you want to take a card, but if the dealer is below 17 he needs to take anyways.
                print()
                while choice not in ["h", "s" ,"hit","stick"]:
                    choice = input("Please enter 'hit' or 'stick' (H or S)").lower()
                if self.check_for_dealer():
                    self.dealer_hand.add_card(self.deck.deal())

                if choice in ['hit', 'h']:
                    self.player_hand.add_card(self.deck.deal())
                    print("Now your hand is:")
                    self.player_hand.display()
                    print("Now the dealer's hand is:")
                    self.dealer_hand.display()



                    if self.player_is_over():
                        print("You have lost!")
                        print()
                        self.lost += 1
                        game_over = True
                    if self.dealer_is_over():
                        print("You Win!, The Dealer went over")
                        print()
                        self.win += 1
                        game_over = True


                else:

                    if self.check_for_dealer():
                        self.dealer_hand.add_card(self.deck.deal())

                    player_hand_value = self.player_hand.get_value()
                    dealer_hand_value = self.dealer_hand.get_value()


                    print("Final Results")
                    print("Your Hand:", player_hand_value)
                    print()
                    print("Dealer's Hand:", dealer_hand_value)

                    if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                        print("You Win!")
                        self.win += 1
                        print()
                    elif player_hand_value == dealer_hand_value:
                        print("Draw")
                        self.tie += 1

                    else:
                        print("You Lose!")
                        self.lost += 1
                        print()
                    game_over = True


            print("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display()
            print("Summary:")
            print("Games Won",self.win)
            print("Games Lost",self.lost)
            print("Games finished in Tie",self.tie)
            print()
            again = input ("Do you want to Play Again? [Y/N]").lower()
            print()
            while again  not in ["y", "n" , "yes", "no"]:
                again = input ("Please enter Yes or No (Y/N)").lower()
            if again in ["no", "n"]:
                print("Thanks for Playing 21 JackBlack or 21 BlackJack")
                playing = False
            else:
                game_over = False



    def player_is_over(self):
        return self.player_hand.get_value() > 21

    def check_for_dealer(self):                                                                                   #Checks if the dealer gets 17 or more
        return self.dealer_hand.get_value() < 17

    def dealer_is_over(self):
        return self.dealer_hand.get_value() > 21


    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True
        return player, dealer





    def show_blackjack_results (self, player_has_blackjack , dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            self.tie += 1
            print(" Draw! Both have BlackJack!")

        elif player_has_blackjack:
            self.win += 1
            print ("You have BlackJack! You win!")

        elif dealer_has_blackjack:
            self.lost += 1
            print("Dealer has BlackJack! You Lose!")



if __name__ == '__main__':
    game = Game()
    game.play()
