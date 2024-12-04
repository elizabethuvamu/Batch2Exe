import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class Batch2ExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch2Exe Converter")
        self.root.geometry("400x300")

        # Batch File Selection
        self.bat_file_label = tk.Label(root, text="Select a .bat file:")
        self.bat_file_label.pack(pady=10)

        self.bat_file_entry = tk.Entry(root, width=40)
        self.bat_file_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_bat_file)
        self.browse_button.pack(pady=5)

        # Output Exe File Location
        self.exe_file_label = tk.Label(root, text="Select output .exe file location:")
        self.exe_file_label.pack(pady=10)

        self.exe_file_entry = tk.Entry(root, width=40)
        self.exe_file_entry.pack(pady=5)

        self.browse_exe_button = tk.Button(root, text="Browse", command=self.browse_exe_location)
        self.browse_exe_button.pack(pady=5)

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_batch_to_exe)
        self.convert_button.pack(pady=20)

        # Status Message
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=10)

    def browse_bat_file(self):
        bat_file = filedialog.askopenfilename(filetypes=[("Batch Files", "*.bat")])
        if bat_file:
            self.bat_file_entry.delete(0, tk.END)
            self.bat_file_entry.insert(0, bat_file)

    def browse_exe_location(self):
        exe_file = filedialog.asksaveasfilename(defaultextension=".exe", filetypes=[("Executable Files", "*.exe")])
        if exe_file:
            self.exe_file_entry.delete(0, tk.END)
            self.exe_file_entry.insert(0, exe_file)

    def convert_batch_to_exe(self):
        bat_file = self.bat_file_entry.get()
        exe_file = self.exe_file_entry.get()

        # Check if paths are valid
        if not os.path.isfile(bat_file):
            messagebox.showerror("Error", "Invalid Batch file selected.")
            return

        if not exe_file:
            messagebox.showerror("Error", "Please select an output location for the EXE.")
            return

        # Convert the batch file to an exe using pyinstaller
        try:
            self.status_label.config(text="Converting...", fg="blue")
            subprocess.run(['pyinstaller', '--onefile', '--distpath', os.path.dirname(exe_file), '--name', os.path.basename(exe_file).replace('.exe', ''), bat_file], check=True)
            self.status_label.config(text="Conversion Complete!", fg="green")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Error in conversion", fg="red")
            messagebox.showerror("Error", "Conversion failed. Ensure PyInstaller is installed.")
        except Exception as e:
            self.status_label.config(text="Unexpected error", fg="red")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Batch2ExeConverter(root)
    root.mainloop()
