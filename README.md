# Water Puzzle Solver
Python AI that gives the steps to solve the game given here: http://phonesapps.org/water-puzzle-walkthrough-level-1-to-10.html

## How to use

When the program starts up, it will ask you a few questions to set up the game before solving it.

1. `Please enter the quantity` Enter the desired water quantity you're trying to make.
2. `Please enter the capacity of the target glass` Enter the volume of the glass you want to pour the desired quantity into
3. `Please enter the target of the level` Enter the goal number of steps you want to complete the puzzle in
4. `Please enter the litre capacity of each glass followed by enter` Enter the volume of all the glasses you're given
  * If asked "Did you forget to enter your target glass", enter the volume of the target glass followed by enter
5. Voila!

## Example
![alt tag](http://phonesapps.org/wp-content/uploads/2013/4/water-puzzle-2.jpg)
```
Welcome to the game solver!
Please enter the quantity:
2
Please enter the capacity of the target glass:
4
Please enter the target for the level:
4
Please enter the litre capacity of each glass followed by enter:
4
6

========
Solution
========

Fill 6L glass
Pour 6L glass in 4L glass
Empty 4L glass
Pour 6L glass in 4L glass

** Done! **

Replay? (y/n)
```
