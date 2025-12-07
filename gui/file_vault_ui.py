import tkinter as tk
from tkinter import filedialog, messagebox
import os
from core.file_vault import encrypt_file, decrypt_file, VAULT_DIR
import gui.theme as theme

class FileVaultUI:
    def __init__(self, parent_tab, key):
        self.key = key
        self.parent_tab = parent_tab
        self.build_ui()
        self.refresh_file_list()

    def build_ui(self):
        self.parent_tab.configure(bg=theme.BG_COLOR)

        # Title
        tk.Label(
            self.parent_tab,
            text="File Encryption / Decryption",
            font=theme.SUBTITLE_FONT,
            bg=theme.BG_COLOR,
            fg=theme.FG_COLOR
        ).pack(pady=theme.PADDING_LARGE)

        # Buttons frame
        btn_frame = tk.Frame(self.parent_tab, bg=theme.BG_COLOR)
        btn_frame.pack(pady=theme.PADDING_MEDIUM)

        btn_style = {"font": theme.BUTTON_FONT, "width": 20, "bg": theme.BUTTON_BG,
                     "fg": theme.BUTTON_FG, "bd": 0, "relief": "raised"}

        tk.Button(btn_frame, text="Encrypt a File", command=self.encrypt_file_dialog, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Decrypt Selected File", command=self.decrypt_selected_file, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected File", command=self.delete_selected_file, **btn_style).pack(side=tk.LEFT, padx=5)

        # Files label
        tk.Label(
            self.parent_tab,
            text="Encrypted Files:",
            font=theme.LABEL_FONT,
            bg=theme.BG_COLOR,
            fg=theme.FG_COLOR
        ).pack(pady=theme.PADDING_SMALL)

        # Files listbox
        self.file_listbox = tk.Listbox(
            self.parent_tab,
            width=60,
            height=15,
            font=theme.LABEL_FONT,
            bg=theme.LISTBOX_BG,
            fg=theme.LISTBOX_FG,
            selectbackground=theme.SELECT_BG,
            selectforeground=theme.SELECT_FG
        )
        self.file_listbox.pack(pady=theme.PADDING_SMALL)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        if not os.path.exists(VAULT_DIR):
            os.makedirs(VAULT_DIR)
        for f in os.listdir(VAULT_DIR):
            if f.endswith(".bin"):
                self.file_listbox.insert(tk.END, f)

    def encrypt_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not file_path: return
        try:
            enc_path = encrypt_file(self.key, file_path)
            messagebox.showinfo("Success", f"File encrypted:\n{enc_path}")
            self.refresh_file_list()
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed:\n{e}")

    def decrypt_selected_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a file to decrypt.")
            return
        filename = self.file_listbox.get(selection[0])
        encrypted_path = os.path.join(VAULT_DIR, filename)

        save_path = filedialog.asksaveasfilename(
            title="Save Decrypted File As",
            defaultextension="",
            initialfile=f"decrypted_{filename.replace('encrypted_', '')}"
        )
        if not save_path: return

        try:
            decrypt_file(self.key, encrypted_path, save_path)
            messagebox.showinfo("Success", f"File decrypted to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed:\n{e}")

    def delete_selected_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a file to delete.")
            return
        filename = self.file_listbox.get(selection[0])
        encrypted_path = os.path.join(VAULT_DIR, filename)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?"):
            try:
                os.remove(encrypted_path)
                messagebox.showinfo("Deleted", f"{filename} has been deleted from the vault.")
                self.refresh_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file:\n{e}")
