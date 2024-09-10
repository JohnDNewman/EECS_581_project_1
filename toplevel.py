from pygameloop import PyGameLoop


def main():
    # Instantiate the pygame class 
    numShips = int(input("How many Ships will you be playing with? (1-5): "))
    game = PyGameLoop(800,600,numShips)
    game.setUpGame()
    game.run()


if __name__ == "__main__":
    main()
