## Implementation:
- PyGame - UI navigate using arrow keys
- Game class, turn number, turn checking, win checking
  - Board/player class, each player interacts with a separate instance, makes moves, checks hits
    - Ship class with list containing cells alive and another list with boolean values and matching indices denoting hit cells
### Ship: 
- Construct with coord list of tuples of (0,0) based on size of ship
- _hitFlag list of boolean values with corresponding indices to coord list
- Method boolean isHit (tuple coords)
- Method boolean isSunk ()
### Board:
- Construct involves entering how many ships you want to place
- List of lists (matrix) representing coordinates
- shipList [Ship, Ship, …]
- Method boolean allSunk()
- Method void shoot(tuple coord)
- Method void setBoard()
- Method boolean _placeShip()
### Battleship:
- boardZero(Player)
- boardOne(Player)
- turn (int)
- Method takeTurn()
- Method _switchTurn()
- Method int checkWin()
### PyGame Loop:
- Constructing means getting two ship lists from the players and constructing the players using these, also create Battleship object
- runningGame (Game)
- Method _pixToCoords (tuple pix)
- Method _coordsToPix (tuple coords)
- Method setUpGame(int numShips)
- Background will show both boards, users place ships on the right board and shoot on the left board
## Tasks:
- Aiden: PyGame
- Andrew: Battleship
- John: Ship
- Kai: Player
- Landon: PyGame

![alt text](https://github.com/JohnDNewman/EECS_581_project_1/blob/main/assets/overview.png?raw=true)
