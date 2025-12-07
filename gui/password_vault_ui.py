import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pyperclip
from core.password_vault import load_vault, add_entry, delete_entry
import gui.theme as theme

class PasswordVaultUI:
    def __init__(self, parent_tab, key):
        self.parent_tab = parent_tab
        self.key = key
        self.vault_data = []
        self.show_passwords = False

        self.build_ui()
        self.refresh_vault_list()

    def build_ui(self):
        self.parent_tab.configure(bg=theme.BG_COLOR)

        tk.Label(self.parent_tab, text="Password Manager", font=theme.TITLE_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_LARGE)

        btn_frame = tk.Frame(self.parent_tab, bg=theme.BG_COLOR)
        btn_frame.pack(pady=theme.PADDING_SMALL)

        tk.Button(btn_frame, text="Add Entry", width=15, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.add_entry_ui).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Search Entry", width=15, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.search_entry_ui).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Entry", width=15, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.delete_selected_entry).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Copy Password", width=15, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.copy_selected_password).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Show/Hide Passwords", width=18, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.toggle_passwords).grid(row=0, column=4, padx=5)

        columns = ("Website", "Username", "Password")
        self.tree = ttk.Treeview(self.parent_tab, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(pady=theme.PADDING_MEDIUM)

    def refresh_vault_list(self):
        self.tree.delete(*self.tree.get_children())
        try:
            self.vault_data = load_vault(self.key)
        except Exception:
            self.vault_data = []

        for entry in self.vault_data:
            pwd_display = entry["password"] if self.show_passwords else "******"
            self.tree.insert("", tk.END, values=(entry["website"], entry["username"], pwd_display))

    def add_entry_ui(self):
        website = simpledialog.askstring("Website", "Enter website/app name:", parent=self.parent_tab)
        if not website: return
        username = simpledialog.askstring("Username", "Enter username/email:", parent=self.parent_tab)
        if username is None: return
        password = simpledialog.askstring("Password", "Enter password:", parent=self.parent_tab, show="*")
        if password is None: return
        try:
            add_entry(self.key, website, username, password)
            self.refresh_vault_list()
            messagebox.showinfo("Success", "Password entry added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry:\n{e}")

    def search_entry_ui(self):
        query = simpledialog.askstring("Search", "Enter website or username:", parent=self.parent_tab)
        if not query: return
        results = [e for e in self.vault_data if query.lower() in e["website"].lower() or query.lower() in e["username"].lower()]
        if not results:
            messagebox.showinfo("Search Results", "No matching entries found.")
            return
        self.tree.delete(*self.tree.get_children())
        for entry in results:
            pwd_display = entry["password"] if self.show_passwords else "******"
            self.tree.insert("", tk.END, values=(entry["website"], entry["username"], pwd_display))

    def delete_selected_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an entry to delete.")
            return
        index = self.tree.index(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if not confirm: return
        try:
            delete_entry(self.key, index)
            self.refresh_vault_list()
            messagebox.showinfo("Success", "Entry deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete entry:\n{e}")

    def copy_selected_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an entry to copy password.")
            return
        index = self.tree.index(selected[0])
        password = self.vault_data[index]["password"]
        try:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy password:\n{e}")

    def toggle_passwords(self):
        self.show_passwords = not self.show_passwords
        self.refresh_vault_list()
