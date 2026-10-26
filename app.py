import tkinter as tk
from tkinter import simpledialog

window = tk.Tk()
window.title("Taskflow")
window.geometry("800x500")

#Judul aplikasi
judul = tk.Label(
    window,
    text="Daftar tugas saya",
    font=("Arial", 18, "bold")
    
)
judul.pack(pady=20)

#Tempat menampilkan daftar tugas
daftar_tugas = tk.Frame(window)
daftar_tugas.pack(pady=10)

#fungsi yg dijalankan ketika tombol di klik
def tambah_tugas():
    tugas = simpledialog.askstring(
        "Tambah Tugas",
        "Masukan nama tugas"

    )

    if tugas:
        label_tugas = tk.Label(
            daftar_tugas,
           text=f"• {tugas}",
           font=("Arial", 12,)
        )
        label_tugas.pack(anchor="w", padx=20, pady=3)
        
#Tombol tambah tugas
tombol = tk.Button(
    window,
    text="+Tambah Tugas",
    command=tambah_tugas
    )

tombol.pack(pady=10)

window.mainloop()