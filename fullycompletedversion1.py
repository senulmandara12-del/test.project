# import tkinter + messagebox
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

# main app class
class SimpleCafe(tk.Tk):
    # setup window
    def __init__(self):
        tk.Tk.__init__(self)

        # window title + size
        self.title("Simple Cafe Menu")
        self.geometry("420x420")

        # store order items
        self.order = {}

        # menu title label
        ttk.Label(self, text="Cafe Menu", font=("Arial",14,"bold")).pack(pady=10)

        # table for menu items
        self.tree = ttk.Treeview(self, columns=("a","b"), show="headings", height=8)
        self.tree.heading("a", text="Item")
        self.tree.heading("b", text="Price")
        self.tree.column("a", width=150)
        self.tree.column("b", width=80)
        self.tree.pack()

        # insert menu items into table
        for item, price in menu_items.items():
            self.tree.insert("", "end", values=(item, "$"+str(price)))

        # quantity label
        ttk.Label(self, text="Qty").pack(pady=3)

        # quantity selector
        self.qty = ttk.Spinbox(self, from_=1, to=10, width=5)
        self.qty.pack()

        # add item button
        ttk.Button(self, text="Add Item", command=self.add_item).pack(pady=10)

        # total price label
        self.total_lbl = ttk.Label(self, text="Total: $0.00", font=("Arial",12,"bold"))
        self.total_lbl.pack(pady=10)

        # BUY NOW button
        ttk.Button(self, text="Buy Now", command=self.buy_now).pack(pady=10)

    # add item to order
    def add_item(self):
        # get selected item
        pick = self.tree.selection()

        # if nothing selected
        if pick == ():
            messagebox.showerror("Error", "Pick an item first")
            return

        # get item name + quantity
        item = self.tree.item(pick[0])["values"][0]
        qty = int(self.qty.get())

        # update order dictionary
        if item in self.order:
            self.order[item] += qty
        else:
            self.order[item] = qty

        # calculate total price
        total = 0
        for x in self.order:
            total += self.order[x] * menu_items[x]

        # update total label
        self.total_lbl.config(text="Total: $" + str(round(total,2)))

    # BUY NOW popup
    def buy_now(self):
        # if no items selected
        if not self.order:
            messagebox.showerror("Error", "No items selected")
            return

        # calculate total
        total = sum(self.order[x] * menu_items[x] for x in self.order)

        # payment window
        win = tk.Toplevel(self)
        win.title("Payment")
        win.geometry("300x200")

        # show total
        ttk.Label(win, text=f"Total: ${round(total,2)}", font=("Arial",12,"bold")).pack(pady=10)

        # cash button
        ttk.Button(win, text="Pay with Cash",
                   command=lambda: self.finish_payment(win, "Cash")).pack(pady=10)

        # card button
        ttk.Button(win, text="Pay with Card",
                   command=lambda: self.finish_payment(win, "Card")).pack(pady=10)

    # finish payment + show receipt
    def finish_payment(self, win, method):
        # close payment window
        win.destroy()

        # calculate total again
        total = sum(self.order[x] * menu_items[x] for x in self.order)

        # build receipt text
        receipt = "----- RECEIPT -----\n"
        for item, qty in self.order.items():
            receipt += f"{item} x{qty} = ${menu_items[item] * qty}\n"

        receipt += f"\nTOTAL PAID: ${round(total,2)}\n"
        receipt += f"Payment Method: {method}\n"
        receipt += "--------------------"

        # show receipt popup
        messagebox.showinfo("Payment Complete", receipt)

        # reset order
        self.order = {}
        self.total_lbl.config(text="Total: $0.00")

# run the app
if __name__ == "__main__":
    app = SimpleCafe()
    app.mainloop()
