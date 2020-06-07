# Settlers of Catan Implmented Using Python

## This is a project written by Dunmin Zhu for [15-112 2019 Spring Term Project](http://www.krivers.net/15112-s19/notes/term-project.html) at Carnegie Mellon University.

### Basic Introduction:

The game is modelled on the classic ["Settlers of Catan"](https://www.catan.com/game/catan) board game in python. This includes all the rules in the official rulebook. The inclusion of socket allows multiplayers to operate on the same game board at the same time and interact with each other by trading "goods".

### Requirements
* Python 3
* tkinter (included)

### Instructions
* Run "Catan_server.py"
* If you only intend to test the game, there is no need to input any IP address. All you left to do is to run "Catan_client.py" in two separate terminals.
* If you want to play with friends, you need to input each other's IP address in the file. Both need to run the above client file.

```
-------------------------------------------
Basic introduction to the game:
The game is invented by Klaus Teuber and published first in Germany in 1995.

What to do in every turn:
0. In the first turn, each player has enough resources to build two roads and two settlements.
1. Roll the dice. If your settlement/city is built on one of the six points of the patches, and the dice number is equal to the the number on the patch, the player will get the corresponding resource.
2. Building
3. Trading

P.S. If the dice is equal to seven, you have to right to move mob. The patch who has the mob on it cannot produce any resource.

Things to be noticed in building:
1. Every your own settlement must be connected to your road.
2. There must be at least two-road distance between any settlements or cities.

Things to be noticed in trading:
1. In your turn, you can trade any of the FOUR same resources that you have for ONE any of the resource that you desire.
2. If you have a settlement or city built on the port, you can trade with the port. You can trade any of the THREE same resources that you have for ONE any of the resource that you desire.
3. You can send trade request to any of the online players and they have the right to accept or decline the trade.

Things to be noticed in using development card:
1. There are three development cards: moveMob card, feast card, and extra VP card.
2. You can use moveMob card to move the mob
3. You can use feast card to get any of the three identical resource
4. Earning an extra victory point gives you an advantage over other players.

You have to win 10 victory points to win the game. Good Luck!
-------------------------------------------
```
