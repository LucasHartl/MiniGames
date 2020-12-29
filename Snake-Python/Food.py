import random
from Enums import Representation


# the Food class is representing the food inside the GameField
class Food:
    # the constructor of the Food class
    def __init__(self, max_food):
        self.__max_food = max_food  # define how many fruits should be displayed
        self.__coordinates = []

    # updating the food
    def update(self, field):
        if len(self.__coordinates) < self.__max_food:
            # new food will appear either randomly or if no food is existing
            if random.randint(0, 6) == 1 or len(self.__coordinates) == 0:
                self.__create_food(field)

    # creating the food inside the boundaries
    def __create_food(self, field):
        columns = len(field)
        rows = len(field[0])

        # a food should only be displayed on coordinates where nothing else is rendered
        new_column = random.randint(0, columns - 1)
        new_row = random.randint(0, rows - 1)
        while field[new_column][new_row] != Representation.EMPTY:
            new_column = random.randint(0, columns - 1)
            new_row = random.randint(0, rows - 1)

        self.__coordinates.append([new_column, new_row])
        # print("Food created at [Column | Row]: [{} | {}]".format(new_column, new_row))

    # returning the coordinates of the food objects
    def get_coordinates(self):
        return self.__coordinates

    # delete a given fruit (when the snake has eaten it)
    def delete_food(self, coordinate):
        self.__coordinates.remove(coordinate)


if __name__ == '__main__':
    pass
