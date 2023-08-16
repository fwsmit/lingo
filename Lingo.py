import random
import time
import tkinter as tk
import threading
from tkinter import font as tkFont
from playsound import playsound
import pygame as pg


WORD_LENGTH = 6
BEEP_DELAY = 0.20
BG_COLOR = "#0A2E58"
FG_COLOR = "#0952BB"
RED_COLOR = "#d33038"
YELLOW_COLOR = "#d4b83d"
PADDING = 3
d = 1610 / (PADDING + 6)

with open("targets.txt") as file:
    DATABASE = [word.strip() for word in file]
    DATABASE = [word.replace("ij", chr(131)) for word in DATABASE]


def color_code(guess, word):
    colors = ["B", "B", "B", "B", "B", "B"]
    check_word = word.copy()
    for i in range(len(check_word)):
        if check_word[i] == guess[i]:
            colors[i] = "R"
            check_word[i] = "*"

    for i in range(len(check_word)):
        if check_word[i] != "*" and guess[i] in check_word:
            check_word[check_word.index(guess[i])] = "*"
            colors[i] = "Y"
    return colors


def draw_letter(root, row, column, color, text):
    font = tkFont.Font(family="MS Sans Serif", size=56, weight="bold")
    border_color = tk.Frame(
        root, highlightbackground=BG_COLOR, highlightthickness=3, bd=0
    )
    c = tk.Canvas(
        root,
        width=d,
        height=d,
        bg=FG_COLOR if color == "X" else BG_COLOR,
        highlightthickness=0,
        highlightbackground=BG_COLOR,
        relief="flat",
    )
    c.grid(row=row, column=column)
    if color == "Y":
        c.create_oval(3, 3, d, d, fill=YELLOW_COLOR, outline="")
    else:
        c.create_rectangle(
            3, 3, d, d, fill=RED_COLOR if color == "R" else BG_COLOR, outline=""
        )
    c.create_text(
        d / 2, d / 2, text=text.replace(chr(131), "ij"), fill="white", font=font
    )
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
            width=d - 20,
            height=d,
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


pg.init()
pg.mixer.init()
red_beep = pg.mixer.Sound("sound/Beep (goed).wav")
blue_beep = pg.mixer.Sound("sound/Beep (fout).wav")
yellow_beep = pg.mixer.Sound("sound/Beep (half goed).wav")


def game():
    victory = pg.mixer.Sound("sound/Lingo Goed Word.mp3")
    pg.mixer.set_num_channels(8)
    app = Lingo()
    time.sleep(1)
    app.root.update()
    while True:
        used_words = []
        word = [x for x in DATABASE.pop(random.randint(0, len(DATABASE) - 1))]
        red_word = [word[0], ".", ".", ".", ".", "."]
        guess = red_word.copy()
        turn = 1
        print("Answer:", ("".join(word)).replace(chr(131), "ij"))
        show_word(
            app.root, guess, color_code(guess, word), turn, mute=True, delay=False
        )
        app.root.update()
        while True:
            while True:
                guess = input("Guess: ")
                guess = guess.replace("ij", chr(131)).replace("ij", chr(131))
                if len(guess) != 6:
                    print(f"dat woord is niet 6 lang, foei. ga je schamen")
                else:
                    break
            colors = color_code(guess, word)
            red_word = [
                guess[i] if colors[i] == "R" else red_word[i] for i in range(len(guess))
            ]
            # show_word(app.root, ["", "", "", "", "", ""], ["B", "B", "B", "B", "B", "B"], turn, True, False)
            # time.sleep(0.1)
            show_word(app.root, guess, colors, turn, False, True)
            turn += 1
            if all(x == "R" for x in colors):
                print("CORRECT")
                victory.play()
                print("Press enter to play again")
                input()
                break
            show_word(
                app.root, red_word, ["B", "B", "B", "B", "B", "B"], turn, True, False
            )
            if turn == 7:
                print("press enter to show answer")
                input()
                show_word(app.root, word, ["R", "R", "R", "R", "R", "R"], turn-1, False, True)
                print("Press enter to play again")
                input()
                break
            # app.root.update()
        clear(app.root)


game()
