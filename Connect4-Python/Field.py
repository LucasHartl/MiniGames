import numpy as np


# the Field class offers a numpy array as the game field and offers two methods to interact with the array
class Field:
    # the constructor of the Field class
    def __init__(self, x, y):
        self.__columns = x
        self.__rows = y

        # generate the field (size = given values)
        self.__field = np.zeros((self.__rows, self.__columns), dtype=int)

    # this method is setting a chip to the game field
    def set(self, x, player_id):
        # calculate the y coordinate
        y = -1
        i = 0
        while self.__field[i][x] == 0:
            y = i
            i += 1
            if i >= self.__rows:
                # the column is completed an no chip can be set anymore
                break

        # if the chip can be set (the column is not completed yet): return the row, else return -1
        if y != -1:
            self.__field[y][x] = player_id

        return y

    # this method checks if a user reached 4 chips in a row and return either the player_id, None, or -1 (played a draw)
    def check_lines(self):
        # check the vertical options
        for x in range(0, self.__columns):
            for y in range(0, self.__rows - 3):
                if self.__field[y][x] != 0 and\
                        (self.__field[y][x] == self.__field[y + 1][x] == self.__field[y + 2][x] == self.__field[y + 3][x]):
                    return self.__field[y][x]

        # check the horizontal options
        for y in range(0, self.__rows):
            for x in range(0, self.__columns - 3):
                if self.__field[y][x] != 0 and\
                        (self.__field[y][x] == self.__field[y][x + 1] == self.__field[y][x + 2] == self.__field[y][x + 3]):
                    return self.__field[y][x]

        # check the diagonal options
        # first the diagonals from lower left to upper right
        for y in range(3, self.__rows):
            for x in range(0, self.__columns - 3):
                if self.__field[y][x] != 0 and\
                        (self.__field[y][x] == self.__field[y - 1][x + 1] == self.__field[y - 2][x + 2] == self.__field[y - 3][x + 3]):
                    return self.__field[y][x]

        # now check the inverse diagonals
        for y in range(0, self.__rows - 3):
            for x in range(0, self.__columns - 3):
                if self.__field[y][x] != 0 and\
                        (self.__field[y][x] == self.__field[y + 1][x + 1] == self.__field[y + 2][x + 2] == self.__field[y + 3][x + 3]):
                    return self.__field[y][x]

        # check if all fields are set, so it is a draw
        drawn = True
        for y in range(self.__rows):
            for x in range(self.__columns):
                if self.__field[y][x] == 0:
                    drawn = False
                    break
        if drawn:
            return -1

        return None

    def __str__(self):
        return str(self.__field)


if __name__ == '__main__':
    # the following lines of code are only for testing purposes
    field = Field(7, 6)
    field.set(2, 2)
    field.set(2, 2)
    field.set(2, 2)
    field.set(2, 1)
    field.set(2, 2)
    field.set(2, 1)
    field.set(2, 3)  # no chip should be set

    # create a vertical row
    field.set(1, 2)
    field.set(1, 2)
    field.set(1, 1)
    field.set(1, 1)

    # create a vertical row
    field.set(5, 1)
    field.set(5, 2)
    field.set(5, 1)
    field.set(5, 1)

    field.set(3, 1)
    field.set(4, 1)
    field.set(3, 2)
    field.set(4, 2)

    print("The winner is: " + str(field.check_lines()))
    print(field)
