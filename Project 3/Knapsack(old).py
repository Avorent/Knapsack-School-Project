# Although you are given this small example, your code should be able to input a size n matrix
# of weights and values and a knapsack size (read in a file). Here are the steps to complete
# the project:
#
# Step 1. Code an exhaustive search algorithm to find the optimal solution to the above
# problem.
from itertools import combinations
from tkinter import *
import ast

sample1 = (1, 3, 25), (2, 2, 20), (3, 1, 15), (4, 4, 40), (5, 5, 50)


def ex(items, capacity):
    def anycomb(x):
        """ return combinations of any length from the items """
        return (comb
                for r in range(1, len(x) + 1)
                for comb in combinations(x, r)
                )

    def totalvalue(x):
        """ Sums up a combination of items """
        total_weight = total_value = 0
        for i, w, v in x:
            total_weight += w
            total_value += v
        return (total_value, -total_weight) if total_weight <= capacity else (0, 0)

    result = max(anycomb(items), key=totalvalue)  # max val or min wt if values are equal to each other
    val, wt = totalvalue(result)
    answer = ('\n\n Finished! The optimal set of items is/are:\n       Item ' +
              '\n       Item '.join(sorted(str(Item) for Item, _, _ in result)) +
              '\n for a maximum value of {} and a total weight of {}'.format(val, -wt))
    return str(answer)

# Step 2. Code a DP method to find the optimal solution to the problem.


def dyn(items, capacity):
    K = [[0 for x in range(capacity + 1)] for x in range(len(items) + 1)]
    # wt = [items[i][1] for i in range(len(items))]
    # val = [items[i][2] for i in range(len(items))]
    # tw = 0
    # Build table K[][] in bottom up manner
    for i in range(len(items)+1):
        _, wt, val = items[i-1]
        for w in range(capacity+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif wt <= w:
                K[i][w] = max(val + K[i-1][w-wt],  K[i-1][w])

            else:
                K[i][w] = K[i-1][w]

    result = []
    maxw = capacity
    for j in range(len(items), 0, -1):
        was_added = K[j][maxw] != K[j-1][maxw]

        if was_added:
            item, wt, val = items[j-1]
            result.append(items[j-1])
            maxw -= wt

    val, wt = result
    answer = ('\n\n Finished! The optimal set of items is/are:\n       Item ' +
              '\n       Item '.join(sorted(str(result) for _, _ in result)) +
              '\n for a maximum value of {} and a total weight of {}'.format(val, -wt))
    return str(answer)

# Step 3. Code your chosen method to find the optimal solution to the problem.

# Step 4. Be sure to create a user friendly menu (no crashing and easy exit, read knapsack
# data from a file).


class KnapsackUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="SkyBlue")
        self.DialogText = ""
        self.menu()
        self.currentSample = [sample1, 6]
        with open('input.txt', 'r') as f:
            x = f.read().splitlines()
            self.inputCap = ast.literal_eval(x[0])

            ranges = [x for x in range(len(ast.literal_eval(x[1]))+1)]

            self.inputSample = tuple(zip(ranges[1:], ast.literal_eval(x[1]), ast.literal_eval(x[2])))

    def menu(self):

        self.knapimg = Label(self, image=sack, bg="SkyBlue")
        self.knapimg.pack(side="top")

        self.q = Button(self, text="EXIT", fg="GhostWhite", bg="Crimson", activebackground="GhostWhite", activeforeground="Crimson", command=root.destroy)
        self.h = Button(self, text="HELP", fg="DarkRed", bg="LightCoral", activebackground="DarkRed", activeforeground="LightCoral", command=self.tutorial)
        self.c = Button(self, text="RECURSION", fg="Sienna", bg="Wheat", activebackground="Sienna", activeforeground="Wheat")
        self.DP = Button(self, text="DYNAMIC PROGRAMMING", fg="DarkSlateGray", bg="LightGreen", activebackground="DarkSlateGray", activeforeground="LightGreen", command=self.dp)
        self.ex = Button(self, text="EXHAUSTIVE", fg="DarkSlateGray", bg="MediumSpringGreen", activebackground="DarkSlateGray", activeforeground="MediumSpringGreen", command=self.exhaust)
        MainMenuButtons = [self.q, self.h, self.c, self.DP, self.ex]

        self.introTitle = Label(self, text="The Knapsack", fg="White", bg="SkyBlue")
        self.Title(self.introTitle)

        self.introText = Label(self, text="Which algorithm method would you like to try for this Knapsack problem?", fg="DarkSlateGrey", bg="SkyBlue")
        self.introText.config(font=("Georgia", 12))
        self.introText.pack(side="top", fill='y', expand=0)
        self.pack()
        for x in MainMenuButtons:
            self.expandBottom(x)

    def tutorial(self):
        # display text
        t = Toplevel(self)
        t.title("Knapsack: Tutorial")
        t.resizable(0, 0)

        t.Title = Label(t, text="Sorry!", fg="Maroon", bg="HoneyDew")
        self.Title(t.Title)

        t.Body1 = Label(t, text="Exhaustive Algorithm", fg="Brown", bg="PapayaWhip")
        self.Body(t.Body1)

        t.Body2 = Label(t, text="Dynamic Programming Algorithm", fg="Maroon", bg="Wheat")
        self.Body(t.Body2)

        t.Body3 = Label(t, text="Recursion Algorithm", fg="MistyRose", bg="LightSalmon")
        self.Body(t.Body3)

        t.Body4 = Label(t, text="Navigation", fg="MistyRose", bg="LightCoral")
        self.Body(t.Body4)

        t.exit = Button(t, text="THANKS", fg="GhostWhite", bg="Crimson", activebackground="GhostWhite", activeforeground="Crimson", command=t.destroy)
        self.expandBottom(t.exit)

        self.limitwindows(t)

    def exhaust(self):
        t = Toplevel()
        t.title("Knapsack: Exhaustive Algorithm")
        t.geometry(f'{int(width/2)}x{int(height/2)}')
        t.resizable(0,0)
        t.config(bg="DarkSlateGrey")
        x = Text(t, fg="DarkSlateGrey", bg="Ivory")
        t.Title = Label(t, text="Knapsack: Exhaustive Algorithm", fg="MediumSpringGreen", bg="DarkSlateGrey")
        self.Title(t.Title)

        t.Frame = Frame(t)
        t.Frame.pack(side="bottom", fill='x', expand=0)

        t.Frame.load = Button(t.Frame, text="LOAD FILE", fg="DarkSlateGrey", bg="MediumSpringGreen",
                              activebackground="DarkSlateGrey", activeforeground="MediumSpringGreen", command=lambda: self.updateSample(x))
        self.normalButton(t.Frame.load)
        t.Frame.enter = Button(t.Frame, text="START", fg="DarkSlateGrey", bg="Gold", activebackground="DarkSlateGrey", activeforeground="Gold"
                               , command=lambda: self.calculateExhaust(x))
        self.normalButton(t.Frame.enter)
        t.Frame.exit = Button(t.Frame, text="EXIT", fg="GhostWhite", bg="Crimson", activebackground="GhostWhite", activeforeground="Crimson", command=t.destroy)
        self.normalButton(t.Frame.exit)

        x.config(font=("Georgia", 12), bd=0, width=100, state="disabled")
        x.pack(side="bottom", fill='both', expand='1', padx=10, pady=10)
        self.textintro(x)

        self.limitwindows(t)

    def dp(self):
        t = Toplevel()
        t.title("Knapsack: Exhaustive Algorithm")
        t.geometry(f'{int(width/2)}x{int(height/2)}')
        t.resizable(0,0)
        t.config(bg="DarkSlateGrey")
        x = Text(t, fg="DarkSlateGrey", bg="Ivory")
        t.Title = Label(t, text="Knapsack: Dynamic Programming", fg="MediumSpringGreen", bg="DarkSlateGrey")
        self.Title(t.Title)

        t.Frame = Frame(t)
        t.Frame.pack(side="bottom", fill='x', expand=0)

        t.Frame.load = Button(t.Frame, text="LOAD FILE", fg="DarkSlateGrey", bg="MediumSpringGreen",
                              activebackground="DarkSlateGrey", activeforeground="MediumSpringGreen", command=lambda: self.updateSample(x))
        self.normalButton(t.Frame.load)
        t.Frame.enter = Button(t.Frame, text="START", fg="DarkSlateGrey", bg="Gold", activebackground="DarkSlateGrey", activeforeground="Gold"
                               , command=lambda: self.calculateDP(x))
        self.normalButton(t.Frame.enter)
        t.Frame.exit = Button(t.Frame, text="EXIT", fg="GhostWhite", bg="Crimson", activebackground="GhostWhite", activeforeground="Crimson", command=t.destroy)
        self.normalButton(t.Frame.exit)

        x.config(font=("Georgia", 12), bd=0, width=100, state="disabled")
        x.pack(side="bottom", fill='both', expand='1', padx=10, pady=10)
        self.textintro(x)

        self.limitwindows(t)

    def textintro(self, text):
        self.DialogText = ""
        with open('CurrentSample.txt', 'r') as f:
            self.DialogText = (f.read())
        text.config(state="normal")
        text.insert(END, self.DialogText)
        x = self.currentSample
        for i in range(len(self.currentSample[0])):
            text.insert(END, '\n        Item {} has a weight of {} pounds and has a value of {}.'.format(x[0][i][0], x[0][i][1], x[0][i][2]))
        text.insert(END, '\n\nThe capacity of which how much weight the knapsack can hold is {} pounds.'.format(self.currentSample[1]))
        text.config(state="disabled")

    def updateSample(self, text):
        self.currentSample = [self.inputSample, self.inputCap]
        self.DialogText = ""
        text.config(state="normal")
        text.insert(END, '\n\n Load success! The sample has been updated.'
                         '\n    Here are the new item(s):')
        x = self.currentSample
        for i in range(len(self.currentSample[0])):
            text.insert(END, '\n        Item {} has a weight of {} pounds and has a value of {}.'.format(x[0][i][0], x[0][i][1], x[0][i][2]))
        text.insert(END, '\n\nThe knapsack can now hold {} pounds.'.format(self.currentSample[1]))
        text.see(END)
        text.config(state='disabled')

    def calculateExhaust(self, text):
        self.DialogText = ""
        text.config(state="normal")
        text.insert(END, ex(self.currentSample[0], self.currentSample[1]))
        text.see(END)
        text.config(state='disabled')

    def calculateDP(self, text):
        self.DialogText = ""
        text.config(state="normal")
        text.insert(END, dyn(self.currentSample[0], self.currentSample[1]))
        text.see(END)
        text.config(state='disabled')

    def normalButton(self, Button):
        self.x = Button
        self.x.config(font=("Helvetica", 16, "bold"), bd=0)
        self.x.pack(side="left",fill='x', expand=1, padx=0, pady=0)

    def expandBottom(self, Button):
        self.x = Button
        self.x.config(font=("Helvetica", 16, "bold"), bd=0)
        self.x.pack(side="bottom", fill='x', expand=1, padx=0, pady=0)

    def Title(self, Label):
        self.x = Label
        self.x.config(font=("Helvetica", 50, "bold"))
        self.x.pack(side="top", fill='x', padx=10, pady=10)

    def Body(self, Label):
        self.x = Label
        self.x.config(font=("Georgia", 11))
        self.x.pack(side="top", fill='both', expand=0, anchor=W)

    def limitwindows(self, t):
        t.transient(root)
        t.grab_set()
        root.wait_window(t)


root = Tk()
root.title("The Knapsack")
sack = PhotoImage(file="knapsack1.png")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.resizable(0, 0)


app = KnapsackUI(master=root)
app.mainloop()
