# Poker-Hand-Strength-Visualizer

QUICK UPDATE Oct 2, 2023 to get us started (Brief overview posted here for reference):

Added a main.py for the backend, index.html for the frontend (served via Flask), and images for each of the 52 cards.

![image](https://github.com/GeoffreyFClark/Poker-Hand-Strength-Visualizer/assets/97141856/ab3d5112-f282-49c6-8851-a5a83d2b1386)

## TO DO:

General:
- Debug and add test cases (e.g., ensure Table Cards are optional)

Backend:
- Implement algorithm1 and algorithm2. (Rename for clarity once we've agreed upon algorithms to use)
- Ensure input from the frontend is properly processed as parameters for our algorithm functions

Frontend:
- ~~Debug missing AD card in the selection GUI~~ Evidently, my Google Chrome adblock extension was somehow interfering with the AD card specifically haha
- ~~Style the card selection GUI into a grid format (4 columns x 13 rows)~~
- Gray out selected cards (e.g., change to a gray rectangle)
- Populate the selected card images into the "Your Hand" and "Table Cards" input boxes as opposed to 2 alphanumeric characters in boxes
- Allow removal of a card by clicking on populated card image instead of the current "X" system
- Add further CSS styling
- Display the results once the "CALCULATE!" button is clicked (pending completion of algorithm1 and algorithm2)
