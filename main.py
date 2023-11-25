from flask import Flask, render_template, request
from itertools import combinations

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


# Two different types of combinatorial analysis

# Iterative Approach Using Hash Tables
def algorithm1(hand_cards, table_cards=[]):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
                   'A': 14}

    def calculate_hand_strength(hand):
        sorted_hand = sorted(hand, key=lambda card: card_values[card.rank], reverse=True)
        values = [card_values[card.rank] for card in sorted_hand]

        is_straight = (values[0] - values[4] == 4) or (values == [14, 5, 4, 3, 2])

        is_flush = len(set(card.suit for card in sorted_hand)) == 1

        if is_straight and is_flush:
            return 9  # straight flush
        elif values.count(values[0]) == 4 or values.count(values[1]) == 4:
            return 8  # four of a kind
        elif values.count(values[0]) == 3 and values.count(values[3]) == 2:
            return 7  # full house
        elif is_flush:
            return 6  # flush
        elif is_straight:
            return 5  # straight
        elif values.count(values[0]) == 3:
            return 4  # three of a kind
        elif values.count(values[0]) == 2 and values.count(values[2]) == 2:
            return 3  # two pair
        elif values.count(values[0]) == 2:
            return 2  # one pair
        else:
            return 1  # high card

    all_cards = hand_cards + table_cards
    combinations_count = {}

    for card in all_cards:
        if card.rank in combinations_count:
            combinations_count[card.rank] += 1
        else:
            combinations_count[card.rank] = 1

    total_combinations = 1
    for count in combinations_count.values():
        total_combinations *= count

    hand_strength = calculate_hand_strength(all_cards)
    percentile_strength = (hand_strength / total_combinations) * 100

    return f"Hand Strength: {hand_strength} (Percentile Strength: {percentile_strength:.2f}%)"


# Recursive Approach Using Graphs
def algorithm2(hand_cards, table_cards=[]):
    return "Output from algorithm2"


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
