# Strong and Weakly Dominant Strategy Equilibrium

## Run
`python dse.py <nfg input file>`

This python code finds strongly as well as weakly dominant strategy equilibrium of any n person matrix form game. The input is taken in `.nfg` file format of `gambit`. Read more about the format here <http://www.gambit-project.org/gambit14/formats.html#the-strategic-game-nfg-file-format-payoff-version> 

Please note, that the input nfg file shouldn't have a trailing space. The first line should contain the game name, and the second line should have the player names, followed by the no. of strategies of each player. Third line should be blank, and the 4th line should contain all the payoffs as stated for nfg files on the Gambit website. Please ensure that there are no trailing spaces for the program to function properly

The answers use 0-based indexing

## Files
`GameFiles` folder contains different types of nfg files representing various forms of games. One can run the code on them to find the Strong or Weak Equilibrium (if any)