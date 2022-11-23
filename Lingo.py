import tkinter
import random
import tkinter.messagebox
from tkinter import font as tkFont
from playsound import playsound
import threading
import time

class Lingo:

    def __init__(self) -> None:
        self.five_word: list[str] = self.import_words("targets.txt", 5)
        self.six_word: list[str] = self.import_words("targets.txt", 6)
        self.seven_word: list[str] = self.import_words("targets.txt", 7)
        self.ten_word: list[str] = self.import_words("targets.txt", 10)
        self.al_gekozen: list[str] = []
        self.antwoord: str = ""
        self.len: int = 5

    def import_words(self, filename: str, length) -> list[str]:
        with open(filename) as file:
            return [word.strip() for word in file if len(word.strip()) == length]
    
    def chose_word(self) -> None:
        if self.len == 5:
            word_list = self.five_word
        elif self.len == 6:
            word_list = self.six_word
        elif self.len == 7:
            word_list = self.seven_word
        else:
            word_list = self.ten_word

        word = random.sample(word_list, 1)

        while word in self.al_gekozen:
            word = random.sample(word_list)

        self.al_gekozen.append(word)
        self.antwoord = "".join(word)

    def kleur_code(self, guess: str) -> str:
        antwoord = list(self.antwoord)
        kleuren = list("B"*self.len)
        for i in range(self.len):
            if antwoord[i] == guess[i]:
                kleuren[i] = "G"
                antwoord[i] = "*"

        for i in range(self.len):
            if kleuren[i] != "G":
                try:
                    index = antwoord.index(guess[i])
                    antwoord[index] = "*"
                    kleuren[i] = "Y"
                except ValueError:
                    pass

        return "".join(kleuren)

    def correct(self, kleuren: str) -> bool:
        return all(x == "G" for x in kleuren)

    def chose_len(self) -> None:
        getal =  False
        lengte = 0
        while lengte not in (5, 6, 7, 10):
            while getal is False:
                try:
                    lengte = int(input("Hoelang wordt het woord? opties: (5, 6, 7, 10) \n"))
                    getal = True
                except ValueError:
                    print("dat is geen getal")
            if lengte not in (5,6,7,10):
                print("dat is niet een van (5, 6, 7, 10)")
                getal = False
        self.len = lengte

class letter:
    def __init__(self):
        pass

    @staticmethod
    def maak_knop(window,backgr, tekst, row, column):
        border_color = tkinter.Frame(window, highlightbackground = "#223e75", highlightthickness = 2, bd=0)
        helv36 = tkFont.Font(family='MS Sans Serif', size=56, weight='bold')
        if backgr == "#d4b83d":
            #window.after(1000,letter.gele_circel,window, row, column, tekst, helv36)
            letter.gele_circel(window, row, column, tekst, helv36)
        else:
            #window.after(1000,letter.normale_knop, window, tekst, backgr, row, column)
            letter.normale_knop(window, tekst, backgr, row, column)
            

    @staticmethod
    def gele_circel(window, row, column, tekst, helv36):
        border_color = tkinter.Frame(window, highlightbackground = "#223e75", highlightthickness = 2, bd=0)
        c= tkinter.Canvas(window,width=160, height=160, bg='#1673c7', highlightthickness=2, highlightbackground="#223e75", relief='flat')
        c.grid(row=row, column=column)
        #Draw an Oval in the canvas
        c.create_oval(3,3,159,159, fill = '#d4b83d', outline="")
        c.create_text(80, 80, text = tekst, font = helv36, fill='white')
        border_color.grid(row=row, column=column)
        

    @staticmethod
    def normale_knop(window, tekst, backgr, row, column):
        border_color = tkinter.Frame(window, highlightbackground = "#223e75", highlightthickness = 3, bd=0)
        helv36 = tkFont.Font(family='MS Sans Serif', size=56, weight='bold')
        pixel = tkinter.PhotoImage(width=1, height=1)
        button = tkinter.Button(
            border_color,
            text=tekst,
            bg = backgr,
            fg = 'white',
            image=pixel,
            compound='center',
            width=150,
            height=150,
            relief="flat"
        )
        button['font'] = helv36
        button.grid(row=row, column=column)
        border_color.grid(row=row, column=column)

    @staticmethod
    def clear(window):
        for widget in window.winfo_children():
            widget.destroy()
    
    def click(self):
        pass



def create_main_window():

    # create a window for main form of app
    Lingo = tkinter.Tk()

    # title for dialog box
    Lingo.title("Axif Lingo")

    # set form width and height
    form_width = 600
    form_height = 700

    # fix screen width and height
    screen_width = Lingo.winfo_screenwidth()
    screen_height = Lingo.winfo_screenheight()

    # calculate horizontal and vertical offset
    horizontal_offset = \
        int((screen_width/2) - (form_width/2))
    vertical_offset = \
        int((screen_height/2) - (form_height/2))

    # show form in middle of screen
    Lingo.geometry('{0}x{1}+{2}+{3}'.format(form_width,form_height,horizontal_offset,vertical_offset))

    # stop the window being resizable
    Lingo.resizable(True,True)    

    return Lingo

def playsound_async(sound):
    threading.Thread(target=playsound, args=(sound,), daemon=True).start()

def show_word(L, lingo, word, row, delay=False):
        kleuren = L.kleur_code(word)   
        for i in range(len(word)):
            if kleuren[i] == "G":
                backgr = "#d33038"
            elif kleuren[i] == "B":
                backgr = '#1673c7'
            else:
                backgr = "#d4b83d"
            letter.maak_knop(lingo, backgr, word[i].upper(), row = row, column=i)
            if delay:
                lingo.update()
                if kleuren[i] == "G":
                    playsound_async("sound/Beep (goed).wav")
                elif kleuren[i] == "B":
                    playsound_async("sound/Beep (fout).wav")
                else:
                    playsound_async("sound/Beep (half goed).wav")
                time.sleep(0.2)

        return kleuren

def main():
    L = Lingo()
    lingo = create_main_window()
    #tkinter.messagebox.showwarning("showwarning", "Lingo gaat beginnen, ben je er klaar voor?")
    while True:
        #tkinter.messagebox.showwarning("showwarning", "LET'S GO")
        win = False
        L.chose_len()
        L.chose_word()
        letter.clear(lingo)
        first_letter = L.antwoord[0]
        show_word(L, lingo, first_letter+" "*(L.len-1), 0, delay=False)
        row = 0
        while win is False:
            invoer = False
            while invoer is False:
                isn = input("Guess: " )
                if len(isn) != L.len:
                    print(f"dat woord is niet {L.len} lang, foei\n Probeer maar opnieuw")
                elif isn[0] != first_letter:
                    print(f"Eerste letter komt niet overeen")
                else:
                    invoer = True

            kleuren = show_word(L, lingo, isn, row, delay=True)

            print(kleuren)
            row += 1
            if L.correct(kleuren):
                win = True
                playsound_async("sound/Lingo Goed Word.mp3")
        #tkinter.messagebox.showinfo("wow! je hebt het goed :D")

        print("op naar een nieuw potje")



if __name__ == '__main__':
    main()


