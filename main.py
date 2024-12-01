import tkinter as tk
import random

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.bind("<Key>", self.key_handler)
        
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.init_UI()
        self.start_game()

    def init_UI(self):
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack()

        self.score_label = tk.Label(self.score_frame, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.score_frame, text="Restart", font=("Helvetica", 16), command=self.restart_game)
        self.restart_button.pack(side=tk.RIGHT, padx=10)

        self.frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        self.frame.pack()

        self.tiles = []
        for i in range(4):
            row = []
            for j in range(4):
                label = tk.Label(self.frame, text="", bg="white", font=("Helvetica", 24), width=4, height=2)
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.tiles.append(row)

    def start_game(self):
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_UI()

    def restart_game(self):
        self.start_game()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def update_UI(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))
        self.score_label.config(text=f"Score: {self.score}")
        self.root.update_idletasks()

    def get_tile_color(self, value):
        colors = {
            0: "white", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def key_handler(self, event):
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            if self.move(key):
                self.add_new_tile()
                self.update_UI()
                if self.is_game_over():
                    self.game_over()

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        return new_row + [0] * (4 - len(new_row))

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_row_left(self, row):
        row = self.compress(row)
        row = self.merge(row)
        return self.compress(row)

    def move(self, direction):
        rotated = False
        if direction == "Up":
            self.board = list(zip(*self.board))
            rotated = True
        elif direction == "Down":
            self.board = list(zip(*self.board[::-1]))
            rotated = True
        elif direction == "Right":
            self.board = [row[::-1] for row in self.board]

        moved = False
        new_board = []
        for row in self.board:
            new_row = self.move_row_left(row)
            new_board.append(new_row)
            if new_row != row:
                moved = True

        if direction == "Up" or direction == "Down":
            new_board = list(zip(*new_board)) if direction == "Up" else list(zip(*new_board[::-1]))
            new_board = [list(row) for row in new_board]
        elif direction == "Right":
            new_board = [row[::-1] for row in new_board]

        if moved:
            self.board = new_board
        return moved

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def game_over(self):
        self.frame.destroy()
        self.score_frame.destroy()
        game_over_label = tk.Label(self.root, text=f"Game Over!\nFinal Score: {self.score}", bg="red", fg="white", font=("Helvetica", 36))
        game_over_label.pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
