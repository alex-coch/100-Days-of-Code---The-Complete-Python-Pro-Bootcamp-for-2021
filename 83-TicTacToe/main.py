pos = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

def check_winner(str):
    if (pos[0][0] == str and pos[0][1] == str and pos[0][2] == str) or \
        (pos[1][0] == str and pos[1][1] == str and pos[1][2] == str) or \
        (pos[2][0] == str and pos[2][1] == str and pos[2][2] == str) or \
        (pos[0][0] == str and pos[1][0] == str and pos[2][0] == str) or \
        (pos[0][1] == str and pos[1][1] == str and pos[2][1] == str) or \
        (pos[0][2] == str and pos[1][2] == str and pos[2][2] == str) or \
        (pos[0][0] == str and pos[1][1] == str and pos[2][2] == str) or \
        (pos[0][2] == str and pos[1][1] == str and pos[2][0] == str):
        print (f"{str} wins the game")
        return True
    return False
 
def draw_board():
    for row in range(0, 3):
        for col in range(0, 3):
            print(pos[row][col], end=" | ")
        print()
        print("----------")

turns = 9

draw_board()

str = ""

end_of_game = False

while not end_of_game:
    if turns % 2 != 0:
        print("Player 1's turn, X's")
        str = "X"
    else:
        print("Player 2's turn, O's")
        str = "O"

    row = int(input("Enter the row: "))
    col = int(input("Enter the col: "))

    pos[row][col] = str

    if check_winner(str):
        end_of_game = True

    draw_board()
    turns -= 1

    if turns == 0:
        print("It's a draw")
        end_of_game = True