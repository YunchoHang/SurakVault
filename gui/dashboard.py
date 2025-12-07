import tkinter as tk
from gui.file_vault_ui import FileVaultUI
from gui.password_vault_ui import PasswordVaultUI
from gui.settings_ui import SettingsUI
import gui.theme as theme

class Dashboard:
    def __init__(self, key):
        self.key_container = {'key': key}

        self.root = tk.Tk()
        self.root.title("SurakVault - Dashboard")
        self.root.geometry("750x550")
        self.root.configure(bg=theme.BG_COLOR)
        self.root.resizable(False, False)
        self.root.iconbitmap("assets/favicon.ico")


        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="SurakVault Dashboard", font=theme.TITLE_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_LARGE)

        notebook = tk.ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=theme.PADDING_MEDIUM, pady=theme.PADDING_SMALL)

        # Use tk.Frame for tabs to support bg
        self.file_vault_tab = tk.Frame(notebook, bg=theme.BG_COLOR)
        self.password_tab   = tk.Frame(notebook, bg=theme.BG_COLOR)
        self.settings_tab   = tk.Frame(notebook, bg=theme.BG_COLOR)

        notebook.add(self.file_vault_tab, text="File Vault")
        notebook.add(self.password_tab, text="Password Vault")
        notebook.add(self.settings_tab, text="Settings")

        FileVaultUI(self.file_vault_tab, self.key_container['key'])
        PasswordVaultUI(self.password_tab, self.key_container['key'])
        SettingsUI(self.settings_tab, self.key_container)
