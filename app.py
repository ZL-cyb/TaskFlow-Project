import tkinter as tk
from tkinter import simpledialog
import json
from pathlib import Path

window = tk.Tk()
window.title("Taskflow")
window.geometry("800x500")

file_tugas = Path(__file__).with_name("task.json")
daftar_data =[]

#Memuat tugas yg sudah tersimpan
def muat_tugas():
    global daftar_data
    
    if file_tugas.exists():
        with open(file_tugas, "r" , encoding="utf-8") as file:
            daftar_data = json.load(file)

#Menyimpan tugas ke file 
def simpan_tugas():
    with open(file_tugas, "w", encoding="utf-8") as file:
        json.dump(daftar_data, file, indent=4 , ensure_ascii=False)
        
        
judul = tk.Label(
    window,
    text="Daftar tugas saya",
    font=("Arial", 18, "bold")
    
)
judul.pack(pady=20)

daftar_tugas = tk.Frame(window)
daftar_tugas.pack(pady=10, fill="x")

#Menampilkan daftar tugas
def tampilkan_daftar_tugas():
    for widget in daftar_tugas.winfo_children():
        widget.destroy()

    for tugas in daftar_data:
        baris = tk.Frame(daftar_tugas)
        baris.pack(fill="x", padx=20, pady=3)

        status = tk.BooleanVar(value=tugas["selesai"])
        
        checkbox = tk.Checkbutton(
            baris,
            text=tugas["nama"],
            variable=status,
            font=("Arial", 12),
            command=lambda t=tugas, s=status: ubah_status(t, s)
        )
        checkbox.pack(side="left")

        tombol_hapus = tk.Button(
            baris,
            text="Hapus",
            command=lambda t=tugas: hapus_tugas(t)
        )
        tombol_hapus.pack(side="right")
        
#Memperbarui status tugas
def ubah_status(tugas, status):
        tugas["selesai"] = status.get()
        simpan_tugas()
        
#Menambah tugas baru
def tambah_tugas():
    nama = simpledialog.askstring(
        "Tambah Tugas",
        "Masukan nama tugas"

    )

    if nama and nama .strip():
        daftar_data.append({
            "nama": nama .strip(),
            "selesai": False
            })
        
        simpan_tugas()
        tampilkan_daftar_tugas()
        
#Menghapus tugas
def hapus_tugas(tugas):
    daftar_data.remove(tugas)
    simpan_tugas()
    tampilkan_daftar_tugas()
    
#Tombol tambah tugas
tombol = tk.Button(
    window,
    text="+Tambah Tugas",
    command=tambah_tugas
    )

tombol.pack(pady=10)

muat_tugas()
tampilkan_daftar_tugas()

window.mainloop()