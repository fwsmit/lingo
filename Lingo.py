import random
import time
import tkinter as tk
import threading
from tkinter import font as tkFont
from playsound import playsound
import pygame as pg


WORD_LENGTH = 6
BEEP_DELAY = 0.23
BG_COLOR = "#0A2E58"
FG_COLOR = "#0952BB"
RED_COLOR = "#d33038"
YELLOW_COLOR = "#d4b83d"
PADDING = 2

with open("targets.txt") as file:
    DATABASE = [word.strip() for word in file]


def chose_word(words):
    word = random.sample(DATABASE, 1)[0]
    while word in words:
        word = random.sample(DATABASE, 1)[0]
    words.append(word)
    return [x for x in word]


def color_code(guess, word):
    colors = ["R", "B", "B", "B", "B", "B"]
    check_word = word.copy()
    for i in range(len(check_word)):
        if check_word[i] == guess[i]:
            colors[i] = "R"
            check_word[i] = "*"

    for i in range(len(check_word)):
        if check_word[i] != "*":
            if guess[i] in check_word:
                check_word[i] = "*"
                colors[i] = "Y"
    return colors


def draw_letter(root, row, column, color, text):
    font = tkFont.Font(family="MS Sans Serif", size=56, weight="bold")
    border_color = tk.Frame(
        root, highlightbackground=BG_COLOR, highlightthickness=3, bd=0
    )
    c = tk.Canvas(
        root,
        width=160,
        height=160,
        bg=FG_COLOR if color == "X" else BG_COLOR,
        highlightthickness=0,
        highlightbackground=BG_COLOR,
        relief="flat",
    )
    c.grid(row=row, column=column)
    if color == "Y":
        c.create_oval(3, 3, 159, 159, fill=YELLOW_COLOR, outline="")
        c.create_text(80, 80, text=text, fill="white", font=font)
        border_color.grid(row=row, column=column)
    else:
        c.create_rectangle(
            3, 3, 159, 159, fill=RED_COLOR if color == "R" else BG_COLOR, outline=""
        )
        c.create_text(80, 80, text=text, fill="white", font=font)
        border_color.grid(row=row, column=column)


def show_word(root, word, color_code, row, mute, delay):
    pad_grid(root, row)
    for i in range(len(color_code)):
        draw_letter(root, row, i + PADDING, color_code[i], word[i].upper())
        if not mute:
            if color_code[i] == "R":
                red_beep.play()
            elif color_code[i] == "Y":
                yellow_beep.play()
            else:
                blue_beep.play()
        if delay:
            time.sleep(BEEP_DELAY)


def playsound_async(sound):
    threading.Thread(target=playsound, args=(sound,), daemon=True).start()


def pad_grid(root, row):
    for i in range(0, PADDING):
        c = tk.Canvas(
            root,
            width=160,
            height=160,
            bg=BG_COLOR,
            highlightthickness=0,
            highlightbackground=BG_COLOR,
            relief="flat",
        )
        c.grid(row=row, column=i)


def clear(current_window):
    for widget in current_window.winfo_children():
        widget.destroy()
    current_window["bg"] = BG_COLOR


class Lingo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.root = None
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Blik Bier Lingo")
        self.root.attributes("-fullscreen", True)
        self.root["bg"] = BG_COLOR
        self.root.mainloop()


pg.mixer.init()
pg.init()
red_beep = pg.mixer.Sound("sound/Beep (goed).wav")
blue_beep = pg.mixer.Sound("sound/Beep (fout).wav")
yellow_beep = pg.mixer.Sound("sound/Beep (half goed).wav")
victory = pg.mixer.Sound("sound/Lingo Goed Word.mp3")

pg.mixer.set_num_channels(8)

app = Lingo()
time.sleep(1)
app.root.update()
while True:
    used_words = []
    word = chose_word(used_words)
    guess = [word[0], ".", ".", ".", ".", "."]
    turn = 1
    print("Answer:", word)
    show_word(
        app.root, guess, ["R", "B", "B", "B", "B", "B"], turn, mute=True, delay=False
    )
    app.root.update()
    while True:
        while True:
            guess = input("Guess: ")
            if len(guess) != 6:
                print(f"dat woord is niet 6 lang, foei. ga je schamen")
            else:
                break
        colors = color_code(guess, word)
        show_word(app.root, guess, colors, turn, False, True)
        turn += 1
        if all(x == "R" for x in colors):
            print("CORRECT")
            victory.play()
            print("Press enter to play again")
            input()
            break
        w = "".join([word[i] if colors[i] == "R" else "." for i in range(len(guess))])
        show_word(app.root, w, color_code(w, word), turn, True, False)
        turn += 1
        app.root.update()
    clear(app.root)
