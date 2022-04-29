from tkinter import *
import random, time

class Snake:
    def __init__(self, root, color):
        self.color = color
        self.root = root
        self.x = 0
        self.y = 0
        self.blocks = []
        self.coords = []
        self.key_history = ["Nothing"]
        self.game_is_over = False
        self.id = self.root.create_rectangle(40, 40, 60, 60,
         outline = "black", width = 5, fill=self.color)
        self.position = self.root.coords(self.id)
        self.root.bind_all('<KeyPress-Up>', self.turn_up)
        self.root.bind_all('<KeyPress-Down>', self.turn_down)
        self.root.bind_all('<KeyPress-Left>', self.turn_left)
        self.root.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.position = self.root.coords(self.id)
        self.root.move(self.id, self.x, self.y)
        self.coords.insert(0, self.position)
        self.check_hit_wall()
        self.x1 = snake.coords[0][0]
        self.y1 = snake.coords[0][1]
        self.block = self.root.create_rectangle(self.x1, self.y1, self.x1 + 20,
         self.y1 + 20, outline = "black", width = 5, fill=self.color)
        self.blocks.insert(0, self.block)

    def check_hit_wall(self):
        self.position = self.root.coords(self.id)
        if self.position[0] < 0: #Left
            self.change_position(380, self.y1, 400, self.y1 + 20)
        elif self.position[2] > 400: #Right
            self.change_position(0, self.y1, -20, self.y1 + 20)
        elif self.position[1] < 0: #Up
            self.change_position(self.x1, 380, self.x1 + 20, 400)
        elif self.position[3] > 400: #Down
            self.change_position(self.x1, 0, self.x1 + 20, -20)
        for x in range(0, score.score):
            if self.position[0] == self.coords[x+1][0] and self.position[1] == self.coords[x+1][1]:
                self.game_is_over = True

    def change_position(self, x, y, x1, y1):
        root.delete(self.id)
        self.id = self.root.create_rectangle(x, y, x1,
         y1, outline = "black", width = 5, fill=self.color)

    def turn_left(self, event):
        if self.key_history[-1] != "Right":
            self.y = 0
            self.x = -20
            self.key_history.clear
            self.key_history.append("Left")

    def turn_right(self, event):
        if self.key_history[-1] != "Left":
            self.y = 0
            self.x = 20
            self.key_history.clear
            self.key_history.append("Right")

    def turn_up(self, event):
        if self.key_history[-1] != "Down":
            self.x = 0
            self.y = -20
            self.key_history.clear
            self.key_history.append("Up")

    def turn_down(self, event):
        if self.key_history[-1] != "Up":
            self.x = 0
            self.y = 20
            self.key_history.clear
            self.key_history.append("Down")

    def game_restart(self):
        for x in range(0, score.score):
            del self.coords[-1]
            self.root.delete(self.blocks[-1])
            del self.blocks[-1]
        self.root.delete(self.id)
        score.score = 0
        self.key_history.clear()
        self.key_history.append("Nothing")
        self.id = self.root.create_rectangle(40, 40, 60, 60,
         outline = "black", width = 5, fill=self.color)
        self.x = 0
        self.y = 0
        window.update()
        self.game_is_over = False

class Food:
    def __init__(self, root, color):
        self.root = root
        self.color = color
        self.id = self.root.create_rectangle(-20, -20, 0, 0, outline = "black", 
         width = 0, fill = self.color)
        self.x = int(random.choice(range(60, 361, 20)))
        self.y = int(random.choice(range(60, 361, 20)))
        self.root.move(self.id, self.x, self.y)

    def draw(self):
        self.position = self.root.coords(self.id)
        if snake.position == self.position:
            score.score += 1
            self.root.itemconfig(snake.id, width = 0)
            root.delete(self.id)
            self.id = self.root.create_rectangle(-20, -20, 0, 0, outline = "black",
             width = 0, fill = self.color)
            self.x = int(random.choice(range(60, 361, 20)))
            self.y = int(random.choice(range(60, 361, 20)))
            self.root.move(self.id, self.x, self.y)
        else:
            self.root.itemconfig(snake.id, width = 5)
            del snake.coords[-1]
            root.delete(snake.blocks[-1])
            del snake.blocks[-1]

class Score:
    def __init__(self, root, color):
        self.root = root
        self.score = 0
        self.id = self.root.create_text(280, 18,
         text = f"Score: {self.score}", font = ("Arial", 20), fill = color)
    
    def draw(self):
        self.root.itemconfig(score.id, text=f"Score: {self.score}")

window = Tk() #                Window settings
window.title("Snake")
window.resizable(False, False)
root = Canvas(window, background="black",  width=400,
 height=400, highlightthickness=0)
root.pack()
 
food = Food(root, "red") #     Game settings
snake = Snake(root, "white")
score = Score(root, "#00ff42")
fps = 24

while True: #                  Gameloop
    if snake.game_is_over == True:
        snake.game_restart()
    else:
        window.update()
        snake.draw()
        food.draw()
        score.draw()
        time.sleep(1/fps)