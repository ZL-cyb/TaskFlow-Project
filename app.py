import tkinter as tk
from tkinter import simpledialog, ttk
import json
from pathlib import Path
from datetime import datetime

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

#Tampilan statistik tugas
statistik_frame = tk.Frame(window)
statistik_frame.pack(padx=10)

label_total = tk.Label(
    statistik_frame,
    text="Total: 0",
    font=("Arial", 12, "bold" ),
)
label_total.pack(side="left", padx=15)

label_selesai = tk.Label(
    statistik_frame,
    text="Selesai: 0",
    font=("Arial", 12, "bold"),
    fg="green"
)
label_selesai.pack(side="left", padx=15)

label_belum =tk.Label(
    statistik_frame,
    text="Belum selesai: 0",
    font=("Arial", 12, "bold"),
    fg="orange"
)
label_belum.pack(side="left", padx=15)

#Progres pengerjaan tugas
label_progress = tk.Label(
    window,
    text="Progress: 0%",
    font=("Arial", 11, "bold")
)
label_progress.pack(padx=5)

progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    length=300,
    mode="determinate",
    maximum=100
)
progress_bar.pack(padx=5)

#Filter daftar tugas 
filter_status = tk.StringVar(value="Semua")

pilihan_filter = ttk.Combobox(
    window,
    textvariable=filter_status,
    values=["Semua", "Belum selesai", "Selesai"],
    state="readonly",
    width=20
)
pilihan_filter.pack(padx=10)

pilihan_filter.bind(
    "<<ComboboxSelected>>",
    lambda event: tampilkan_daftar_tugas()
)

daftar_tugas = tk.Frame(window)
daftar_tugas.pack(pady=10, fill="x")

#Memperbarui statistik tugas
def perbarui_statistik():
    total = len(daftar_data)
    
    selesai = sum(
        1 for tugas in daftar_data
        if tugas.get("selesai", False)
    )
    
    belum = total - selesai
    
    label_total.config(text=f"Total: {total}")
    label_selesai.config(text=f"Selesai: {selesai}")
    label_belum.config(text=f"Belum selesai: {belum}")
    
    #menghitung presentase tugas selesai
    if total > 0:
        presentase = (selesai / total) * 100
    else:
        presentase = 0
        
    progress_bar["value"] = presentase
        
    label_progress.config(
            text=f"Progress: {presentase:.0f}%"
    )

#Menampilkan daftar tugas
def tampilkan_daftar_tugas():
    for widget in daftar_tugas.winfo_children():
        widget.destroy()
        
    urutkan_tugas()
    perbarui_statistik()

    for tugas in daftar_data:
        tugas.setdefault("prioritas", "Sedang")
        
        pilihan = filter_status.get()
        
        if pilihan == "Belum selesai" and tugas.get("selesai", False):
            continue
        
        if pilihan == "Selesai" and not tugas.get("selesai", False):
            continue
        
        baris = tk.Frame(daftar_tugas)
        baris.pack(fill="x", padx=20, pady=3)
    
        status = tk.BooleanVar(value=tugas["selesai"])
    
        deadline = tugas.get("deadline", "Belum ditentukan")
        peringatan = cek_deadline(tugas)
            
        checkbox = tk.Checkbutton(
            baris,
            text=f'{tugas["nama"]} - Prioritas: {tugas.get("prioritas", "Sedang")} - Deadline: {deadline} ({peringatan})',
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
        
        tombol_deadline = tk.Button(
            baris,
            text="Ubah Deadline",
            command=lambda t=tugas: ubah_deadline(t)
        )
        tombol_deadline.pack(side="right", padx=5)
        
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
        perbarui_statistik()
        
#Menambah tugas baru
def tambah_tugas():
    nama = simpledialog.askstring(
        "Tambah Tugas",
        "Masukan nama tugas"
    )
    
    if nama and nama.strip():

        # Meminta tanggal deadline
        while True:
            deadline = simpledialog.askstring(
                "Deadline Tugas",
                "Masukkan tanggal (DD-MM-YYYY):\nContoh: 12-12-2026"
            )

            if deadline is None:
                return

            if deadline.strip() == "":
                deadline = "Belum ditentukan"
                break

            try:
                datetime.strptime(deadline, "%d-%m-%Y")
                break
            except ValueError:
                continue

        # Membuat pop-up pilihan prioritas
        pilihan = tk.Toplevel(window)
        pilihan.title("Pilihan Prioritas")
        pilihan.geometry("300x150")
        pilihan.transient(window)
        pilihan.grab_set()

        tk.Label(
            pilihan,
            text="Pilihan Prioritas Tugas:"
        ).pack(pady=10)

        prioritas = tk.StringVar(value="Sedang")

        ttk.Combobox(
            pilihan,
            textvariable=prioritas,
            values=["Tinggi", "Sedang", "Rendah"],
            state="readonly"
        ).pack(pady=5)

        # Menyimpan tugas
        def simpan_prioritas():
            daftar_data.append({
                "nama": nama.strip(),
                "selesai": False,
                "prioritas": prioritas.get(),
                "deadline": deadline
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

#Mengubah deadline tugas
def ubah_deadline(tugas):
    deadline_baru =simpledialog.askstring(
        "Ubah Deadline",
        "Masukan tanggal baru (DD-MM-YYYY):\n"
        "Kosongkan jika ingin menghapus deadline"
    )
    
    if deadline_baru is None:
        return
    
    if deadline_baru.strip() == "":
        tugas["deadline"] = "Belum ditentukan"
    else:
        try:
            datetime.strptime(deadline_baru, "%d-%m-%Y")
        except ValueError:
            return
        
        tugas["deadline"] = deadline_baru
        
    simpan_tugas()
    tampilkan_daftar_tugas()
    
#Mengecek stat deadline
def cek_deadline(tugas):
    if tugas["selesai"]:
        return "Selesai"
    
    deadline = tugas.get("deadline", "Belum ditentukan")
    
    if deadline == "Belum ditentukan":
        return "Belum ada deadline"
    
    try:
        tanggal = datetime.strptime(
            deadline, "%d-%m-%Y"
        ).date()
        
        hari_ini = datetime.now().date()
        selisih = (tanggal - hari_ini).days
        
        if selisih < 0:
            return f"Terlambat{abs(selisih)} hari"
        elif selisih == 0:
            return "Deadline hari ini!"
        elif selisih == 1:
            return "Deadline besok!"
        elif selisih <= 3:
            return f"Deadline {selisih} hari lagi"
        else:
            return f"{selisih} hari lagi"
        
    except ValueError:
        return "Tanggal tidak valid"
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