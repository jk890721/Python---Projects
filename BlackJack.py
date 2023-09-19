# BlackJack game 
import random

def deal_card():
    deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(deck)
    return card

def calculate_score(two_cards):
    if 11 in two_cards and 10 in two_cards and len(two_cards) == 2:
        return 21
    if 11 in two_cards and sum(two_cards) > 21:
        two_cards.remove(11)
        two_cards.append(1)
    
    return sum(two_cards)


def compare(user_score, computer_score, user_cards, computer_cards):
    if computer_score == 21 and len(computer_cards) == 2:
        return "Lose, Dealer has BlackJack"
    elif user_score == 21 and len(user_cards) == 2:
        return "You win with BlackJack"
    elif user_score == computer_score:
        return "Draw"
    elif user_score > 21:
        return "You busted. Dealer win"
    elif computer_score > 21:
        return "Dealer busted. You win"
    elif user_score > computer_score:
        return "You win"
    else:
        return"Dealer win"

# def split():






def play():
    user_cards = []
    computer_cards = []
    split_cards = []
    is_game_over = False
    do_split = False

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    split_cards.append(deal_card())


    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        split_score = calculate_score(split_cards)
        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")
        if computer_score == 21 and computer_cards == 2 and user_score == 21 and user_cards == 2:
            print("Both got BlackJack, Lucky you two")
        elif computer_score == 21 and computer_cards == 2:
            print("Dealer got BlackJacke, U lose")
            is_game_over = True
        elif user_score == 21 and user_cards == 2:
            print("You got BlackJacke, U win")
            is_game_over = True


        if user_cards[0] == user_cards [1]: 
            do_split = input("Type 'y' to split the card into two hands, and type 'n' to pass: ")
            if do_split == 'y':
                split_cards[0] = user_cards[1]
                user_cards.remove(user_cards[1])
                user_cards.append(deal_card())
                split_cards.append(deal_card())
                user_score = calculate_score(user_cards)
                split_score = calculate_score(split_cards)
                print(f"Your first split cards: {user_cards}, current score: {user_score}")
                print(f"Computer's first card: {computer_cards[0]}")
                user_should_deal = input("Tpye 'y' to get another card for first hand, type 'n' to pass: ")
                if user_should_deal == 'y':
                    user_cards.append(deal_card())
                else:
                    is_game_over = True
                print(f"Your cards: {split_cards}, current score: {split_score}")
                print(f"Computer's first card: {computer_cards[0]}")
                user_should_deal = input("Tpye 'y' to get another card for second hand, type 'n' to pass: ")
                if user_should_deal == 'y':
                    split_cards.append(deal_card())
                else:
                        is_game_over = True
            else:
                    is_game_over = True
        elif user_score > 21:
            is_game_over = True

        else:
            user_should_deal = input("Tpye 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True
        
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"Ure final hand: {user_cards}, final score: {user_score}")
    print(f"Computer final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score, user_cards, computer_cards))

while input("Do u want to play a game of BlackJack? Type 'y' or 'n': ") == "y":
    play()

