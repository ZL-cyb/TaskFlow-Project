import tkinter as tk
from tkinter import messagebox,simpledialog

window = tk.Tk()
window.title("Taskflow")
window.geometry("800x500")

#fungsi yg dijalankan ketika tombol di klik
def tambah_tugas():
    tugas = simpledialog.askstring(
        "Tambah Tugas",
        "Masukan nama tugas"

    )

    if tugas:
        messagebox.showinfo("Taskflow",f"Tugas ditambahkan:{tugas}")
        
#membuat  tombol  pertama
tombol = tk.Button(
    window,
    text="Tambah Tugas",
    command=tambah_tugas
    )

tombol.pack(pady=20)

window.mainloop()