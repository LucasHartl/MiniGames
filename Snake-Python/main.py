from GameField import GameField
from Enums import Directions, Representation
from tkinter import Tk, messagebox
import pygame


# the Game class is handling the user interface as well as the user input (arrow keys)
# this class exists of some standard attributes and a GameField, which is handling the logic behind the user interface
class Game:
    # the constructor of the Game class
    def __init__(self):
        pygame.init()  # using pygame to display the user interface
        self.__font = pygame.font.SysFont("Comic Sans MS", 30)
        self.__size_tiles = 20  # the size of the tiles
        self.__width = 15  # the width of the GameField
        self.__height = 15  # the height of the GameField
        self.__game_field = GameField(self.__width, self.__height)
        self.__headline_space = 50
        self.__width_window = self.__size_tiles * self.__width
        self.__height_window = self.__size_tiles * self.__height + self.__headline_space
        self.__window = pygame.display.set_mode((self.__width_window, self.__height_window))
        pygame.display.set_caption("Snake")

    # the main method, containing the game loop
    def run(self):
        playing = True
        frame_counter = 0
        # game loop
        while playing:
            pygame.time.delay(10)
            frame_counter += 1

            # getting the events and the key presses
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    playing = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.__game_field.set_direction(Directions.LEFT)
            elif keys[pygame.K_RIGHT]:
                self.__game_field.set_direction(Directions.RIGHT)
            elif keys[pygame.K_UP]:
                self.__game_field.set_direction(Directions.UP)
            elif keys[pygame.K_DOWN]:
                self.__game_field.set_direction(Directions.DOWN)

            # update the whole game field
            # use the frame_counter variable in order to delay the game a bit because when increasing the delay time,
            # the keyboard input may not be recognized by the game loop (the program is sleeping)
            # so for the necessary delay use an additional frame_counter
            if frame_counter >= 15:
                frame_counter = 0
                # if the GameField can not be updated, the snake died
                if self.__game_field.update() == False:
                    # display a messagebox using tkinter and restarting the game
                    root = Tk()
                    root.withdraw()
                    messagebox.showerror("Game Over", "The Snake died!\nYour Score: {}".format(self.__game_field.get_score()))
                    root.destroy()
                    self.__game_field.reset()

                # rendering the changes to the screen
                self.__window.fill((0, 0, 0))
                for column in range(self.__game_field.get_columns_count()):
                    for row in range(self.__game_field.get_rows_count()):
                        representation = self.__game_field.get_representation(column, row)
                        if representation is Representation.EMPTY:
                            pygame.draw.rect(self.__window, (255, 255, 255),
                                             (column * self.__size_tiles, row * self.__size_tiles + self.__headline_space,
                                              self.__size_tiles, self.__size_tiles))
                        elif representation == Representation.FOOD:
                            pygame.draw.rect(self.__window, (255, 0, 0),
                                             (column * self.__size_tiles, row * self.__size_tiles + self.__headline_space,
                                              self.__size_tiles, self.__size_tiles))
                        elif representation == Representation.SNAKE:
                            pygame.draw.rect(self.__window, (0, 255, 0),
                                             (column * self.__size_tiles, row * self.__size_tiles + self.__headline_space,
                                              self.__size_tiles, self.__size_tiles))
                        elif representation == Representation.HEAD_SNAKE:
                            pygame.draw.rect(self.__window, (52, 83, 0),
                                             (column * self.__size_tiles, row * self.__size_tiles + self.__headline_space,
                                              self.__size_tiles, self.__size_tiles))
                        else:
                            print(representation)
                            print("Fatal Error, exit.")
                            exit(2)

            # finally rendering the score to the screen and update the window
            headline = self.__font.render("Snake Score: {}".format(self.__game_field.get_score()), False, (0, 255, 0))
            self.__window.blit(headline, (0, 0))
            pygame.display.update()

        pygame.quit()


# start the game
if __name__ == '__main__':
    Game().run()
