from collections import OrderedDict
import csv

hands = ['AA', 'KK', 'QQ', 'JJ', 'AK', 'TT', 'AK', 'AQ', '99', 'AJ', 'AQ', '88',
           'AT', 'KQ', 'AJ', '77', 'KJ', 'QJ', 'KT', 'KQ', 'A9', 'AT', '66', 'A8',
           'QT', 'JT', 'KJ', 'A7', 'A5', 'K9', 'A4', 'A6', '55', 'Q9', 'A3', 'J9',
           'KT', 'QJ', 'A9', 'T9', 'K8', 'A2', 'K7', '44', 'A8', 'QT', 'Q8', 'JT',
           'J8', 'K6', '98', 'T8', 'K5', 'A7', 'K4', 'K9', 'A5', '33', 'K3', 'A4',
           'Q9', '87', 'Q7', 'T7', 'Q6', 'K2', 'J7', 'A6', '97', 'Q5', 'A3', 'J9',
           'T9', '22', 'K8', 'A2', 'Q4', '76', 'K7', '86', '96', 'J6', 'J5', 'K6',
           'Q3', 'Q2', 'T6', '65', 'K5', '75', 'Q8', '54', 'J8', 'J4', 'T8', '98',
           '85', '95', 'K4', 'J3', '64', 'T4', 'T5', '87', 'Q7', 'K3', 'J2', '74',
           '97', 'J7', '53', 'Q6', 'T3', 'K2', '94', 'T7', '84', '43', '63', 'Q5',
           '86', 'T2', '93', '76', 'Q4', '92', '96', '73', 'J6', 'Q3', '52', '65',
         'J5', 'T6', '82', '42', '83', 'Q2', '75', '54', 'J4', '62', '85', '32',
         '95', '72', 'J3', 'T5', 'T4', '64', 'J2', '53', '74', '84', 'T3', '43',
         '94', 'T2', '93', '63', '92', '73', '52', '42', '83', '82', '62', '32',
         '72']

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

total_items = len(swapped_dataset)
percentiles = {k: (i + 1) / total_items * 100 / 10 for i, k in enumerate(swapped_dataset.keys())}

csv_filename = '2card_poker_hands.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['pokerHand', 'strength'])

    for poker_hand, percentile in zip(swapped_dataset.keys(), percentiles.values()):
        csv_writer.writerow([poker_hand, percentile])

print(f'Data written to {csv_filename}')
