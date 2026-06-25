import tkinter as tk
from tkinter import ttk, messagebox

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

        self.title("Simple Cafe Menu")
        self.geometry("420x360")

        self.order = {}

        ttk.Label(self, text="Cafe Menu", font=("Arial",14,"bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("a","b"), show="headings", height=8)
        self.tree.heading("a", text="Item")
        self.tree.heading("b", text="Price")
        self.tree.column("a", width=150)
        self.tree.column("b", width=80)
        self.tree.pack()

        for item, price in menu_items.items():
            self.tree.insert("", "end", values=(item, "$"+str(price)))

        ttk.Label(self, text="Qty").pack(pady=3)
        self.qty = ttk.Spinbox(self, from_=1, to=10, width=5)
        self.qty.pack()

        ttk.Button(self, text="Add Item", command=self.add_item).pack(pady=10)

        self.total_lbl = ttk.Label(self, text="Total: $0.00", font=("Arial",12,"bold"))
        self.total_lbl.pack(pady=10)

    def add_item(self):
        pick = self.tree.selection()

        if pick == ():
            messagebox.showerror("Error", "Pick an item first")
            return

        item = self.tree.item(pick[0])["values"][0]
        qty = int(self.qty.get())

        if item in self.order:
            self.order[item] += qty
        else:
            self.order[item] = qty

        total = 0
        for x in self.order:
            total += self.order[x] * menu_items[x]

        self.total_lbl.config(text="Total: $" + str(round(total,2)))

if __name__ == "__main__":
    app = SimpleCafe()
    app.mainloop()
