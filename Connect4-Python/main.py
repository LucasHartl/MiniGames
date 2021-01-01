from Field import Field
import pygame


# the Game class is handling the game, the user input and is offering a user interface
class Game:
    # the constructor of the Game class
    def __init__(self):
        pygame.init()  # using pygame to display the user interface
        pygame.font.init()

        # with and height: 700x700
        self.__width_window = 700
        self.__height_window = self.__width_window
        self.__font = pygame.font.SysFont("Comic Sans MS", int(self.__height_window * 4/70))
        self.__window = pygame.display.set_mode((self.__width_window, self.__height_window))
        pygame.display.set_caption("4 Gewinnt!")

        self.__columns = 7  # the amount of columns
        self.__rows = 6  # the amount of rows
        self.__field = Field(self.__columns, self.__rows)  # the game field object
        self.__player_a_chips = []  # storing the chips of player a
        self.__player_b_chips = []  # storing the chips of player b
        self.__current_player = 1  # the current player id (the value is toggling permanently)

        self.__img_field = pygame.image.load("./res/gamefield.png")  # loading the game field image
        self.__img_red = pygame.image.load("./res/red.png")  # loading the chip for the red player
        self.__img_yellow = pygame.image.load("./res/yellow.png")  # loading the chip for the yellow player
        self.__img_red_icon = pygame.image.load("./res/red.png")  # loading the chip-icon for the red player, displayed in the top right corner
        self.__img_yellow_icon = pygame.image.load("./res/yellow.png")  # loading the chip-icon for the yellow player, displayed in the top right corner

        # scale the images relative to the size of the window
        tmp = int(self.__img_field.get_rect().size[1] * self.__width_window / self.__img_field.get_rect().size[0])
        self.__img_field = pygame.transform.scale(self.__img_field, (self.__width_window, tmp))

        tmp = int(self.__img_field.get_rect().size[0] / self.__columns)
        self.__img_red = pygame.transform.scale(self.__img_red, (tmp, tmp))
        self.__img_yellow = pygame.transform.scale(self.__img_yellow, (tmp, tmp))

        tmp = int((self.__img_field.get_rect().size[0] / self.__columns) / 2)
        self.__img_red_icon = pygame.transform.scale(self.__img_red_icon, (tmp, tmp))
        self.__img_yellow_icon = pygame.transform.scale(self.__img_yellow_icon, (tmp, tmp))

        self.__winner_exists = False

    # the main method, containing the game loop
    def run(self):
        # initially render the empty field
        self.__window.fill((0, 0, 0))
        self.__window.blit(self.__img_field, (0, self.__height_window - self.__img_field.get_rect().size[1]))
        if self.__current_player == 1:
            title = "Rot ist am Zug!"
            image = self.__img_red_icon
        else:
            title = "Gelb ist am Zug!"
            image = self.__img_yellow_icon

        self.__window.blit(self.__font.render(title, False, (255, 0, 0)), (10, 10))
        # the size of the two icons are the same, so the size of yellow can be used to calculate the position
        self.__window.blit(image, (self.__width_window - self.__img_yellow_icon.get_rect().size[0] - 10, 10))

        # starting the game loop
        run = True
        while run:
            pygame.time.delay(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP and not self.__winner_exists:
                    pos = pygame.mouse.get_pos()
                    self.__window.fill((0, 0, 0))
                    self.update(int(pos[0] / (self.__width_window / self.__columns)))  # update the game

            pygame.display.update()
        pygame.quit()

    # this method is updating the game and is called if the user clicks on the user interface
    def update(self, column):
        # if the chip was set successfully, toggle the current player
        row = self.__field.set(column, self.__current_player)
        if row != -1:
            if self.__current_player == 1:
                # call the set_chip method to display the animation
                self.set_chip(column, row)
                self.__player_a_chips.append((column, row))
                self.__current_player = 2
            else:
                self.set_chip(column, row)
                self.__player_b_chips.append((column, row))
                self.__current_player = 1

        self.draw_chips()

        # get the current winner state (winner = red = 1, winner = yellow = 2, drawn = -1)
        winner = self.__field.check_lines()
        if winner == 1:
            title = "Rot hat gewonnen!"
            color = (255, 0, 0)
            print(title)
            self.__winner_exists = True
        elif winner == 2:
            title = "Gelb hat gewonnen!"
            color = (255, 255, 0)
            print(title)
            self.__winner_exists = True
        elif winner == -1:
            title = "Unentschieden!"
            color = (255, 255, 255)
            print(title)
            self.__winner_exists = True
        else:
            # change the icon in the top right corner to the current player color and display the corresponding text
            if self.__current_player == 1:
                title = "Rot ist am Zug!"
                color = (255, 0, 0)
                image = self.__img_red_icon
            else:
                title = "Gelb ist am Zug!"
                color = (255, 255, 0)
                image = self.__img_yellow_icon

            # draw the icon to show the current players color
            self.__window.blit(image, (self.__width_window - self.__img_yellow_icon.get_rect().size[0] - 10, 10))

        # draw the headline
        self.__window.blit(self.__font.render(title, False, color), (10, 10))

        # draw the game field image over the individual chips
        self.__window.blit(self.__img_field, (0, self.__height_window - self.__img_field.get_rect().size[1]))

    # drawing all the chips
    def draw_chips(self):
        # the chips are additionally stored in the list __player_a_chips or __player_b_chips
        # loop through this lists and display the corresponding image
        for coordinate in self.__player_a_chips:
            self.__window.blit(self.__img_red, (int(coordinate[0] * (self.__width_window / self.__columns)), int(
                coordinate[1] * self.__img_red.get_rect().size[0] + self.__height_window -
                self.__img_field.get_rect().size[1])))

        for coordinate in self.__player_b_chips:
            self.__window.blit(self.__img_yellow, (int(coordinate[0] * (self.__width_window / self.__columns)), int(
                coordinate[1] * self.__img_yellow.get_rect().size[0] + self.__height_window -
                self.__img_field.get_rect().size[1])))

    # display the animation
    def set_chip(self, column, row):
        # define the image which should be rendered
        if self.__current_player == 1:
            image = self.__img_red
        else:
            image = self.__img_yellow

        y = 0
        y_max = int(
            row * self.__img_yellow.get_rect().size[0] + self.__height_window - self.__img_field.get_rect().size[1])
        threshold = 20
        while y < y_max:
            pygame.time.delay(5)
            self.__window.fill((0, 0, 0))
            self.__window.blit(image, (int(column * (self.__width_window / self.__columns)), y))
            self.draw_chips()
            y += threshold
            self.__window.blit(self.__img_field, (0, self.__height_window - self.__img_field.get_rect().size[1]))
            pygame.display.update()

        self.__window.fill((0, 0, 0))
        self.draw_chips()
        pygame.display.update()


# start the game
if __name__ == '__main__':
    Game().run()
