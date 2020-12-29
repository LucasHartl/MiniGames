from Enums import Directions


# the Snake class is representing the snake-character
class Snake:
    # the constructor of the Snake class
    def __init__(self, start_column, start_row, max_columns, max_rows):
        self.__direction = Directions.RIGHT  # default direction on start
        self.__coordinates = [[start_column, start_row], [start_column-1, start_row]]  # start with a score of 2
        self.__grow = False  # this flag is used when the snake has eaten a fruit
        self.__max_columns = max_columns  # boundary of the GameField
        self.__max_rows = max_rows  # boundary of the GameField

    # this method is setting the wanted direction to the snake
    def set_direction(self, direction):
        # if the user wants a turn of 180° do not accept this input
        if self.__direction == Directions.LEFT and direction != Directions.RIGHT or \
                self.__direction == Directions.RIGHT and direction != Directions.LEFT or \
                self.__direction == Directions.UP and direction != Directions.DOWN or \
                self.__direction == Directions.DOWN and direction != Directions.UP:
            self.__direction = direction

    # moving the snake with the current direction inside the GameField
    def move(self):
        # delete the last coordinate and insert it before the head of the snake with new coordinates
        if self.__grow:
            # create a dummy value
            last_coordinate = [0, 0]
        else:
            last_coordinate = self.__coordinates.pop()

        edge_collision = False
        if self.__direction == Directions.LEFT:
            # print("LEFT")
            if self.__coordinates[0][0] - 1 < 0:
                edge_collision = True
            else:
                last_coordinate[0] = self.__coordinates[0][0] - 1
                last_coordinate[1] = self.__coordinates[0][1]
        elif self.__direction == Directions.RIGHT:
            # print("Right")
            if self.__coordinates[0][0] + 1 >= self.__max_columns:
                edge_collision = True
            else:
                last_coordinate[0] = self.__coordinates[0][0] + 1
                last_coordinate[1] = self.__coordinates[0][1]
        elif self.__direction == Directions.UP:
            # print("UP")
            if self.__coordinates[0][1] - 1 < 0:
                edge_collision = True
            else:
                last_coordinate[0] = self.__coordinates[0][0]
                last_coordinate[1] = self.__coordinates[0][1] - 1
        elif self.__direction == Directions.DOWN:
            # print("DOWN")
            if self.__coordinates[0][1] + 1 >= self.__max_rows:
                edge_collision = True
            else:
                last_coordinate[0] = self.__coordinates[0][0]
                last_coordinate[1] = self.__coordinates[0][1] + 1
        else:
            print("Fatal Error, exit")
            exit(1)
        self.__coordinates.insert(0, last_coordinate)
        self.__grow = False

        # if the snake dies return False
        if self.bitten_itself() or edge_collision:
            return False
        else:
            return True

    # if the snake should grow in the next round set the flag __grow to True
    def grow_in_next_round(self, b):
        self.__grow = b

    # returning the used coordinates of the Snake
    def get_coordinates(self):
        return self.__coordinates

    # if the snake has bitten itself, return True
    def bitten_itself(self):
        for i in range(1, len(self.__coordinates)):
            if self.__coordinates[0] == self.__coordinates[i]:
                return True
        return False

    # returning the length of the snake (used for the score)
    def get_length(self):
        return len(self.__coordinates)


if __name__ == '__main__':
    pass
