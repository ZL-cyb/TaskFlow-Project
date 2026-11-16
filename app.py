import tkinter as tk
from tkinter import simpledialog, ttk
import json
from pathlib import Path
from datetime import datetime

window = tk.Tk()
window.title("TaskFlow - Task Management")
window.geometry("1000x650")
window.minsize(850, 550)
window.configure(bg="#F4F6FA")

#Set tema app
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    padding=6,
    font=("Segoe UI", 10)
)

style.configure(
    "Horizontal.TProgressbar",
    troughcolor="#E2E8F0",
    background="#2563EB",
    thickness=10
)


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
# Dashboard statistik tugas
statistik_frame = tk.Frame(
    window,
    bg="#F4F6FA"
)
statistik_frame.pack(fill="x", padx=25, pady=15)

# Kartu Total Tugas
card_total = tk.Frame(
    statistik_frame,
    bg="white",
    padx=25,
    pady=18
)
card_total.pack(side="left", expand=True, fill="x", padx=8)

tk.Label(
    card_total,
    text="TOTAL TUGAS",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#64748B"
).pack()

label_total = tk.Label(
    card_total,
    text="0",
    font=("Segoe UI", 24, "bold"),
    bg="white",
    fg="#2563EB"
)
label_total.pack()

# Kartu Tugas Selesai
card_selesai = tk.Frame(
    statistik_frame,
    bg="white",
    padx=25,
    pady=18
)
card_selesai.pack(side="left", expand=True, fill="x", padx=8)

tk.Label(
    card_selesai,
    text="TUGAS SELESAI",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#64748B"
).pack()

label_selesai = tk.Label(
    card_selesai,
    text="0",
    font=("Segoe UI", 24, "bold"),
    bg="white",
    fg="#16A34A"
)
label_selesai.pack()

# Kartu Tugas Belum Selesai
card_belum = tk.Frame(
    statistik_frame,
    bg="white",
    padx=25,
    pady=18
)
card_belum.pack(side="left", expand=True, fill="x", padx=8)

tk.Label(
    card_belum,
    text="BELUM SELESAI",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#64748B"
).pack()

label_belum = tk.Label(
    card_belum,
    text="0",
    font=("Segoe UI", 24, "bold"),
    bg="white",
    fg="#EA580C"
)
label_belum.pack()

#Progres pengerjaan tugas
# Progress pengerjaan tugas
progress_frame = tk.Frame(
    window,
    bg="#F4F6FA",
    padx=25,
    pady=10
)
progress_frame.pack(fill="x")

label_progress = tk.Label(
    progress_frame,
    text="Progress: 0%",
    font=("Segoe UI", 10, "bold"),
    bg="#F4F6FA",
    fg="#334155"
)
label_progress.pack(anchor="w")

progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=300,
    mode="determinate",
    maximum=100
)
progress_bar.pack(fill="x", pady=8)

#Filter daftar tugas 
# Filter daftar tugas
filter_frame = tk.Frame(
    window,
    bg="#F4F6FA"
)
filter_frame.pack(fill="x", padx=25, pady=5)

tk.Label(
    filter_frame,
    text="Filter tugas:",
    font=("Segoe UI", 10, "bold"),
    bg="#F4F6FA",
    fg="#334155"
).pack(side="left", padx=(0, 10))

filter_status = tk.StringVar(value="Semua")

pilihan_filter = ttk.Combobox(
    filter_frame,
    textvariable=filter_status,
    values=["Semua", "Belum selesai", "Selesai"],
    state="readonly",
    width=20
)
pilihan_filter.pack(side="left")

pilihan_filter.bind(
    "<<ComboboxSelected>>",
    lambda event: tampilkan_daftar_tugas()
)

# Tampilan rekomendasi tugas
frame_rekomendasi = tk.Frame(
    window,
    bg="#E8F3FF",
    padx=20,
    pady=15
)
frame_rekomendasi.pack(
    fill="x",
    padx=25,
    pady=15
)

tk.Label(
    frame_rekomendasi,
    text="REKOMENDASI UNTUK KAMU",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#2563EB"
).pack(anchor="w", pady=(0, 8))


label_rekomendasi = tk.Label(
    frame_rekomendasi,
    text="Rekomendasi Tugas: Belum ada",
    font=("Segoe UI", 11),
    bg="white",
    fg="#334155",
    justify="left",
    wraplength=900
)
label_rekomendasi.pack(anchor="w")


# Daftar tugas
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
    
    tugas_rekomendasi = rekomendasi_tugas()
    
    if tugas_rekomendasi:
        label_rekomendasi.config(
            text=(
                   f"Rekomendasi Tugas: {tugas_rekomendasi['nama']}\n"
                   f"Prioritas: {tugas_rekomendasi.get('prioritas', 'Sedang')}\n"
                   f"Deadline: {tugas_rekomendasi.get('deadline', 'Belum ditentukan')}\n"
                   f"Sebaiknya kerjakan tugas ini terlebih dahulu!"
            )
        )
    else:
        label_rekomendasi.config(
            text="Semua tugas sudah selesai"
        )
    

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
        tampilkan_daftar_tugas()
        
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

#rekomendasi tugas 
def rekomendasi_tugas():
    tugas_belum_selesai = [
        tugas for tugas in daftar_data
        if not tugas.get("selesai", False)
    ]
    
    if not tugas_belum_selesai:
        return None
    
    urutan_prioritas = {
        "Tinggi": 1,
        "Sedang": 2,
        "Rendah": 3
    }
    
    def nilai_tugas(tugas):
        deadline = tugas.get("deadline", "Belum ditentukan")

        if deadline == "Belum ditentukan":
            tanggal = datetime.max.date()
        else:
            tanggal = datetime.strptime(
                deadline, "%d-%m-%Y"
            ).date()
            
        hari_ini = datetime.now().date()
        
        if tanggal < hari_ini:
            status_deadline = 0
        elif tanggal == hari_ini:
            status_deadline = 1
        else:
            status_deadline = 2
            
        return (
            status_deadline,
            tanggal,
            urutan_prioritas.get(tugas.get("prioritas", "Sedang"), 2)
        )
        
    return min(tugas_belum_selesai, key=nilai_tugas)

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