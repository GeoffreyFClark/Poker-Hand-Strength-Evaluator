from flask import Flask, render_template, request
from itertools import combinations
from Custom_Dataset_of_all_5_card_poker_hands.5Card_PokerHand_Dataset_Generator.py 
import evaluate_hand
import csv
import time

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


# <---------------------------------------------->
# Two different types of combinatorial analysis


# Iterative Approach Using Hash Tables
# Currently requires 2 hand cards and >= 3 table cards. TODO: Add logic to handle 0-2 table cards.
hand_strengths = {}
with open('Custom_Dataset_of_all_5_card_poker_hands/poker_hands.csv', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        hand_strengths[row[0]] = float(row[1])
        # Pre-made dataset took 36.50181007385254 seconds to generate + evaluate all 2,598,960 possible 5 card hand combinations.


def card_sort_key(card):
    rank_order = '23456789TJQKA'
    suit_order = 'HDCS'
    return (rank_order.index(card[0]), suit_order.index(card[1]))


def calculate_percentile(best_strength, hand_strengths):
    less_or_equal_count = sum(
        1 for strength in hand_strengths.values() if strength <= best_strength)
    total_hands = len(hand_strengths)
    percentile = (less_or_equal_count / total_hands) * 100
    return percentile

# algorithm2 functions
def evaluate_hand(hand, hand_strengths):
    # Evaluates the strength of the current hand to be used in build_graph
    sorted_hand = sorted(hand, key=card_sort_key)
    hand_key = ''.join(sorted_hand)
    return hand_strengths.get(hand_key, 0)

def build_graph(hand_cards, table_cards):
    # Graphs possible movies in a Poker game
    graph = {}
    combined_cards = hand_cards + table_cards

    for card in combined_cards:
        potential_hand = combined_cards.copy()
        potential_hand.remove(card)
        strength = evaluate_hand(potential_hand, hand_strengths)
        graph[tuple(potential_hand)] = strength

    return graph

def dfs(graph, current_hand, best_strength):
    # Depth-first recursive function to explore all possible paths to find maximum strength and only returns the maximum found
    for card in graph:
        new_hand = current_hand + [card]
        new_strength = graph[card]
        best_strength = max(best_strength, new_strength)
        best_strength = dfs(graph, new_hand, best_strength)
    return best_strength

def algorithm1(hand_cards, table_cards=[]):
    start_time = time.time()

    best_strength = 0
    combined_cards = hand_cards + table_cards
    all_possible_hands = combinations(combined_cards, 5)

    for hand in all_possible_hands:
        # Sort each hand correctly
        sorted_hand = sorted(hand, key=card_sort_key)
        hand_key = ''.join(sorted_hand)
        hand_strength = hand_strengths.get(hand_key, 0)
        best_strength = max(best_strength, hand_strength)

    percentile = calculate_percentile(best_strength, hand_strengths)

    end_time = time.time()
    execution_time = end_time - start_time

    return f"Hand strength percentile among all 2,598,960 possible poker hands: {percentile:.4f}% \n Execution time: {execution_time:.4f} seconds."

# <---------------------------------------------->
# Recursive Approach Using Graphs
def algorithm2(hand_cards, table_cards=[]):
    start_time = time.time()

    # Run build_graph, dfs, and calculate_percentile functions here
    graph = build_graph(hand_cards, table_cards)
    best_strength = dfs(graph, [], 0)
    percentile = calculate_percentile(best_strength, hand_strengths)

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


# Run Flask app. Debug mode currently on.
if __name__ == "__main__":
    app.run(debug=True)
