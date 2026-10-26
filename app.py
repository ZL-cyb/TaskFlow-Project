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
daftar_tugas.pack(pady=10, fill="x")

#fungsi yg dijalankan ketika tombol di klik
def tambah_tugas():
    tugas = simpledialog.askstring(
        "Tambah Tugas",
        "Masukan nama tugas"

    )

    if tugas and tugas.strip():
        baris_tugas = tk.Frame(daftar_tugas)
        baris_tugas.pack(fill="x", padx=20, pady=3)
        
        checkbox = tk.Checkbutton(
            baris_tugas,
            text=tugas.strip(),
            font=("Arial", 12)
        )
        checkbox.pack(side="left")
        
        tombol_hapus = tk.Button(
            baris_tugas,
            text="Hapus",
            command=baris_tugas.destroy
        )
        
        tombol_hapus.pack(side="right")
        
        
#Tombol tambah tugas
tombol = tk.Button(
    window,
    text="+Tambah Tugas",
    command=tambah_tugas
    )

tombol.pack(pady=10)

window.mainloop()