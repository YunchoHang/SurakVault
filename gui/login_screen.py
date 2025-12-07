import tkinter as tk
from tkinter import messagebox
from core.auth import derive_key
from core.password_vault import load_vault, save_vault
import os
import gui.theme as theme

VAULT_FILE = "data/password_vault.enc"

class LoginScreen:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("SurakVault - Login / Setup")
        self.root.geometry("400x300")
        self.root.configure(bg=theme.BG_COLOR)
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("assets/favicon.ico")
        except Exception as e:
            print("Icon load failed:", e)

        self.key = None
        self.first_time_setup = not os.path.exists(VAULT_FILE)
        self.build_ui()

    def build_ui(self):
        if self.first_time_setup:
            self.build_setup_ui()
        else:
            self.build_login_ui()

    def build_setup_ui(self):
        tk.Label(self.root, text="Setup Master Password", font=theme.TITLE_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_LARGE)

        tk.Label(self.root, text="Enter Master Password:", font=theme.LABEL_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_SMALL)
        self.new_password_entry = tk.Entry(self.root, show="*", width=30, font=theme.ENTRY_FONT)
        self.new_password_entry.pack(pady=theme.PADDING_SMALL)

        tk.Label(self.root, text="Confirm Master Password:", font=theme.LABEL_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_SMALL)
        self.confirm_password_entry = tk.Entry(self.root, show="*", width=30, font=theme.ENTRY_FONT)
        self.confirm_password_entry.pack(pady=theme.PADDING_SMALL)

        tk.Button(self.root, text="Create Vault", width=20, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.create_vault).pack(pady=theme.PADDING_MEDIUM)

        self.new_password_entry.bind("<Return>", lambda e: self.create_vault())
        self.confirm_password_entry.bind("<Return>", lambda e: self.create_vault())

    def build_login_ui(self):
        tk.Label(self.root, text="SecureVault Login", font=theme.TITLE_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_LARGE)

        tk.Label(self.root, text="Enter Master Password:", font=theme.LABEL_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_SMALL)
        self.password_entry = tk.Entry(self.root, show="*", width=30, font=theme.ENTRY_FONT)
        self.password_entry.pack(pady=theme.PADDING_SMALL)
        self.password_entry.focus()

        tk.Button(self.root, text="Unlock Vault", width=20, font=theme.BUTTON_FONT,
                  bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0, relief="raised",
                  command=self.login).pack(pady=theme.PADDING_MEDIUM)

        self.password_entry.bind("<Return>", lambda e: self.login())

    def create_vault(self):
        new_pass = self.new_password_entry.get().strip()
        confirm_pass = self.confirm_password_entry.get().strip()
        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "All fields required!")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        try:
            key = derive_key(new_pass)
            save_vault(key, {})
            self.key = key
            messagebox.showinfo("Success", "Vault created successfully!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vault:\n{e}")

    def login(self):
        master_password = self.password_entry.get().strip()
        if not master_password:
            messagebox.showerror("Error", "Enter master password!")
            return
        try:
            key = derive_key(master_password)
            load_vault(key)
            self.key = key
            messagebox.showinfo("Success", "Vault unlocked!")
            self.root.destroy()
        except Exception:
            messagebox.showerror("Error", "Incorrect master password!")

    def run(self):
        self.root.mainloop()
        return self.key
