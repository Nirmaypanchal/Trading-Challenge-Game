from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import numpy as np
import math


RULES = "1. You are in the crowd and you will trade against each other.\n" \
        "2. The value of the product is calculated on the sum of the dice throws.\n" \
        "3. Each time a dice is thrown, the value of the product changes.\n" \
        "4. The dice throw expires after every time it is thrown, meaning it will stay the same.\n" \
        "5. The dice will be thrown 10 times.\n" \
        "6. Aim for being as quick as possible, there is a timer that takes into account how fast you trade.\n" \
        "7. If you want to buy, you need to click on the amount you want to buy it for.\n" \
        "8. Same goes for selling.\n" \
        "9. You buy or sell the amount indicated in the Bid size/Ask size columns.\n" \
        "10. Remember that you are a market maker, so you buy at ask price and sell at bid price.\n" \
        "11. You must also hedge your transaction for a price of $0.25 per contract\n" \
        "12. Your profit or loss will be indicated on the top. This profit/loss is considered after the transaction costs."


######################################################################################
#------------------------------------ HOME PAGE -------------------------------------#
######################################################################################

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk,Frame.__init__(self, parent)
        background = tk.LabelFrame(self, bg="black", font=("Arial", 10), highlightthickness=0)
        background.pack(fill="both", expand="yes")

        logo = ImageTk.PhotoImage(Image.open("Trading Challenge Simulator.png"))
        app_logo = tk.Label(self, image=logo, highlightthickness=0)
        app_logo.image = logo
        app_logo.place(x=268, y=50)


        play_button = tk.Button(background, text="Let's play!", font = ("Arial Bold", 15), command=lambda: controller.show_frame(GamePage))
        play_button.place(x=500, y=400)

        rules_button = tk.Button(background, text="Rules", font=("Arial Bold", 15), command=lambda:controller.show_frame(RulesPage))
        rules_button.place(x=200, y=400)


######################################################################################
#------------------------------------ GAME PAGE -------------------------------------#
######################################################################################

class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk,Frame.__init__(self, parent)

        self.pnl = 0
        self.dice_value = 35
        self.round = 1

        #label = tk.Label(self, text="Trading Challenge Simulator", font=("Arial Bold", 30))
        self.background = tk.LabelFrame(self, bg="black", font=("Arial", 10), highlightthickness=0)
        self.background.pack(fill="both", expand="yes")

        self.pnl_score = tk.Label(self.background, text="Net P/L: $0", fg="white", bg="black", font=("Arial", 15))
        self.pnl_score.place(x=550, y=50)

        self.expected_value_of_dice = tk.Label(self.background, text="Previous value of dice: 35", fg="white", bg="black", font=("Arial", 15))
        self.expected_value_of_dice.place(x=100, y=50)

        dice_throw = random.randint(1,6)
        self.dice_value = dice_throw - 3.5 + self.dice_value
        dice_image = ImageTk.PhotoImage(Image.open(f"dice{dice_throw}.jpg"))
        self.roll_dice = tk.Label(self, image=dice_image)
        self.roll_dice.image = dice_image
        self.roll_dice.place(x=375,y=30)

        execute_button = tk.Button(self.background, text="Execute trade", font=("Arial Bold", 15),
                                command=self.update_game_page)
        execute_button.place(x=500, y=400)

        quit_button = tk.Button(self.background, text="Quit", font=("Arial Bold", 15),
                                 command=lambda: controller.show_frame(HomePage))
        quit_button.place(x=200, y=400)

        ########################################################################
        #-------------------------- Bid-Ask Table UI --------------------------#
        ########################################################################

        self.anchorx = 260
        self.anchory = 200
        self.bid_1 = IntVar()
        self.bid_2 = IntVar()
        self.bid_3 = IntVar()
        self.bid_4 = IntVar()
        self.selected_bids = [self.bid_1, self.bid_2, self.bid_3, self.bid_4]
        self.ask_1 = IntVar()
        self.ask_2 = IntVar()
        self.ask_3 = IntVar()
        self.ask_4 = IntVar()
        self.selected_asks = [self.ask_1, self.ask_2, self.ask_3, self.ask_4]

        self.bid_ask = [["Bid Size", "Bid Price", "Ask Price", "Ask Size"], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.bid_ask_table = [["Bid Size", "Bid Price", "Ask Price", "Ask Size"], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        self.update_bid_ask()


    def update_bid_ask(self):
        for row in range(5):
            for column in range(4):
                if row == 1:
                    self.bid_ask_table[0][0] = Label(self.background, text=f"{self.bid_ask[0][0]}",
                                                                bg="black", fg="white", font=("Arial Bold", 20))
                    self.bid_ask_table[0][0].place(x=self.anchorx - 150, y=self.anchory-30)

                    self.bid_ask_table[0][1] = Label(self.background, text=f"{self.bid_ask[0][1]}",
                                                     bg="black", fg="white", font=("Arial Bold", 20))
                    self.bid_ask_table[0][1].place(x=self.anchorx, y=self.anchory - 30)

                    self.bid_ask_table[0][2] = Label(self.background, text=f"{self.bid_ask[0][2]}",
                                                     bg="black", fg="white", font=("Arial Bold", 20))
                    self.bid_ask_table[0][2].place(x=self.anchorx + 150, y=self.anchory - 30)

                    self.bid_ask_table[0][3] = Label(self.background, text=f"{self.bid_ask[0][3]}",
                                                     bg="black", fg="white", font=("Arial Bold", 20))
                    self.bid_ask_table[0][3].place(x=self.anchorx + 300, y=self.anchory - 30)

                if column == 0:
                    if row == 1:
                        self.bid_ask[row][column] = random.randint(3,10)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx - 120, y=self.anchory)
                    elif row == 2:
                        self.bid_ask[row][column] = random.randint(7, 13)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx - 120, y=self.anchory+25)
                    elif row == 3:
                        self.bid_ask[row][column] = random.randint(10, 17)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx - 120, y=self.anchory + 50)
                    elif row == 4:
                        self.bid_ask[row][column] = random.randint(15, 25)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx - 120, y=self.anchory + 75)

                if column == 3:
                    if row == 1:
                        self.bid_ask[row][column] = random.randint(3,10)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx + 330, y=self.anchory)
                    elif row == 2:
                        self.bid_ask[row][column] = random.randint(7, 13)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx + 330, y=self.anchory+25)
                    elif row == 3:
                        self.bid_ask[row][column] = random.randint(10, 17)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx + 330, y=self.anchory + 50)
                    elif row == 4:
                        self.bid_ask[row][column] = random.randint(15, 25)
                        self.bid_ask_table[row][column] = Label(self.background, text=f"{self.bid_ask[row][column]}",
                                                                bg="black", fg="white", font=("Arial", 15))
                        self.bid_ask_table[row][column].place(x=self.anchorx + 330, y=self.anchory + 75)

                if column == 1:
                    if row == 1:
                        value = np.random.default_rng().normal(self.dice_value - 1, 2, 1)[0]
                        if value % 1 < 0.25:
                            value = math.floor(value)
                        elif value % 1 < 0.75:
                            value = math.floor(value) + 0.5
                        else:
                            value = math.ceil(value)
                        self.bid_ask[row][column] = value
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.bid_1)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 10, y=self.anchory)

                    elif row == 2:
                        self.bid_ask[row][column] = self.bid_ask[1][1] - 0.5
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.bid_2, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 10, y=self.anchory+25)

                    elif row == 3:
                        self.bid_ask[row][column] = self.bid_ask[1][1] - 1
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.bid_3, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 10, y=self.anchory + 50)
                    elif row == 4:
                        self.bid_ask[row][column] = self.bid_ask[1][1] - 1.5
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.bid_4, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 10, y=self.anchory + 75)

                if column == 2:
                    if row == 1:
                        value = np.random.default_rng().normal(self.dice_value + 1, 2, 1)[0]
                        if value % 1 < 0.25:
                            value = math.floor(value)
                        elif value % 1 < 0.75:
                            value = math.floor(value) + 0.5
                        else:
                            value = math.ceil(value)
                        self.bid_ask[row][column] = value
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.ask_1)
                        self.bid_ask_table[row][column].place(x=self.anchorx+160, y=self.anchory)
                    elif row == 2:
                        self.bid_ask[row][column] = self.bid_ask[1][2] + 0.5
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.ask_2, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 160, y=self.anchory+25)

                    elif row == 3:
                        self.bid_ask[row][column] = self.bid_ask[1][2] + 1
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.ask_3, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 160, y=self.anchory + 50
                                                              )
                    elif row == 4:
                        self.bid_ask[row][column] = self.bid_ask[1][2] + 1.5
                        self.bid_ask_table[row][column] = Checkbutton(self.background, bg="black", fg="white",
                                                                      text=f"$ {self.bid_ask[row][column]}",
                                                                      font=("Arial", 15), onvalue=1, offvalue=0,
                                                                      variable=self.ask_4, command=self.toggle_other_boxes)
                        self.bid_ask_table[row][column].place(x=self.anchorx + 160, y=self.anchory + 75)


    #Function that executes the trade
    def update_game_page(self):
        self.show_popup()
        self.clear_switches()
        self.round += 1
        if self.pnl >= 0:
            self.pnl_score.config(text=f"Net P/L: ${self.pnl}", fg="green")
        else:
            self.pnl_score.config(text=f"Net P/L: ${self.pnl}", fg="red")
        self.expected_value_of_dice.config(text=f"Previous value of dice: {self.dice_value}")

        dice_throw = random.randint(1,6)
        self.dice_value = dice_throw - 3.5 + self.dice_value
        new_dice = ImageTk.PhotoImage(Image.open(f"dice{dice_throw}.jpg"))
        self.roll_dice = tk.Label(self, image=new_dice)
        self.roll_dice.image = new_dice
        self.roll_dice.place(x=375,y=30)

        self.update_bid_ask()


    def clear_switches(self):
        self.bid_1.set(0)
        self.bid_2.set(0)
        self.bid_3.set(0)
        self.bid_4.set(0)

        self.ask_1.set(0)
        self.ask_2.set(0)
        self.ask_3.set(0)
        self.ask_4.set(0)


    def toggle_other_boxes(self):
        if self.bid_2.get() == 1:
            self.bid_1.set(1)
        elif self.bid_3.get() == 1:
            self.bid_1.set(1)
            self.bid_2.set(1)
        elif self.bid_4.get() == 1:
            self.bid_1.set(1)
            self.bid_2.set(1)
            self.bid_3.set(1)

        if self.ask_2.get() == 1:
            self.ask_1.set(1)
        elif self.ask_3.get() == 1:
            self.ask_1.set(1)
            self.ask_2.set(1)
        elif self.ask_4.get() == 1:
            self.ask_1.set(1)
            self.ask_2.set(1)
            self.ask_3.set(1)


    def show_popup(self):
        print_string = ""
        for i in range(4):
            check_selected_bid = self.selected_bids[i].get()
            if check_selected_bid == 1:
                expected_dice_value = self.dice_value
                bid_price = self.bid_ask[i+1][1]
                bid_amount = self.bid_ask[i+1][0]
                net_pnl = (bid_price - expected_dice_value - 0.25)*bid_amount
                print_string += f"Your order: Sell {bid_amount} at ${bid_price}, \n" \
                                f"Expected value of the dice = {expected_dice_value}, \n" \
                                f"Net P/L = (${bid_price} - ${self.dice_value} - $0.25)*{bid_amount} = ${net_pnl}\n\n"
                self.pnl += net_pnl

            check_selected_ask = self.selected_asks[i].get()
            if check_selected_ask == 1:
                expected_dice_value = self.dice_value
                ask_price = self.bid_ask[i+1][2]
                ask_amount = self.bid_ask[i+1][3]
                net_pnl = (expected_dice_value - ask_price - 0.25)*ask_amount
                print_string += f"Your order: Buy {ask_amount} at ${ask_price}, \n" \
                                f"Expected value of the dice = {expected_dice_value}, \n" \
                                f"Net P/L = (${self.dice_value} - ${ask_price} - $0.25)*{ask_amount} = ${net_pnl}\n\n"
                self.pnl += net_pnl

        popup = messagebox.showinfo(f"Your P/L calculations for round {self.round}", f"{print_string}")



######################################################################################
#----------------------------------- RULES PAGE -------------------------------------#
######################################################################################

class RulesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk,Frame.__init__(self, parent)

        #label = tk.Label(self, text="Trading Challenge Simulator", font=("Arial Bold", 30))
        background = tk.LabelFrame(self, bg="black", font=("Arial", 10), highlightthickness=0)
        background.pack(fill="both", expand="yes")

        rules_frame = tk.LabelFrame(background, text="Rules", fg="white", bg="black", font=("Arial Bold", 25, "bold"), highlightthickness=0, height=100, width=100)
        rules_frame.place(x=40, y=50)

        rules = tk.Label(rules_frame, text=RULES, fg="white", bg="black", font=("Arial", 15), justify=LEFT)
        rules.pack()

        play_button = tk.Button(background, text="Let's play!", font=("Arial Bold", 15),
                                command=lambda: controller.show_frame(GamePage))
        play_button.place(x=500, y=400)



        quit_button = tk.Button(background, text="Home", font=("Arial Bold", 15),
                                command=lambda: controller.show_frame(HomePage))
        quit_button.place(x=200, y=400)

######################################################################################
#---------------------------------- APPLICATION -------------------------------------#
######################################################################################

class Application(tk.Tk):
     def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.config(bg="black")
        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)
        window.pack()


        self.frames = {}
        for page in (HomePage, GamePage, RulesPage):
            frame = page(window, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

     def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

app = Application()

app.mainloop()
