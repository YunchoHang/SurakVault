import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
from core.crypto import derive_key
from core.password_vault import load_vault, save_vault
from core.file_vault import VAULT_DIR, reencrypt_file_vault
import gui.theme as theme

class SettingsUI:
    def __init__(self, parent_tab, key_container):
        """
        key_container: dict containing 'key', so that the key can be updated on password change
        """
        self.parent_tab = parent_tab
        self.key_container = key_container
        self.build_ui()

    def build_ui(self):
        self.parent_tab.configure(bg=theme.BG_COLOR)

        tk.Label(self.parent_tab, text="Settings", font=theme.TITLE_FONT,
                 bg=theme.BG_COLOR, fg=theme.FG_COLOR).pack(pady=theme.PADDING_LARGE)

        tk.Button(self.parent_tab, text="Change Master Password", font=theme.BUTTON_FONT,
                  width=25, bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0,
                  relief="raised", command=self.change_master_password).pack(pady=theme.PADDING_SMALL)

        tk.Button(self.parent_tab, text="Backup Vault", font=theme.BUTTON_FONT,
                  width=25, bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0,
                  relief="raised", command=self.backup_vault).pack(pady=theme.PADDING_SMALL)

        tk.Button(self.parent_tab, text="Exit", font=theme.BUTTON_FONT,
                  width=25, bg=theme.BUTTON_BG, fg=theme.BUTTON_FG, bd=0,
                  relief="raised", command=self.parent_tab.quit).pack(pady=theme.PADDING_LARGE)

    def change_master_password(self):
        dialog = tk.Toplevel(self.parent_tab)
        dialog.title("Change Master Password")
        dialog.geometry("350x300")
        dialog.resizable(False, False)
        dialog.configure(bg=theme.BG_COLOR)

        tk.Label(dialog, text="Current Password:", bg=theme.BG_COLOR, fg=theme.FG_COLOR,
                 font=theme.LABEL_FONT).pack(pady=5)
        current_var = tk.StringVar()
        tk.Entry(dialog, textvariable=current_var, show="*", font=theme.ENTRY_FONT, width=25).pack(pady=5)

        tk.Label(dialog, text="New Password:", bg=theme.BG_COLOR, fg=theme.FG_COLOR,
                 font=theme.LABEL_FONT).pack(pady=5)
        new_var = tk.StringVar()
        tk.Entry(dialog, textvariable=new_var, show="*", font=theme.ENTRY_FONT, width=25).pack(pady=5)

        tk.Label(dialog, text="Confirm New Password:", bg=theme.BG_COLOR, fg=theme.FG_COLOR,
                 font=theme.LABEL_FONT).pack(pady=5)
        confirm_var = tk.StringVar()
        tk.Entry(dialog, textvariable=confirm_var, show="*", font=theme.ENTRY_FONT, width=25).pack(pady=5)

        def save_new_password():
            current = current_var.get().strip()
            new = new_var.get().strip()
            confirm = confirm_var.get().strip()

            if not current or not new or not confirm:
                messagebox.showerror("Error", "All fields required!")
                return
            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match!")
                return
            try:
                load_vault(self.key_container['key'])
            except Exception:
                messagebox.showerror("Error", "Current password is incorrect!")
                return
            try:
                new_key = derive_key(new)
                vault_data = load_vault(self.key_container['key'])
                save_vault(new_key, vault_data)
                reencrypt_file_vault(self.key_container['key'], new_key)
                self.key_container['key'] = new_key
                messagebox.showinfo("Success", "Master password changed successfully!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password:\n{e}")

        tk.Button(dialog, text="Save", font=theme.BUTTON_FONT, bg=theme.BUTTON_BG, fg=theme.BUTTON_FG,
                  width=20, bd=0, relief="raised", command=save_new_password).pack(pady=15)

    def backup_vault(self):
        backup_dir = filedialog.askdirectory(title="Select Backup Location")
        if not backup_dir: return
        try:
            # Backup file vault
            file_vault_backup = os.path.join(backup_dir, "vault_files_backup")
            os.makedirs(file_vault_backup, exist_ok=True)
            for f in os.listdir(VAULT_DIR):
                shutil.copy(os.path.join(VAULT_DIR, f), file_vault_backup)

            # Backup password vault
            from core.password_vault import VAULT_FILE
            shutil.copy(VAULT_FILE, backup_dir)

            messagebox.showinfo("Success", f"Vault backup completed at {backup_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed:\n{e}")
