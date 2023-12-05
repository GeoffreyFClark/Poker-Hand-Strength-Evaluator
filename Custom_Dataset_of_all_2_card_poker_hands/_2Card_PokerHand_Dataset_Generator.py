from collections import OrderedDict
import csv

hands = ['AA', 'KK', 'QQ', 'JJ', 'AK', 'TT', 'AK', 'AQ', '99', 'AJ', 'AQ', '88',
           'AT', 'KQ', 'AJ', '77', 'JK', 'JQ', 'KT', 'KQ', 'A9', 'AT', '66', '8A',
           'QT', 'JT', 'KJ', '7A', '5A', '9K', '4A', '6A', '55', '9Q', '3A', '9J',
           'KT', 'QJ', '9A', '9T', '8K', '2A', '7K', '44', '8A', 'QT', '8Q', 'JT',
           '8J', '6K', '89', '8T', '5K', '7A', '4K', '9K', '5A', '33', '3K', '4A',
           '9Q', '87', '7Q', '7T', '6Q', '2K', '7J', '6A', '97', '5Q', 'A3', 'J9',
           'T9', '22', 'K8', 'A2', 'Q4', '67', 'K7', '68', '69', 'J6', 'J5', 'K6',
           'Q3', 'Q2', 'T6', '59', 'K5', '57', 'Q8', '45', '8J', '4J', 'T8', '89',
           '58', '59', '4K', '3J', '46', '4T', '5T', '78', '7Q', '3K', '2J', '47',
           '79', '7J', '35', 'Q6', '3T', '2K', '49', '7J', '48', '34', '36', '5Q',
           '68', '2T', '39', '67', '4Q', '29', '69', '37', '6J', '3Q', '25', '56',
         '5J', '6T', '28', '24', '38', '2Q', '57', '45', '4J', '26', '58', '23',
         '59', '27', '3J', '5T', '4T', '46', '2J', '35', '47', '48', '3T', '34',
         '49', '2T', '39', '36', '29', '37', '25', '24', '38', '28', '26', '23',
         '27']

modified_dataset = OrderedDict()

for card in hands:
    modified_card = [
        card[0] + suit + card[1] + other_suit
        for suit in ['S', 'C', 'D', 'H']
        for other_suit in ['S', 'C', 'D', 'H']
        if len(card) > 1 and other_suit != card[1] and card[0] + card[1] != card[2:] + other_suit
    ]
    modified_card = [
        item
        for item in modified_card
        if item[:2] != item[2:] and item[:2][::-1] not in modified_dataset
    ]
    for unique_combination in set(modified_card):
        modified_dataset[unique_combination] = None

reversed_modified_dataset = OrderedDict(reversed(modified_dataset.items()))

swapped_dataset = OrderedDict((key[2:] + key[:2] if key[0] > key[2] else key, value) for key, value in reversed_modified_dataset.items())

total_items = len(hands)
percentiles = {k: (i + 1) / total_items * 100 / 10 for i, k in enumerate(swapped_dataset.keys())}

csv_filename = '2card_poker_hands.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['pokerHand', 'strength'])

    for poker_hand in swapped_dataset.keys():
        first_char = poker_hand[0]
        third_char = poker_hand[2]
        index = hands.index(first_char + third_char)
        percentile = (total_items - index) / total_items * 10
        csv_writer.writerow([poker_hand, percentile])