from Snake import Snake
from Food import Food
from Enums import Representation


# the GameField class contains the field itself, the snake which is moving inside the field and the food objects
# the game logic is also handled in this class
class GameField:
    # the constructor of the GameField class
    def __init__(self, columns, rows):
        self.__columns = columns
        self.__rows = rows
        # creating the snake, starting in the left middle of the GameField
        self.__snake = Snake(1, int(self.__rows / 2), self.__columns, self.__rows)
        # the field is like: self.__field[columns][rows]
        self.__field = [[Representation.EMPTY for i in range(self.__rows)] for j in range(self.__columns)]
        # creating 3 food objects. To increase the amount of food, increase the parameter
        self.__food = Food(3)

    # forward the parameter to the snake object
    def set_direction(self, direction):
        self.__snake.set_direction(direction)

    # updating the whole GameFiled
    def update(self):
        # update the food and getting the current coordinates of the food objects
        self.__food.update(self.__field)
        food_coordinates = self.__food.get_coordinates()

        # clear the game field and move the snake
        self.__field = [[Representation.EMPTY for i in range(self.__rows)] for j in range(self.__columns)]
        if not self.__snake.move():
            # the snake died
            return False

        # getting the current coordinates of the snake object
        snake_coordinates = self.__snake.get_coordinates()

        # setting the representation mode for the food tiles
        for i in range(0, len(food_coordinates)):
            self.__field[food_coordinates[i][0]][food_coordinates[i][1]] = Representation.FOOD

        # check for food collision with the snake
        for i in range(0, len(food_coordinates)):
            if food_coordinates[i][0] == snake_coordinates[0][0] and food_coordinates[i][1] == snake_coordinates[0][1]:
                self.__food.delete_food(food_coordinates[i])
                self.__snake.grow_in_next_round(True)
                break

        # the first element is the head, so mark this special coordinate different than the body
        self.__field[snake_coordinates[0][0]][snake_coordinates[0][1]] = Representation.HEAD_SNAKE

        # set the representation mode for the rest of the snake (except of the head, which is handled a line above)
        for i in range(1, len(snake_coordinates)):
            self.__field[snake_coordinates[i][0]][snake_coordinates[i][1]] = Representation.SNAKE

    # returning the amount of rows
    def get_rows_count(self):
        return self.__rows

    # returning the amount of columns
    def get_columns_count(self):
        return self.__columns

    # returning the representation mode of the tile by the given coordinates
    def get_representation(self, column, row):
        return self.__field[column][row]

    # reset the GameField and the snake (used for restarting the game)
    def reset(self):
        self.__field = [[Representation.EMPTY for i in range(self.__rows)] for j in range(self.__columns)]
        self.__snake = Snake(1, int(self.__rows / 2), self.__columns, self.__rows)

    # returning the length of the snake, which is representing the score
    def get_score(self):
        return self.__snake.get_length()

    # used to print the object (for debugging purposes)
    def __str__(self):
        tmp = ""
        tmp += "Columns: {}\tRows: {}\n".format(str(len(self.__field)), str(len(self.__field[0])))
        for row in range(self.__rows):
            for column in range(self.__columns):
                tmp += "X (Col): {},\tY (Row): {},\tType: {}".format(column, row, self.__field[column][row])
                tmp += "\t\t"
            tmp += "\n"
        tmp += "--------\n"
        for row in range(self.__rows):
            for column in range(self.__columns):
                tmp += str(self.__field[column][row].value) + " "
            tmp += "\n"
        return tmp


if __name__ == '__main__':
    print(GameField(5, 10))
