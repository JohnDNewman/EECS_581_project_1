import pygame as pg
import os
from battleship import Battleship
from ship import Ship


class PyGameLoop:
    def __init__(self):
        '''
        Each board is 1004x1004 and displayed side by side
        10x10 pixels for each box with a 2 pixel outside border
        50 pixel gap between them when displayed
        Left board is where the player shoots
        Right board is where the player places their ships
        '''
        singleBoardWidth  = 1004
        self._width       = 2 * singleBoardWidth + 50
        self._height      = 1004

        self._battleship  = Battleship()
        self._screen      = pg.display.set_mode((self._width, self._height))     # initializes the window
        self._placedShips = [[], []]                                 # list to store the user placed locations of the ships


    def _coordsToPix(boardNum, coords):                                     # takes in 0 or 1 to indicate board to draw on and takes coords to returns pixels on given board
        match coords[0]:
            case 0:
                y = 2
            case 1:
                y = 102
            case 2:
                y = 202
            case 3:
                y = 302
            case 4:
                y = 402
            case 5:
                y = 502
            case 6:
                y = 602
            case 7:
                y = 702
            case 8:
                y = 802
            case 9:
                y = 902

        match coords[1]:
            case 0:
                x = 2
            case 1:
                x = 102
            case 2:
                x = 202
            case 3:
                x = 302
            case 4:
                x = 402
            case 5:
                x = 502
            case 6:
                x = 602
            case 7:
                x = 702
            case 8:
                x = 802
            case 9:
                x = 902

        return ((x + (boardNum * 1054), y))                                     # if boardNum is 0, it's left board and won't shift, if 1, it'll add on the constant x value of the left board to shift
    
    
    def _pixToCoords(pix):                                                  # takes in pixels and returns coordinate values SHOULD ONLY BE NEEDED FOR LEFT BOARD AND NOT RIGHT BOARD
        x, y = -1, -1                                                           # initializes as -1 in case no coordinates are matched
        
        if (pix[0] < 102):
            y = 0
        elif (pix[0] < 202):
            y = 1
        elif (pix[0] < 302):
            y = 2
        elif (pix[0] < 402):
            y = 3
        elif (pix[0] < 502):
            y = 4
        elif (pix[0] < 602):
            y = 5
        elif (pix[0] < 702):
            y = 6
        elif (pix[0] < 802):
            y = 7
        elif (pix[0] < 902):
            y = 8
        elif (pix[0] < 1004):
            y = 9

        if (pix[0] < 102):
            x = 0
        elif (pix[0] < 202):
            x = 1
        elif (pix[0] < 302):
            x = 2
        elif (pix[0] < 402):
            x = 3
        elif (pix[0] < 502):
            x = 4
        elif (pix[0] < 602):
            x = 5
        elif (pix[0] < 702):
            x = 6
        elif (pix[0] < 802):
            x = 7
        elif (pix[0] < 902):
            x = 8
        elif (pix[0] < 1004):
            x = 9

        return ((x, y))


    def _createShips(self, p0Ships, p1Ships):                               # creates ship list based on number of ships
        for event in pg.event.get():                                            # waits for keyboard event
            if (event.type in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5]):            # always adds one ship
                p0Ships.append([(0, 0)])                                                # positions ship in 0th column
                p1Ships.append([(0, 0)])                                                # positions ship in 0th column

            if (event.type in [pg.K_2, pg.K_3, pg.K_4, pg.K_5]):                    # adds second ship if at least 2
                p0Ships.append([(1, 0), (1, 1)])                                        # positions ship in 0th column
                p1Ships.append([(1, 0), (1, 1)])                                        # positions ship in 0th column

            if (event.type in [pg.K_3, pg.K_4, pg.K_5]):                            # adds third ship if at least 3
                p0Ships.append([(2, 0), (2, 1), (2, 2)])                                # positions ship in 0th column
                p1Ships.append([(2, 0), (2, 1), (2, 2)])                                # positions ship in 0th column

            if (event.type in [pg.K_4, pg.K_5]):                                    # adds fourth ship if at least 4
                p0Ships.append([(3, 0), (3, 1), (3, 2), (3, 3)])                        # positions ship in 0th column
                p1Ships.append([(3, 0), (3, 1), (3, 2), (3, 3)])                        # positions ship in 0th column

            if (event.type in [pg.K_5]):                                            # adds fifth ship if it is 5
                p0Ships.append([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])                # positions ship in 0th column
                p1Ships.append([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])                # positions ship in 0th column


    def _drawShips(self, player=None):                                      # draws a player's ships
        if (player is None):                                                    # runs if nothing passed in
            player = self._battleship.turn                                          # defaults to whose turn it is

        shipImgs = [[pg.image.load(os.path.join('assets', 'redShip1.jpg')),     # loads all ship images
                     pg.image.load(os.path.join('assets', 'redShip2.jpg')),
                     pg.image.load(os.path.join('assets', 'redShip3.jpg')),
                     pg.image.load(os.path.join('assets', 'redShip4.jpg')),
                     pg.image.load(os.path.join('assets', 'redShip5.jpg'))],

                    [pg.image.load(os.path.join('assets', 'blueShip1.jpg')),
                     pg.image.load(os.path.join('assets', 'blueShip2.jpg')),
                     pg.image.load(os.path.join('assets', 'blueShip3.jpg')),
                     pg.image.load(os.path.join('assets', 'blueShip4.jpg')),
                     pg.image.load(os.path.join('assets', 'blueShip5.jpg'))]]
        
        for shipLen in range(len(self._placedShips[player])):                   # iterates through the placed ships
            self._screen.blit(shipImgs[player][shipLen], self._coordsToPix(1, self._placedShips[player][shipLen][0])) # draws ship on board (ISSUE WITH VERTICAL/HORIZONTAL DECISION AND COORD TO PIX CONVERSION ON DIFFERENT BOARDS)


    def _drawShots(self):                                                   # draws all the shots taken in the game on the correct side
        missedShot = pg.image.load(os.path.join('assets', 'MissedShot.jpg'))
        hitShot    = pg.image.load(os.path.join('assets', 'HitShot.jpg'))
        sunkShot   = pg.image.load(os.path.join('assets', 'SunkShot.jpg'))

        if (self._battleship.turn == 0):                                        # runs if current turn is PlayerZero
            for i in range(len(self._battleship.boardZero.board)):                  # iterates through current player's board rows
                for j in range(len(i)):                                                 # iterates through current player's board columns
                    match self._battleship.boardZero.board[i][j]:                           # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 3:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot

            for i in range(len(self._battleship.boardOne.board)):                   # iterates through opponent's board rows
                for j in range(len(i)):                                                 # iterates through opponent's board columns
                    match self._battleship.boardOne.board[i][j]:                            # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 3:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot

        else:                                                                   # runs if current turn is PlayerOne
            for i in range(len(self._battleship.boardOne.board)):                   # iterates through current player's board rows
                for j in range(len(i)):                                                 # iterates through current player's board columns
                    match self._battleship.boardOne.board[i][j]:                            # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 3:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot

            for i in range(len(self._battleship.boardZero.board)):                  # iterates through opponent's board rows
                for j in range(len(i)):                                                 # iterates through opponent's board columns
                    match self._battleship.boardZero.board[i][j]:                           # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 3:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot


    def run(self):
        '''
        -------------------------------------------------------------------------------------------
        Local Variables
        -------------------------------------------------------------------------------------------
        '''
        running       = True                                    # boolean for running the game loop
        fps           = 60                                      # frames per second of the window
        fpsClock      = pg.time.Clock()                         # clock that FPS is based on
        #font          = pg.font.SysFont('Arial', 40)            # sets font for text within window (COMMENTED OUT FOR NOW, THINGS NEED TO BE INSTALLED FOR THE FONT)

        welcomeScreen = pg.image.load(os.path.join('assets', 'WelcomeScreen.jpg'))      # PHOTO NOT YET ADDED
        background    = pg.image.load(os.path.join('assets', 'Background.jpg'))         # PHOTO NOT YET ADDED
        passToP0      = pg.image.load(os.path.join('assets', 'PassToP0.jpg'))           # PHOTO NOT YET ADDED
        passToP1      = pg.image.load(os.path.join('assets', 'PassToP1.jpg'))           # PHOTO NOT YET ADDED
        winScreen     = [pg.image.load(os.path.join('assets', 'RedWinScreen.jpg')),     # PHOTO NOT YET ADDED
                         pg.image.load(os.path.join('assets', 'BlueWinScreen.jpg'))]    # PHOTO NOT YET ADDED
        '''
        gamePhase marks the phase of the game:
        0: Intro screen
        1: PlayerZero ship placement screen
        2: PlayerOne ship placement screen
        3: Shooting screen for either player
        4: Game over screen
        '''
        gamePhase       = 1                                     # initializes to 1 for the intro screen
        passingScreen   = False                                 # bool check to see if passing screen should overlay
        winner          = 2                                     # initializes to 2 to show no winner
        p0UnplacedShips = []                                    # list to store the ships before placed by PlayerOne
        p1UnplacedShips = []                                    # list to store the ships before placed by PlayerOne

        '''
        -------------------------------------------------------------------------------------------
        Game Loop
        -------------------------------------------------------------------------------------------
        '''
        while (running):                                        # continuous game loop
            pg.display.flip()                                       # updates the game window
            if (passingScreen):                                     # displays passing screen
                if (gamePhase == 1 | self.battleship.turn == 0):        # displays pass to PlayerZero screen if in placement phase or their turn
                    self._screen.blit(passToP0, (0, 0))
                else:                                                   # displays pass to PlayerOne screen if in placement phase or their turn
                    self._screen.blit(passToP1, (0, 0))

            else:                                                   # continues displaying the game if not in passing mode
                '''
                -----------------------------------------------------------------------------------
                Intro Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 0):                                 # intro screen loop
                    self._screen.blit(welcomeScreen, (0, 0))
                    self._createShips(p0UnplacedShips, p1UnplacedShips)     # populates default ship coordinates
                    if (len(p0UnplacedShips) != 0):                         # checks if ships have been populated yet
                        passingScreen = True                                    # enables passing screen
                        gamePhase     = 1                                       # changes game phase to PlayerZero ship placement

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerZero Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 1):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    self._drawShips(0)                                      # draws PlayerZero ships
                    pg.display.flip()                                       # updates the game window
                    # logic for actual ship placement needs to go here

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerOne Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 2):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    self._drawShips(1)                                      # draws PlayerZero ships
                    pg.display.flip()                                       # updates the game window
                    # logic for actual ship placement needs to go here

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                Shooting Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 3):                                  # core shooting game loop
                    self._screen.blit(background, (0, 0))                   # draws boards
                    self._drawShips()                                       # draws current players' ships
                    self._drawShots()                                       # draws shots on each board
                    pg.display.flip()                                       # updates the game window

                    for event in pg.event.get():                            # waits for mouse event
                        if (event.type == pg.MOUSEBUTTONDOWN):                  # if event is mouse button down
                            coords = self._pixToCoords(pg.mouse.get_pos())          # gets the coordinates from the mouse position pixels
                            if (-1 in coords):                                      # invalid if either coordinate is negative
                                continue                                                # goes to the next loop

                            self._screen.blit(background, (0, 0))                   # draws boards
                            self._drawShips()                                       # draws current players' ships
                            self._drawShots()                                       # draws shots on each board
                            pg.display.flip()                                       # updates the game window

                            winner = self._battleship.takeTurn(coords)              # sends coordinates to Battleship to take turn
                            if (winner != 2):                                       # someone has won if a 0 or 1 is returned, no one has one if it is a 2
                                self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                                gamePhase = 4

                            else:
                                passingScreen = True

                '''
                -----------------------------------------------------------------------------------
                Winner Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 4):                                  # game over screen
                    self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                    pg.display.flip()                                       # updates the game window
                    for event in pg.event.get():
                        if (event.type == pg.MOUSEBUTTONDOWN):
                            '''
                            -----------------------------------------------------------------------
                            Reset values to play again
                            -----------------------------------------------------------------------
                            '''
                            gamePhase        = 1                                    # reinitializes to 1 for the intro screen
                            winner           = 2                                    # reinitializes to 2 to show no winner
                            self._battleship = Battleship()                         # recreates Battleship
                            p0UnplacedShips.clear()                                 # clear ships
                            p1UnplacedShips.clear()                                 # clear ships
                            self._placedShips[0].clear()                            # clear ships
                            self._placedShips[1].clear()                            # clear ships
