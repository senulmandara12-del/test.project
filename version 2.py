import tkinter as tk
from tkinter import ttk, messagebox

# MENU ITEMS (same as Version 3)
MENU_ITEMS = {
    "Burger": 6.50,
    "Fries": 3.00,
    "Chicken Wrap": 5.00,
    "Fish Nuggets": 3.50,
    "Lasagna": 5.00,
    "Salad": 4.80,
    "Pizza Slice": 4.00,
    "Chicken Nuggets": 4.50,
    "Garlic Bread": 3.50,
    "Chicken Burger": 7.00,
    "Hot Chips": 4.50,
    "Baked Potatoes": 3.00,
    "Macaroni": 5.50,

    # Drinks
    "Iced Chocolate": 4.50,
    "Smoothie": 5.50,
    "Hot Chocolate": 4.00,
    "Coffee": 4.20,
    "Milkshake": 5.00,
    "Iced Coffee": 4.80,
    "Tea": 3.00
}


# MAIN APP
class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("School Cafe - Version 2")
        self.geometry("750x500")
        self.resizable(False, False)

        self.current_user = None
        self.current_order = {}

        # Styling
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

        # Frames
        self.login_frame = LoginFrame(self)
        self.menu_frame = MenuFrame(self)

        self.login_frame.pack(fill="both", expand=True)

    def switch_to_menu(self, username):
        self.current_user = username
        self.login_frame.pack_forget()
        self.menu_frame.reset_order()
        self.menu_frame.pack(fill="both", expand=True)


# LOGIN FRAME
class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)

        ttk.Label(self, text="WELCOME TO THE SCHOOL CAFE", style="Title.TLabel").grid(row=0, column=0, columnspan=2)
        ttk.Label(self, text="Students Years 9–13").grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self, text="Username:").grid(row=2, column=0, sticky="e")
        self.user_entry = ttk.Entry(self, width=30)
        self.user_entry.grid(row=2, column=1)

        ttk.Label(self, text="Year Level (9–13):").grid(row=3, column=0, sticky="e")
        self.year_entry = ttk.Entry(self, width=10)
        self.year_entry.grid(row=3, column=1)

        ttk.Button(self, text="Login", command=self.login).grid(row=4, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.user_entry.get().strip()
        year = self.year_entry.get().strip()

        if not username:
            return messagebox.showerror("Error", "Enter username.")
        if not year.isdigit() or not (9 <= int(year) <= 13):
            return messagebox.showerror("Error", "Year must be 9–13.")
  

        self.master.switch_to_menu(username)


# MENU FRAME (Version 3 layout but simpler)
class MenuFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master

        # LEFT — Menu list
        ttk.Label(self, text="Cafe Menu", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        self.menu_tree = ttk.Treeview(self, columns=("Item", "Price"), show="headings", height=14)
        self.menu_tree.heading("Item", text="Item")
        self.menu_tree.heading("Price", text="Price ($)")
        self.menu_tree.column("Item", width=160)
        self.menu_tree.column("Price", width=80)
        self.menu_tree.grid(row=1, column=0, padx=10)

        for item, price in MENU_ITEMS.items():
            self.menu_tree.insert("", "end", values=(item, f"{price:.2f}"))

        # MIDDLE — Quantity + Add button
        mid = ttk.Frame(self, padding=10)
        mid.grid(row=1, column=1)

        ttk.Label(mid, text="Quantity:").grid(row=0, column=0)
        self.qty_spin = ttk.Spinbox(mid, from_=1, to=20, width=5)
        self.qty_spin.grid(row=0, column=1)

        ttk.Button(mid, text="Add Item", command=self.add_item).grid(row=1, column=0, columnspan=2, pady=10)

        # RIGHT — Order summary
        ttk.Label(self, text="Current Order", style="Header.TLabel").grid(row=0, column=2, sticky="w")

        order_frame = ttk.Frame(self)
        order_frame.grid(row=1, column=2)

        scroll = ttk.Scrollbar(order_frame, orient="vertical")
        self.order_tree = ttk.Treeview(order_frame, columns=("Item", "Qty", "Total"), show="headings",
                                       height=14, yscrollcommand=scroll.set)
        scroll.config(command=self.order_tree.yview)

        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Qty", text="Qty")
        self.order_tree.heading("Total", text="Total ($)")

        self.order_tree.column("Item", width=160)
        self.order_tree.column("Qty", width=40)
        self.order_tree.column("Total", width=70)

        self.order_tree.grid(row=0, column=0)
        scroll.grid(row=0, column=1, sticky="ns")

        self.total_label = ttk.Label(self, text="Total: $0.00", style="Total.TLabel")
        self.total_label.grid(row=2, column=2, sticky="e", padx=10)

        # Bottom buttons
        bottom = ttk.Frame(self, padding=10)
        bottom.grid(row=3, column=0, columnspan=3)

        ttk.Button(bottom, text="Show Invoice", command=self.show_invoice).grid(row=0, column=0, padx=5)
        ttk.Button(bottom, text="Clear Order", command=self.clear_order).grid(row=0, column=1, padx=5)
        ttk.Button(bottom, text="Pay Now", command=self.pay_now).grid(row=0, column=2, padx=5)
        ttk.Button(bottom, text="Logout", command=self.logout).grid(row=0, column=3, padx=5)

    # Reset order
    def reset_order(self):
        self.master.current_order = {}
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        self.update_total()

    
    # Add item instantly (no customization)
    def add_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Select an item.")
        
        qty_text = self.qty_spin.get()
        if not qty_text.isdigit():
         return messagebox.showerror("Error", "Invalid quantity")
  


        item = self.menu_tree.item(selected[0])["values"][0]
        price = MENU_ITEMS[item]
        qty = int(self.qty_spin.get())

        if item not in self.master.current_order:
            self.master.current_order[item] = 0
        self.master.current_order[item] += qty

        self.refresh_order_view()


    # Refresh order list
    def refresh_order_view(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        for item, qty in self.master.current_order.items():
            total = MENU_ITEMS[item] * qty
            self.order_tree.insert("", "end", values=(item, qty, f"{total:.2f}"))

        self.update_total()

    # Update total
    def update_total(self):
        total = sum(MENU_ITEMS[i] * q for i, q in self.master.current_order.items())
        self.total_label.config(text=f"Total: ${total:.2f}")
        return total

    # Clear order
    def clear_order(self):
        self.reset_order()

    # Show invoice
    def show_invoice(self):
        if not self.master.current_order:
            return messagebox.showerror("Error", "No items.")

        total = self.update_total()

        text = "Invoice:\n\n"
        for item, qty in self.master.current_order.items():
            price = MENU_ITEMS[item] * qty
            text += f"{item} x{qty} = ${price:.2f}\n"

        text += f"\nTotal: ${total:.2f}"

        messagebox.showinfo("Invoice", text)

    # Payment window
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

    # Card payment
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

    # Finish payment
    def finish_payment(self, win, method):
        win.destroy()
        total = self.update_total()

        receipt = "----- RECEIPT -----\n"
        receipt += f"Customer: {self.master.current_user}\n\n"

        for item, qty in self.master.current_order.items():
            price = MENU_ITEMS[item] * qty
            receipt += f"{item} x{qty} = ${price:.2f}\n"

        receipt += f"\nTOTAL PAID: ${total:.2f}\n"
        receipt += f"Payment Method: {method}\n"
        receipt += "--------------------\n"
        receipt += "Thank you for your order!"

        messagebox.showinfo("Payment Complete", receipt)

        self.clear_order()

    # Logout
    def logout(self):
        self.master.current_user = None
        self.master.current_order = {}
        self.pack_forget()
        self.master.login_frame.pack(fill="both", expand=True)


# RUN APP
if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()
