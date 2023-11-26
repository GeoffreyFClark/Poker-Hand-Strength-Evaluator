
import itertools
import csv


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


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


# Generate a standard deck of cards
suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [Card(rank, suit) for suit in suits for rank in ranks]

# Generate all possible 5-card combinations
five_card_combinations = itertools.combinations(deck, 5)

# Evaluate each hand and store in a list
hands_data = []
z = 0
for hand in five_card_combinations:
    z += 1
    if z % 10000 == 0:
        print(f'{z} hands processed.')
    hand_strength = evaluate_hand(hand)
    hands_data.append((''.join(map(str, hand)), hand_strength))
print(f'{z} hands evaluated in total.')

# Write the data to a CSV file
with open('poker_hands.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hand', 'Strength'])  # Writing the header
    writer.writerows(hands_data)
