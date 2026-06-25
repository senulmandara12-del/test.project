import tkinter as tk
from tkinter import ttk, messagebox

# menu items + prices
menu_items = {
    "Burger": 6.5,
    "Fries": 3.0,
    "Pizza Slice": 4.0,
    "Milkshake": 5.0,
    "Tea": 3.0
}

class SimpleCafe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # window setup
        self.title("Simple Cafe Menu")
        self.geometry("420x360")

        self.order = {}  # stores what the user picks

        # title text
        ttk.Label(self, text="Cafe Menu", font=("Arial",14,"bold")).pack(pady=10)

        # table for menu items
        self.tree = ttk.Treeview(self, columns=("a","b"), show="headings", height=8)
        self.tree.heading("a", text="Item")
        self.tree.heading("b", text="Price")
        self.tree.column("a", width=150)
        self.tree.column("b", width=80)
        self.tree.pack()

        # add items to the table
        for item, price in menu_items.items():
            self.tree.insert("", "end", values=(item, "$"+str(price)))

        # quantity selector
        ttk.Label(self, text="Qty").pack(pady=3)
        self.qty = ttk.Spinbox(self, from_=1, to=10, width=5)
        self.qty.pack()

        # button to add item
        ttk.Button(self, text="Add Item", command=self.add_item).pack(pady=10)

        # total price label
        self.total_lbl = ttk.Label(self, text="Total: $0.00", font=("Arial",12,"bold"))
        self.total_lbl.pack(pady=10)

    def add_item(self):
        # get selected item
        pick = self.tree.selection()

        # if nothing picked
        if pick == ():
            messagebox.showerror("Error", "Pick an item first")
            return

        # get item name + qty
        item = self.tree.item(pick[0])["values"][0]
        qty = int(self.qty.get())

        # add to order dict
        if item in self.order:
            self.order[item] += qty
        else:
            self.order[item] = qty

        # calculate total
        total = 0
        for x in self.order:
            total += self.order[x] * menu_items[x]

        # update total label
        self.total_lbl.config(text="Total: $" + str(round(total,2)))

if __name__ == "__main__":
    app = SimpleCafe()
    app.mainloop()
