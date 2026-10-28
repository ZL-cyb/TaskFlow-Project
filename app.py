import tkinter as tk
from tkinter import simpledialog, ttk
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

#Menyimpan tugas ke file JSON
def simpan_tugas():
    with open(file_tugas, "w", encoding="utf-8") as file:
        json.dump(daftar_data, file, indent=4 , ensure_ascii=False)
        
#Mengurutkan tugas by prioritas
def urutkan_tugas ():
    urutan ={
        "Tinggi": 1,
        "Sedang": 2,
        "Rendah": 3
    }
     
    daftar_data.sort(
        key=lambda tugas: urutan.get(
            tugas.get("prioritas", "Sedang"), 2
        )
    )    
        
judul = tk.Label(
    window,
    text="Daftar Tugas Saya",
    font=("Arial", 18, "bold")
    
)
judul.pack(pady=20)

daftar_tugas = tk.Frame(window)
daftar_tugas.pack(pady=10, fill="x")

#Menampilkan daftar tugas
def tampilkan_daftar_tugas():
    for widget in daftar_tugas.winfo_children():
        widget.destroy()
        
    urutkan_tugas()

    for tugas in daftar_data:
        tugas.setdefault("prioritas", "Sedang")
        
        baris = tk.Frame(daftar_tugas)
        baris.pack(fill="x", padx=20, pady=3)

        status = tk.BooleanVar(value=tugas["selesai"])
        
        checkbox = tk.Checkbutton(
            baris,
            text=f'{tugas["nama"]} - Prioritas: {tugas.get("prioritas, Sedang")}',
            variable=status,
            font=("Arial", 12),
            command=lambda t=tugas, s=status: ubah_status(t, s)
        )
        checkbox.pack(side="left")
        
        tombol_ubah = tk.Button(
            baris,
            text="Ubah Prioritas",
            command=lambda t=tugas: ubah_prioritas(t)
        )
        tombol_ubah.pack(side="right", padx=5)
        
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
        pilihan = tk.Toplevel(window)
        pilihan.title("Pilihan Prioritas")
        pilihan.geometry("300x150")
        pilihan.transient(window)
        pilihan.grab_set()
        
        tk.Label(
            pilihan,
            text="Pilihan Prioritas Tugas:",
        ).pack(pady=10)
        
        prioritas = tk.StringVar(value="Sedang")

        ttk.Combobox(
            pilihan,
            textvariable=prioritas,
            values=["Tinggi", "Sedang", "Rendah"],
            state="readonly"
        ).pack(pady=5)
        
    def simpan_prioritas():
        daftar_data.append({
             "nama": nama.strip(),
             "selesai": False,
             "prioritas": prioritas.get()
             })
        urutkan_tugas()
        simpan_tugas()
        tampilkan_daftar_tugas()
        pilihan.destroy()
    
    tk.Button(  
    pilihan,
    text="Simpan",
    command=simpan_prioritas
    ).pack(pady=10)
    
#Mengubah prioritas tugas yg sudah ada
def ubah_prioritas(tugas):
    pilihan = tk.Toplevel(window)
    pilihan.title("Ubah Prioritas")
    pilihan.geometry("300x150")
    pilihan.transient(window)
    pilihan.grab_set()
    
    tk.Label(
         pilihan,
         text=f'Prioritas: {tugas["nama"]}'
        ).pack(pady=10)
    
    prioritas = tk.StringVar(
        value=tugas.get("prioritas", "Sedang")
    )
    
    ttk.Combobox(
        pilihan,
        textvariable=prioritas,
        values=["Tinggi", "Sedang", "Rendah"],
        state="readonly"
    ).pack(pady=5)
    
    def simpan_perubahan():
            tugas["prioritas"] = prioritas.get()
    
            urutkan_tugas()
            simpan_tugas()
            tampilkan_daftar_tugas()
            pilihan.destroy()
            
    tk.Button(
            pilihan,
            text="Simpan Perubahan",
            command=simpan_perubahan
        ).pack(pady=10)
    
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