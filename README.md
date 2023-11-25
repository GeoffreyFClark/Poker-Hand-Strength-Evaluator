# Poker-Hand-Strength-Visualizer

![image](nov23frontend.png)

## Key Assignment Requirements:
Implement 2 non-trivial, **comparable** algorithms or data structures. Data Structures and Algorithms that are **not** counted towards the requirement of two data structures and algorithms:
- Any data structure from Module 2: Lists, Stacks, and Queues,
- Binary Search Tree,
- AVL Tree,
- Binary and Linear Search,
- Selection, Bubble, Heap, and Insertion Sort.

You must use a data set that has at least 100,000 tuples or rows or data points (e.g. 100,000 vertices in a Graph).
<br>

## UPDATE:
Frontend essentially complete. Takes user input for hand_cards and optional table_cards. Algo1 or Algo2 is called using these parameters to generate the output to be displayed in the frontend.

TO DO: The plan is to implement Combinatorial Analysis algorithms to output a percentile for the user's hand among all possible poker hand combinations (taking into account 0 to 5 provided table cards).
- 1. Iterative Approach Using Hash Tables
- 2. Recursive Approach Using Graphs

If 3 table cards are input along w the user's hand (2 cards), we can output an additional percentile based on the user's input vs the poker dataset of 5 card combos.
