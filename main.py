from flask import Flask, render_template, request
from itertools import combinations
from Custom_Dataset_of_all_5_card_poker_hands._5Card_PokerHand_Dataset_Generator import evaluate_hand
import csv
import time

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


hand_strengths = {}
with open('Custom_Dataset_of_all_5_card_poker_hands/poker_hands.csv', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        hand_strengths[row[0]] = float(row[1])
        # Pre-made dataset took 36.50181007385254 seconds to generate + evaluate all 2,598,960 possible 5 card hand combinations.


# <---------------------------------------------->
# Two different types of combinatorial analysis
# <---------------------------------------------->

# 1. (Combinatorial Analysis) Iterative Approach Using Hash Tables
# Currently requires 2 hand cards and >= 3 table cards. TODO: Add logic to handle 0-2 table cards.


def card_sort_key(card):
    rank_order = '23456789TJQKA'
    suit_order = 'HDCS'

    try:
        rank_index = rank_order.index(card[0])
    except ValueError:
        print(f"Error: Rank '{card[0]}' not found in rank_order.")
        rank_index = 0

    try:
        suit_index = suit_order.index(card[1])
    except ValueError:
        print(f"Error: Suit '{card[1]}' not found in suit_order.")
        suit_index = 0

    return (rank_order.index(card[0]), suit_order.index(card[1]))


def calculate_percentile(best_strength, hand_strengths):
    less_or_equal_count = sum(
        1 for strength in hand_strengths.values() if strength <= best_strength)
    total_hands = len(hand_strengths)
    percentile = (less_or_equal_count / total_hands) * 100
    return percentile


def algorithm1(hand_cards, table_cards=[]):
    start_time = time.time()

    best_strength = 0
    combined_cards = hand_cards + table_cards
    all_possible_hands = combinations(combined_cards, 5)

    for hand in all_possible_hands:
        converted_hand = [f'T{card[2:]}' if card.startswith('10') else card for card in hand]

        sorted_hand = sorted(converted_hand, key=card_sort_key)

        hand_key = ''.join(sorted_hand)
        hand_strength = hand_strengths.get(hand_key, 0)
        best_strength = max(best_strength, hand_strength)

    percentile = calculate_percentile(best_strength, hand_strengths)

    end_time = time.time()
    execution_time = end_time - start_time

    return f"Hand strength percentile among all 2,598,960 possible poker hands: {percentile:.4f}% \n Execution time: {execution_time:.4f} seconds."

# <---------------------------------------------->

# 2. (Combinatorial Analysis) Recursive Approach Using Graphs


class HandNode:
    def __init__(self, card_objects):
        self.cards = card_objects
        self.strength = evaluate_hand(self.cards)


def build_graph(hand_cards, table_cards):
    graph = {}
    all_cards = hand_cards + table_cards
    for hand_combination in combinations(all_cards, 5):
        graph[hand_combination] = HandNode(list(hand_combination))
    return graph


def find_best_hand(graph):
    return max(graph.values(), key=lambda node: node.strength)


def calculate_percentile_algorithm2(best_strength, all_hand_strengths):
    less_or_equal_count = sum(
        1 for strength in all_hand_strengths if strength <= best_strength)
    total_hands = len(all_hand_strengths)
    percentile = (less_or_equal_count / total_hands) * 100
    return percentile


def algorithm2(hand_cards, table_cards=[]):
    start_time = time.time()

    # Convert string representations to Card objects
    hand_cards_objects = [Card(card[:-1], card[-1]) for card in hand_cards]
    table_cards_objects = [Card(card[:-1], card[-1]) for card in table_cards]
    graph = build_graph(hand_cards_objects, table_cards_objects)

    best_hand_strength = max(node.strength for node in graph.values())
    percentile = calculate_percentile_algorithm2(
        best_hand_strength, list(hand_strengths.values()))

    end_time = time.time()
    execution_time = end_time - start_time
    return f"Hand strength percentile among all 2,598,960 possible poker hands: {percentile:.4f}% \n Execution time: {execution_time:.4f} seconds."

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

        # check if both hand cards were entered
        if not all(hand_cards):
            output = "Please enter both of your hand cards."
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
    app.run(debug=True)
