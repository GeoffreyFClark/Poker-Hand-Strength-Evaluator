from flask import Flask, render_template, request
from itertools import combinations

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


# <---------------------------------------------->
# This algorithm evaluates the strength of a 5-card poker hand, using a numeric value system that incorporates tie-breakers.
# The base strength of each hand type (e.g., pair, straight) is represented as a whole number.
# Tie-breakers are calculated using the card ranks as decimals (0/13 to 12/13),
# with subsequent tiebreak cards descending in magnitude if applicable (1/13, 1/(13^2), 1/(13^3), etc).
# By Geoffrey Clark
def evaluate_hand(hand):
    # Sort the hand by rank with Ace as the highest
    ranks_order = '23456789TJQKA'
    hand = sorted(hand, key=lambda card: ranks_order.index(
        card.rank), reverse=True)

    # Assign numerical values to each card rank for the tiebreaker calculation
    rank_values = {rank: (1/13) * i for i, rank in enumerate(ranks_order)}

    # Initialize dictionaries to count occurrences of each rank and suit
    rank_counts = {rank: 0 for rank in ranks_order}
    suit_counts = {suit: 0 for suit in 'HDCS'}

    # Populate the dictionaries with the counts
    for card in hand:
        rank_counts[card.rank] += 1
        suit_counts[card.suit] += 1

    # Determine if the hand is a flush (all cards of the same suit)
    is_flush = max(suit_counts.values()) == 5

    # Check for a straight and a royal flush
    is_straight = False
    is_royal = False
    sorted_ranks = sorted(hand, key=lambda card: ranks_order.index(card.rank))
    sorted_ranks_str = ''.join(card.rank for card in sorted_ranks)
    if sorted_ranks_str in ranks_order:
        is_straight = True
        if sorted_ranks_str == 'TJQKA':
            is_royal = True

    # Special case for low-Ace straight
    if sorted_ranks_str == '2345A':
        is_straight = True

    # Calculate the hand's strength value
    strength_value = 0

    # Royal Flush
    if is_royal and is_flush:
        strength_value = 10
    # Straight Flush
    elif is_straight and is_flush:
        strength_value = 9 + rank_values[sorted_ranks[-1].rank] / 13
    # Four of a Kind
    elif 4 in rank_counts.values():
        four_of_a_kind_rank = max(
            rank for rank, count in rank_counts.items() if count == 4)
        strength_value = 8 + rank_values[four_of_a_kind_rank] / 13
        # Further tiebreaking logic not applicable (same for 3 of a kind)
        # e.g. Two players aren't going to tie by both having a 4 of a kind with the same rank
    # Full House
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        three_kind_rank = max(
            rank for rank, count in rank_counts.items() if count == 3)
        pair_rank = max(
            rank for rank, count in rank_counts.items() if count == 2)
        strength_value = 7 + \
            (rank_values[three_kind_rank] + rank_values[pair_rank] / 13) / 13
    # Flush
    elif is_flush:
        strength_value = 6
        for i, card in enumerate(sorted(hand, key=lambda card: rank_values[card.rank], reverse=True)):
            strength_value += rank_values[card.rank] / (13 ** (i + 1))
    # Straight
    elif is_straight:
        strength_value = 5 + rank_values[sorted_ranks[-1].rank] / 13
    # Three of a Kind
    elif 3 in rank_counts.values():
        three_kind_rank = max(
            rank for rank, count in rank_counts.items() if count == 3)
        strength_value = 4 + rank_values[three_kind_rank] / 13
    # Two Pair
    elif list(rank_counts.values()).count(2) == 2:
        pairs = sorted(
            (rank for rank in rank_counts if rank_counts[rank] == 2), key=lambda rank: rank_values[rank], reverse=True)
        strength_value = 3
        for i, rank in enumerate(pairs):
            strength_value += rank_values[rank] / (13 ** (i + 1))
    # One Pair
    elif 2 in rank_counts.values():
        pair_rank = max(
            rank for rank, count in rank_counts.items() if count == 2)
        strength_value = 2 + rank_values[pair_rank] / 13
        # Use other hand cards as tie breakers
        remaining_cards = sorted(
            (card for card in hand if rank_counts[card.rank] == 1), key=lambda card: ranks_order.index(card.rank), reverse=True)
        for i, card in enumerate(remaining_cards):
            strength_value += rank_values[card.rank] / (13 ** (i + 2))
    # High Card
    else:
        strength_value = 1
        for i, card in enumerate(sorted(hand, key=lambda card: rank_values[card.rank], reverse=True)):
            strength_value += rank_values[card.rank] / (13 ** (i + 1))

    return strength_value


# Two different types of combinatorial analysis

# <---------------------------------------------->
# Iterative Approach Using Hash Tables
# def algorithm1(hand_cards, table_cards=[]):
#     card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
#                    'A': 14}

#     def calculate_hand_strength(hand):
#         sorted_hand = sorted(
#             hand, key=lambda card: card_values[card.rank], reverse=True)
#         values = [card_values[card.rank] for card in sorted_hand]

#         is_straight = (values[0] - values[4] ==
#                        4) or (values == [14, 5, 4, 3, 2])

#         is_flush = len(set(card.suit for card in sorted_hand)) == 1

#         if is_straight and is_flush:
#             return 9  # straight flush
#         elif values.count(values[0]) == 4 or values.count(values[1]) == 4:
#             return 8  # four of a kind
#         elif values.count(values[0]) == 3 and values.count(values[3]) == 2:
#             return 7  # full house
#         elif is_flush:
#             return 6  # flush
#         elif is_straight:
#             return 5  # straight
#         elif values.count(values[0]) == 3:
#             return 4  # three of a kind
#         elif values.count(values[0]) == 2 and values.count(values[2]) == 2:
#             return 3  # two pair
#         elif values.count(values[0]) == 2:
#             return 2  # one pair
#         else:
#             return 1  # high card

#     all_cards = hand_cards + table_cards
#     combinations_count = {}

#     for card in all_cards:
#         if card.rank in combinations_count:
#             combinations_count[card.rank] += 1
#         else:
#             combinations_count[card.rank] = 1

#     total_combinations = 1
#     for count in combinations_count.values():
#         total_combinations *= count

#     hand_strength = calculate_hand_strength(all_cards)
#     percentile_strength = (hand_strength / total_combinations) * 100

#     return f"Hand Strength: {hand_strength} (Percentile Strength: {percentile_strength:.2f}%)"


# <---------------------------------------------->
# Recursive Approach Using Graphs
def algorithm2(hand_cards, table_cards=[]):
    return "Output from algorithm2"


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
