from flask import Flask, render_template, request
from Custom_Dataset_of_all_5_card_poker_hands._5Card_PokerHand_Dataset_Generator import evaluate_hand
import csv
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


# Convert a two-character string to a Card object
def string_to_card(card_str):

    rank = card_str[0]
    suit = card_str[1]
    return Card(rank, suit)


# Convert a Card object back to its string representation
def card_to_string(card):
    return card.rank + card.suit


hand_strengths = {}
with open('Custom_Dataset_of_all_5_card_poker_hands/5card_poker_hands.csv', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        hand_strengths[row[0]] = float(row[1])
        # Pre-made dataset took 36.50181007385254 seconds to generate + evaluate all 2,598,960 possible 5 card hand combinations using core i5 10300H @ 2.5GHz, 16GB RAM, 1TB SSD
        # 22.071184396743774 seconds Ryzen 5 7600 @ 3.8Ghz, 16GB RAM, 1TB SSD

two_card_hand_strengths = {}
with open('Custom_Dataset_of_all_2_card_poker_hands/2card_poker_hands.csv', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        two_card_hand_strengths[row[0]] = float(row[1])
        # Pre-made dataset took 0.000997304916381836 seconds to generate + evaluate all 1326 possible 2 card hand combinations.


def card_sort_key(card):
    rank_order = '23456789TJQKA'
    suit_order = 'HDCS'

    # Test Unit for suit and rank errors - uncomment to test
    # try:
    #     rank_index = rank_order.index(card[0])
    # except ValueError:
    #     print(f"Error: Rank '{card[0]}' not found in rank_order.")
    #     rank_index = 0

    # try:
    #     suit_index = suit_order.index(card[1])
    # except ValueError:
    #     print(f"Error: Suit '{card[1]}' not found in suit_order.")
    #     suit_index = 0

    return (rank_order.index(card.rank), suit_order.index(card.suit))


def calculate_percentile(best_strength, hand_strengths):
    less_or_equal_count = sum(
        1 for strength in hand_strengths.values() if strength <= best_strength)
    total_hands = len(hand_strengths)
    percentile = (less_or_equal_count / total_hands) * 100
    return percentile


def calculate_percentile_two_card(hand_key, two_card_strengths):
    best_strength = two_card_strengths[hand_key]
    less_or_equal_count = sum(
        1 for strength in two_card_strengths.values() if strength <= best_strength)
    total_hands = len(two_card_strengths)
    percentile = (less_or_equal_count / total_hands) * 100
    return percentile

# <---------------------------------------------->
# Two different types of combinatorial algorithms
# <---------------------------------------------->


# 1. Combinatorial Algo using a stack to ITERATIVELY create all possible hands using 2 hole cards + table cards,
# then custom dataset hashtable lookup to identify strongest possible handle and calculate percentile.


# This is a custom iterative implementation without using itertools to generate all possible combinations of n cards from the given list of cards.
def all_combinations_iterative(cards, n):
    result = []
    # Stack holds tuples of (index, current_combination), initialized with (0, empty list)
    stack = [(0, [])]

    # while loop continues iteratively as long as there's an item in the stack
    while stack:
        # Pop the last item from the stack
        index, current = stack.pop()

        # If the current combination has n cards, add it to the result list and continue
        if len(current) == n:
            result.append(current)
            continue

        for next_index in range(index, len(cards)):
            # For every remaining card in the list, create a new combination by adding it as the next card.
            new_combination = current + [cards[next_index]]

            # Prepare for the next iteration. The next_index + 1 ensures that in the next iteration,
            # we will be looking at the next card in the list, avoiding repetition of the current card.
            next_iteration_start_index = next_index + 1

            # Add this new combination and the index for the next iteration to the stack.
            stack.append((next_iteration_start_index, new_combination))

    return result


def algorithm1(hand_cards, table_cards=[]):
    start_time = time.perf_counter()
    hand_cards_objects = [string_to_card(card) for card in hand_cards]
    table_cards_objects = [string_to_card(card) for card in table_cards]

    if len(table_cards) < 3:
        sorted_hand = sorted(hand_cards_objects, key=card_sort_key)
        hand_key = ''.join(card_to_string(card) for card in sorted_hand)
        percentile = calculate_percentile_two_card(
            hand_key, two_card_hand_strengths)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return f"Hand: {sorted_hand} \
            \n\n Execution time: {execution_time:.12f} seconds. \
            \n\n Hand strength percentile among all 1,326 possible starting hands: \
            \n{percentile:.4f}%"
    else:
        best_strength = 0
        combined_cards = hand_cards_objects + table_cards_objects
        all_possible_hands = all_combinations_iterative(combined_cards, 5)

        for hand in all_possible_hands:
            sorted_hand = sorted(hand, key=card_sort_key)
            hand_key = ''.join(card_to_string(card) for card in sorted_hand)
            hand_strength = hand_strengths.get(hand_key, 0)
            best_strength = max(best_strength, hand_strength)

        percentile = calculate_percentile(best_strength, hand_strengths)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return f"Hand: {sorted_hand} \
            \n\n Execution time: {execution_time:.12f} seconds.\
            \n\n Hand strength percentile among all 2,598,960 possible 5 card poker hands: \
            \n{percentile:.4f}%"


# <---------------------------------------------->


# 1. Combinatorial Algo to RECURSIVELY create all possible hands using 2 hole cards + table cards,
# then custom dataset hashtable lookup to identify strongest possible handle and calculate percentile.


def all_combinations_recursive(cards, n, start=0, current=[]):
    # base cases
    if len(current) == n:  # If the current combination is n length, return it in a list
        return [current]
    if start == len(cards):  # If the end of the cards list is reached, return an empty list
        return []

    # Recursive call using the next card in the list and including the current card
    include_current = all_combinations_recursive(
        cards, n, start + 1, current + [cards[start]])
    # Recursive call using the next card in the list without including the current card
    exclude_current = all_combinations_recursive(
        cards, n, start + 1, current)

    # Combine the results from both recursive calls
    return include_current + exclude_current


def algorithm2(hand_cards, table_cards=[]):
    start_time = time.perf_counter()

    hand_cards_objects = [string_to_card(card) for card in hand_cards]
    table_cards_objects = [string_to_card(card) for card in table_cards]

    if len(table_cards) < 3:
        sorted_hand = sorted(hand_cards_objects, key=card_sort_key)
        hand_key = ''.join(card_to_string(card) for card in sorted_hand)
        percentile = calculate_percentile_two_card(
            hand_key, two_card_hand_strengths)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return f"Hand: {sorted_hand} \
            \n\n Execution time: {execution_time:.12f} seconds. \
            \n\n Hand strength percentile among all 1,326 possible starting hands: \
            \n{percentile:.4f}%"
    else:
        best_strength = 0
        combined_cards = hand_cards_objects + table_cards_objects
        all_possible_hands = all_combinations_recursive(combined_cards, 5)

        for hand in all_possible_hands:
            sorted_hand = sorted(hand, key=card_sort_key)
            hand_key = ''.join(card_to_string(card) for card in sorted_hand)
            hand_strength = hand_strengths.get(hand_key, 0)
            best_strength = max(best_strength, hand_strength)

        percentile = calculate_percentile(best_strength, hand_strengths)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return f"Hand: {sorted_hand} \
        \n\n Execution time: {execution_time:.12f} seconds. \
        \n\n Hand strength percentile among all 2,598,960 possible poker hands: \
        \n{percentile:.4f}%"


# <---------------------------------------------->
# <---------------------------------------------->
# Flask routes to handle GET and POST requests.
# Take user inputs, call algorithms, display result


@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        # Fetch user input from frontend
        hand_cards = [request.form.get('hand1'), request.form.get('hand2')]
        table_cards = [request.form.get(f'table{i}') for i in range(
            1, 6) if request.form.get(f'table{i}')]

        # Replace 'AceOfDiamonds' with 'AD' in hand_cards and table_cards
        hand_cards = ['AD' if card ==
                      'AceOfDiamonds' else card for card in hand_cards]
        table_cards = ['AD' if card ==
                       'AceOfDiamonds' else card for card in table_cards]

        # check if both hand cards were entered
        if not all(hand_cards):
            output = "Please enter both of your hole cards."
        else:
            evaluation_method = request.form.get('evaluation')
            # Call algorithm selected by the user
            if evaluation_method == "algorithm1":
                output = algorithm1(hand_cards, table_cards)
            elif evaluation_method == "algorithm2":
                output = algorithm2(hand_cards, table_cards)
    # Render the main HTML page with any output
    return render_template('index.html', output=output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
