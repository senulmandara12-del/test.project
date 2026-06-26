import json
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

ACCOUNTS_FILE = "accounts_gui.json"


# Load / Save Accounts


def load_accounts():
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}   # returns if file missing or broken

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)   # saves accounts to file


# MENU ITEMS (FOODS)


MENU_ITEMS = { 

    # FOODS
    " 1)  Burger": {"price": 6.50, "type": "food"},
    " 2)  Fries": {"price": 3.00, "type": "food"},
    " 3)  Chicken Wrap": {"price": 5.00, "type": "food"},
    " 4)  Fish Nuggets": {"price": 3.50, "type": "food"},
    " 5)  Lasagna": {"price": 5.00, "type": "food"},
    " 6)  Salad": {"price": 4.80, "type": "food"},
    " 7)  Pizza Slice": {"price": 4.00, "type": "food"},
    " 8)  Chicken Nuggets": {"price": 4.50, "type": "food"},
    " 9)  Garlic Bread": {"price": 3.50, "type": "food"},
    "10)  Chicken Burger": {"price": 7.00, "type": "food"},
    "11)  Hot Chips": {"price": 4.50, "type": "food"},
    "12)  Baked potatoes": {"price": 3.00, "type": "food"},
    "13)  Macaroni": {"price": 5.50, "type": "food"},

    # DRINKS
    " 1) Iced Chocolate": {"price": 4.50, "type": "drink"},
    " 2) Smoothie": {"price": 5.50, "type": "drink"},
    " 3) Hot Chocolate": {"price": 4.00, "type": "drink"},
    " 4) Coffee": {"price": 4.20, "type": "drink"},
    " 5) Milkshake": {"price": 5.00, "type": "drink"},
    " 6) Iced Coffee": {"price": 4.80, "type": "drink"},
    " 7) Tea": {"price": 3.00, "type": "drink"}
}

# size price multipliers
SIZE_MULTIPLIERS = {
    "Small": 0.85,
    "Medium": 1.0,
    "Large": 1.25
}


# Main App Window


class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WELOCOME TO THE SCHOOL CAFE ")
        self.geometry("750x500")
        self.resizable(False, False)

        self.accounts = load_accounts()   # loads saved accounts
        self.current_user = None          # stores logged in user

        self.current_order = {}           # stores items in order
        self.current_prices = {}          # stores item prices

        # UI styling setup
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(bg="#f0f4ff")

        self.style.configure("TFrame", background="#f0f4ff")
        self.style.configure("TLabel", background="#f0f4ff", foreground="#222")
        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1f4e79")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1f4e79")
        self.style.configure("Total.TLabel", font=("Segoe UI", 12, "bold"), foreground="#1f4e79")

        self.style.configure("Treeview", background="white", fieldbackground="white")
        self.style.configure("Treeview.Heading", background="#1f4e79", foreground="white")

        # frames for login + menu
        self.login_frame = LoginFrame(self)
        self.menu_frame = MenuFrame(self)

        self.login_frame.pack(fill="both", expand=True)   # show login first

    def switch_to_menu(self, username):
        self.current_user = username
        self.login_frame.pack_forget()
        self.menu_frame.reset_order()     # clears old order
        self.menu_frame.pack(fill="both", expand=True)

    def save_order(self, total):
        if self.current_user not in self.accounts:
            self.accounts[self.current_user] = []

        # saves order history
        self.accounts[self.current_user].append({
            "order": self.current_order.copy(),
            "prices": self.current_prices.copy(),
            "total": total
        })

        save_accounts(self.accounts)
     

# Login Frame


class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)

        ttk.Label(self, text="WELOCOME TO THE SCHOOL CAFE ", style="Title.TLabel").grid(row=0, column=0, columnspan=2)
        ttk.Label(self, text="Students Years 9–13").grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self, text="Username:").grid(row=2, column=0, sticky="e")
        self.user_entry = ttk.Entry(self, width=30)
        self.user_entry.grid(row=2, column=1)

        ttk.Label(self, text="Year Level (9–13):").grid(row=3, column=0, sticky="e")
        self.year_entry = ttk.Entry(self, width=10)
        self.year_entry.grid(row=3, column=1)

        ttk.Button(self, text="Login / Create Account", command=self.login).grid(row=4, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.user_entry.get().strip()
        year = self.year_entry.get().strip()

        if not username:
            return messagebox.showerror("Error", "Enter username.")

        if not year.isdigit() or not (9 <= int(year) <= 13):
            return messagebox.showerror("Error", "Year must be 9–13.")

        # create new account if not exist
        if username not in self.master.accounts:
            self.master.accounts[username] = []
            save_accounts(self.master.accounts)

        self.master.switch_to_menu(username)


# Menu Frame


class MenuFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master

        # LEFT SIDE — menu list
        ttk.Label(self, text="Cafe Menu", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        self.menu_tree = ttk.Treeview(self, columns=("Name", "Price"), show="headings", height=14)
        self.menu_tree.heading("Name", text="Item")
        self.menu_tree.heading("Price", text="Price ($)")
        self.menu_tree.column("Name", width=160)
        self.menu_tree.column("Price", width=80)
        self.menu_tree.grid(row=1, column=0, padx=10)

     
 
        # add menu items to list
        for item, data in MENU_ITEMS.items():
            self.menu_tree.insert("", "end", values=(item, f"{data['price']:.2f}"))
         
        
        # MIDDLE — quantity + customize button
        mid = ttk.Frame(self, padding=10)
        mid.grid(row=1, column=1)

        ttk.Label(mid, text="Quantity:").grid(row=0, column=0)
        self.qty_spin = ttk.Spinbox(mid, from_=1, to=20, width=5)
        self.qty_spin.grid(row=0, column=1)

        ttk.Button(mid, text="Customize & Add", command=self.customize_item).grid(row=1, column=0, columnspan=2, pady=10)

        # RIGHT SIDE — order summary
        ttk.Label(self, text="Current Order", style="Header.TLabel").grid(row=0, column=2, sticky="w")

        order_frame = ttk.Frame(self)
        order_frame.grid(row=1, column=2)

        scroll = ttk.Scrollbar(order_frame, orient="vertical")
        self.order_tree = ttk.Treeview(order_frame, columns=("Item", "Qty", "Price"), show="headings",
                                       height=14, yscrollcommand=scroll.set)
        scroll.config(command=self.order_tree.yview)

        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Qty", text="Qty")
        self.order_tree.heading("Price", text="Total ($)")

        self.order_tree.column("Item", width=160)
        self.order_tree.column("Qty", width=40)
        self.order_tree.column("Price", width=70)

        self.order_tree.grid(row=0, column=0)
        scroll.grid(row=0, column=1, sticky="ns")

        self.total_label = ttk.Label(self, text="Total: $0.00", style="Total.TLabel")
        self.total_label.grid(row=2, column=2, sticky="e", padx=10)

        # bottom buttons
        bottom = ttk.Frame(self, padding=10)
        bottom.grid(row=3, column=0, columnspan=3)

        ttk.Button(bottom, text="Confirm & Show Invoice", command=self.show_invoice).grid(row=0, column=0, padx=5)
        ttk.Button(bottom, text="Clear Order", command=self.clear_order).grid(row=0, column=1, padx=5)
        ttk.Button(bottom, text="Pay Now", command=self.pay_now).grid(row=0, column=2, padx=5)
        ttk.Button(bottom, text="Logout", command=self.logout).grid(row=0, column=3, padx=5)

        self.grid_columnconfigure(1, weight=1)

    # resets order list
    def reset_order(self):
        self.master.current_order = {}
        self.master.current_prices = {}
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        self.update_total()
 

    # opens customize window
    def customize_item(self):
        selected = self.menu_tree.selection()
        if not selected:
         return messagebox.showerror("Error", "Select an item.")


        base_name = self.menu_tree.item(selected[0])["values"][0]
        base_price = MENU_ITEMS[base_name]["price"]
        item_type = MENU_ITEMS[base_name]["type"]

        qty = int(self.qty_spin.get())

        win = tk.Toplevel(self)
        win.title(f"Customize {base_name}")
        win.geometry("360x360")
        win.configure(bg="#f0f4ff")

        ttk.Label(win, text=f"Customize: {base_name}", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # SIZE OPTIONS
        size_var = tk.StringVar(value="Medium")
        size_frame = ttk.Frame(win)
        size_frame.pack()
        ttk.Label(size_frame, text="Size:").grid(row=0, column=0)

        col = 1
        for s in ["Small", "Medium", "Large"]:
            ttk.Radiobutton(size_frame, text=s, value=s, variable=size_var).grid(row=0, column=col)
            col += 1

        # EXTRAS
        extras_frame = ttk.Frame(win)
        extras_frame.pack(pady=10)

        ttk.Label(extras_frame, text="Extras:").grid(row=0, column=0, sticky="w")

        extra_vars = {}
        row = 1

        if item_type == "food":
            extras = {"Extra Cheese": 1.00, "Extra Sauce": 0.50}
        else:
            extras = {"Whipped Cream": 1.50, "Extra Ice": 0.50, "High Sugar": 1.00}

        for name, cost in extras.items():
            var = tk.BooleanVar()
            label = name if cost == 0 else f"{name} (+${cost:.2f})"
            ttk.Checkbutton(extras_frame, text=label, variable=var).grid(row=row, column=0, sticky="w")
            extra_vars[name] = (var, cost)
            row += 1

        # confirm button
        def confirm():
            size = size_var.get()
            price = base_price * SIZE_MULTIPLIERS[size]

            chosen = []
            for name, (var, cost) in extra_vars.items():
                if var.get():
                    price += cost
                    chosen.append(name)

            label = f"{size} {base_name}"
            if chosen:
                label += " (" + ", ".join(chosen) + ")"

            self.add_custom_item(label, price, qty)
            win.destroy()

        ttk.Button(win, text="Add to Order", command=confirm).pack(pady=10)

    # adds customized item to order
    def add_custom_item(self, label, price, qty):
        self.master.current_order[label] = self.master.current_order.get(label, 0) + qty
        self.master.current_prices[label] = price
        self.refresh_order_view()
  


    # refreshes order list UI
    def refresh_order_view(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        for item, qty in self.master.current_order.items():
            total = self.master.current_prices[item] * qty
            self.order_tree.insert("", "end", values=(item, qty, f"{total:.2f}"))

        self.update_total()

    # updates total price
    def update_total(self):
        total = sum(self.master.current_prices[i] * q for i, q in self.master.current_order.items())
        self.total_label.config(text=f"Total: ${total:.2f}")
        return total

    # clears order
    def clear_order(self):
        self.reset_order()

    # PAYMENT WINDOW
    def pay_now(self):
        if not self.master.current_order:
            return messagebox.showerror("Error", "No items.")

        total = self.update_total()

        win = tk.Toplevel(self)
        win.title("Payment Method")
        win.geometry("300x200")
        win.configure(bg="#f0f4ff")

        ttk.Label(win, text=f"Total: ${total:.2f}", font=("Segoe UI", 12, "bold")).pack(pady=10)

        ttk.Button(win, text="Pay with Cash",
                   command=lambda: self.finish_payment(win, "Cash")).pack(pady=10)

        ttk.Button(win, text="Pay with Card",
                   command=lambda: self.card_payment_window(total, win)).pack(pady=10)

    # card payment window
    def card_payment_window(self, total, parent):
        parent.destroy()

        win = tk.Toplevel(self)
        win.title("Card Payment")
        win.geometry("320x260")
        win.configure(bg="#f0f4ff")

        ttk.Label(win, text="Enter Card Details", font=("Segoe UI", 12, "bold")).pack(pady=10)

        ttk.Label(win, text="Card Number:").pack()
        card_entry = ttk.Entry(win)
        card_entry.pack()

        ttk.Label(win, text="Expiry (MM/YY):").pack()
        expiry_entry = ttk.Entry(win)
        expiry_entry.pack()

        ttk.Label(win, text="CVV:").pack()
        cvv_entry = ttk.Entry(win, show="*")
        cvv_entry.pack()

        def confirm():
            if len(card_entry.get()) < 8:
                return messagebox.showerror("Error", "Invalid card number.")
            messagebox.showinfo("Success", "Card payment approved!")
            self.finish_payment(win, "Card")

        ttk.Button(win, text="Pay Now", command=confirm).pack(pady=15)

    # finishes payment + shows receipt
    def finish_payment(self, win, method):
        win.destroy()
        total = self.update_total()
        self.master.save_order(total)

        now = datetime.datetime.now().strftime("%d/%m/%Y  %I:%M %p")

        invoice = []
        invoice.append("---------------------------------")
        invoice.append("        SCHOOL CAFE RECEIPT")
        invoice.append("---------------------------------n")
        invoice.append(f"Customer: {self.master.current_user}")
        invoice.append(f"Date: {now}\n")
        invoice.append("Items:")

        for item, qty in self.master.current_order.items():
            price = self.master.current_prices[item] * qty
            invoice.append(f"• {item} x{qty} — ${price:.2f}")

        invoice.append("\n--------------------------------")
        invoice.append(f"TOTAL PAID: ${total:.2f}")
        invoice.append(f"Payment Method: {method}")
        invoice.append("--------------------------------\n")
        invoice.append("Thank you for your order!")
        invoice.append("Enjoy your meal ")

        messagebox.showinfo("Payment Complete", "\n".join(invoice))

        self.clear_order()

    # invoice 
    def show_invoice(self):
        if not self.master.current_order:
            return messagebox.showerror("Error", "No items.")

        total = self.update_total()

        text = "Invoice:\n\n"
        for item, qty in self.master.current_order.items():
            price = self.master.current_prices[item] * qty
            text += f"{item} x{qty} = ${price:.2f}\n"

        text += f"\nTotal: ${total:.2f}"

        messagebox.showinfo("Invoice", text)

    # logout back to login screen
    def logout(self):
        self.master.current_user = None
        self.master.current_order = {}
        self.master.current_prices = {}
        self.pack_forget()
        self.master.login_frame.pack(fill="both", expand=True)


# to run app


if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()
