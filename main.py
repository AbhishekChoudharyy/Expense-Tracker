from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as db
from tkcalendar import DateEntry

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry('800x600')

        self.init_database()
        self.create_widgets()

    def init_database(self):
        self.connection = db.connect("expenseTracker.db")
        self.curr = self.connection.cursor()
        query = '''
        create table if not exists expenses (
            id integer primary key,
            date text,
            name text,
            title text,
            expense real
            )
        '''
        self.curr.execute(query)
        self.connection.commit()

    def create_widgets(self):
        # Labels and Entry fields
        date_label = Label(self.root, text="Date", font=('Arial', 15, 'bold'))
        date_label.grid(row=0, column=0, padx=7, pady=7)
        self.date_entry = DateEntry(self.root, width=12, font=('Arial', 15, 'bold'))
        self.date_entry.grid(row=0, column=1, padx=7, pady=7)

        name_label = Label(self.root, text="Name", font=('Arial', 15, 'bold'))
        name_label.grid(row=1, column=0, padx=7, pady=7)
        self.name_entry = Entry(self.root, font=('Arial', 15, 'bold'))
        self.name_entry.grid(row=1, column=1, padx=7, pady=7)

        title_label = Label(self.root, text="Title", font=('Arial', 15, 'bold'))
        title_label.grid(row=2, column=0, padx=7, pady=7)
        self.title_entry = Entry(self.root, font=('Arial', 15, 'bold'))
        self.title_entry.grid(row=2, column=1, padx=7, pady=7)

        expense_label = Label(self.root, text="Expense", font=('Arial', 15, 'bold'))
        expense_label.grid(row=3, column=0, padx=7, pady=7)
        self.expense_entry = Entry(self.root, font=('Arial', 15, 'bold'))
        self.expense_entry.grid(row=3, column=1, padx=7, pady=7)

        # Buttons
        submit_btn = Button(self.root, text="Submit", command=self.submit_expense, font=('Arial', 15, 'bold'))
        submit_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        view_btn = Button(self.root, text="View All Expenses", command=self.view_expenses, font=('Arial', 15, 'bold'))
        view_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        delete_btn = Button(self.root, text="Delete All Expenses", command=self.delete_selected_expense, font=('Arial', 15, 'bold'))
        delete_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Expenses Treeview
        self.expense_columns = ('ID', 'Date', 'Name', 'Title', 'Expense')
        self.expense_tree = ttk.Treeview(self.root, columns=self.expense_columns, show='headings', height=15)
        for col in self.expense_columns:
            self.expense_tree.heading(col, text=col)
        self.expense_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.expense_tree.bind("<<TreeviewSelect>>", self.on_expense_select)

    def submit_expense(self):
        date = self.date_entry.get()
        name = self.name_entry.get()
        title = self.title_entry.get()
        expense = self.expense_entry.get()

        if date and name and title and expense:
            self.curr.execute("INSERT INTO expenses (date, name, title, expense) VALUES (?, ?, ?, ?)",
                              (date, name, title, expense))
            self.connection.commit()
            self.update_expenses_tree()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def view_expenses(self):
        self.expense_tree.delete(*self.expense_tree.get_children())
        self.curr.execute("SELECT * FROM expenses")
        rows = self.curr.fetchall()
        for row in rows:
            self.expense_tree.insert('', 'end', values=row)

    def delete_selected_expense(self):
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all expenses?")
        if confirmation:
            self.curr.execute("DELETE FROM expenses")
            self.connection.commit()
            self.update_expenses_tree()
            messagebox.showinfo("Success", "All expenses deleted successfully.")
        else:
            messagebox.showinfo("Info", "Deletion canceled.")

    def on_expense_select(self, event):
        selected_item = self.expense_tree.selection()
        if selected_item:
            expense_data = self.expense_tree.item(selected_item, "values")
            if len(expense_data) == 5:
                expense_id, date, name, title, expense = expense_data
                self.date_entry.set_date(date)
                self.name_entry.delete(0, END)
                self.name_entry.insert(0, name)
                self.title_entry.delete(0, END)
                self.title_entry.insert(0, title)
                self.expense_entry.delete(0, END)
                self.expense_entry.insert(0, expense)

    def update_expenses_tree(self):
        self.view_expenses()

if __name__ == "__main__":
    root = Tk()
    app = ExpenseTracker(root)
    root.mainloop()
