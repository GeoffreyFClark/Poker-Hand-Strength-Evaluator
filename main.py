from flask import Flask, render_template, request

app = Flask(__name__)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


# Two different types of combinatorial analysis

# Iterative Approach Using Hash Tables
def algorithm1(hand_cards, table_cards=[], num_opponents=0):
    return "Output from algorithm1"


# Recursive Approach Using Graphs
def algorithm2(hand_cards, table_cards=[], num_opponents=0):
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
        num_opponents = int(request.form.get('opponents') or 0)

        # check if both hand cards were entered
        if not all(hand_cards):
            output = "Please enter both of your hand cards."
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
