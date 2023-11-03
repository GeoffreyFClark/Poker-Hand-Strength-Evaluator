from flask import Flask, render_template, request

# Flask app initialization
app = Flask(__name__)

# Card class to store card rank and suit, perhaps add further class methods 
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

# Console inputs initially used before GUI inputs implemented, 
# kept for reference, but planning to remove/archive in future.
def get_user_input():
    print("""Card input format: <rank><suit>. Rank = 2-9, J, Q, K, A; Suit = H, D, S, C. \n
          e.g. 2 of Hearts = 2H; Ace of Diamonds = AD, Jack of Spades = JS, 10 of Clubs = 10C.""")

    hand_cards = [input("Enter your first card: "),
                  input("Enter your second card: ")]
    table_cards = input(
        "Enter table cards (comma separated, e.g. 2H,3D,4C, leave blank for none): ").split(',')
    num_opponents = int(
        input("Enter number of opponents (leave blank for none): ") or 0)
    return hand_cards, table_cards, num_opponents


# Placeholder functions for our evaluation algorithms. 
# We can discuss how to approach these as a group.
def algorithm1(hand_cards, table_cards=[], num_opponents=0):
    return "Output from algorithm1"

def algorithm2(hand_cards, table_cards=[], num_opponents=0):
    return "Output from algorithm2"


# Flask routes to handle both GET and POST requests.
# The main logic for the web app happens here, 
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
            output = "Please enter your hand cards."
        else:
            evaluation_method = request.form.get('evaluation')
            num_opponents = int(request.form.get('opponents') or 0)

            # Call algorithm selected by the user
            if evaluation_method == "algorithm1":
                output = algorithm1(hand_cards, table_cards, num_opponents)
            elif evaluation_method == "algorithm2":
                output = algorithm2(hand_cards, table_cards, num_opponents)

    # Render the main HTML page with any output
    return render_template('index.html', output=output)

# Run Flask app. Debug mode currently on.
if __name__ == "__main__":
    app.run(debug=True)
