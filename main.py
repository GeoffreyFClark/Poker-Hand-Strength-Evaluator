from flask import Flask, render_template, request

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

# TO DO: Using console for now until GUI is fully working.


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


def algorithm1(hand_cards, table_cards=[], num_opponents=0):
    return "Output from algorithm1"


def algorithm2(hand_cards, table_cards=[], num_opponents=0):
    return "Output from algorithm2"


# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        hand_cards = [request.form.get('hand1'), request.form.get('hand2')]
        table_cards = [request.form.get(f'table{i}') for i in range(
            1, 6) if request.form.get(f'table{i}')]

        if not all(hand_cards):
            output = "Please enter your hand cards."
        else:
            evaluation_method = request.form.get('evaluation')
            num_opponents = int(request.form.get('opponents') or 0)

            if evaluation_method == "algorithm1":
                output = algorithm1(hand_cards, table_cards, num_opponents)
            elif evaluation_method == "algorithm2":
                output = algorithm2(hand_cards, table_cards, num_opponents)

    return render_template('index.html', output=output)


if __name__ == "__main__":
    app.run(debug=True)
