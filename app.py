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

# Header aplikasi
header_frame = tk.Frame(
    window,
    bg="#F4F6FA"
)
header_frame.pack(
    fill="x",
    padx=30,
    pady=(20, 10)
)

judul = tk.Label(
    header_frame,
    text="TaskFlow",
    font=("Segoe UI", 24, "bold"),
    bg="#F4F6FA",
    fg="#1E293B"
)
judul.pack(anchor="w")

subjudul = tk.Label(
    header_frame,
    text="Kelola tugasmu, atur prioritas, dan capai targetmu.",
    font=("Segoe UI", 10),
    bg="#F4F6FA",
    fg="#64748B"
)
subjudul.pack(anchor="w", pady=(2, 0))

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

# Footer untuk tombol tambah tugas
footer_frame = tk.Frame(
    window,
    bg="#F4F6FA"
)
footer_frame.pack(
    side="bottom",
    fill="x",
    pady=10
)

# Judul bagian daftar tugas
judul_daftar = tk.Label(
    window,
    text="Daftar Tugas",
    font=("Segoe UI", 15, "bold"),
    bg="#F4F6FA",
    fg="#1E293B"
)
judul_daftar.pack(
    anchor="w",
    padx=30,
    pady=(10, 0)
)

# Area daftar tugas yang bisa di-scroll
area_tugas = tk.Frame(window, bg="#F4F6FA")
area_tugas.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(10, 5)
)

canvas_tugas = tk.Canvas(
    area_tugas,
    bg="#F4F6FA",
    highlightthickness=0
)
canvas_tugas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar_tugas = ttk.Scrollbar(
    area_tugas,
    orient="vertical",
    command=canvas_tugas.yview
)
scrollbar_tugas.pack(side="right", fill="y")

canvas_tugas.configure(
    yscrollcommand=scrollbar_tugas.set
)

daftar_tugas = tk.Frame(
    canvas_tugas,
    bg="#F4F6FA"
)

canvas_window = canvas_tugas.create_window(
    (0, 0),
    window=daftar_tugas,
    anchor="nw"
)

def sesuaikan_scroll(event):
    canvas_tugas.configure(
        scrollregion=canvas_tugas.bbox("all")
    )

def sesuaikan_lebar(event):
    canvas_tugas.itemconfigure(
        canvas_window,
        width=event.width
    )

daftar_tugas.bind(
    "<Configure>",
    sesuaikan_scroll
)

canvas_tugas.bind(
    "<Configure>",
    sesuaikan_lebar
)

def scroll_mouse(event):
    canvas_tugas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

canvas_tugas.bind("<Enter>", lambda event: canvas_tugas.bind_all("<MouseWheel>", scroll_mouse))
canvas_tugas.bind("<Leave>", lambda event: canvas_tugas.unbind_all("<MouseWheel>"))

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
    
    jumlah_tampil =0
    
    for tugas in daftar_data:
        tugas.setdefault("prioritas", "Sedang")
        
        pilihan = filter_status.get()
        
        if pilihan == "Belum selesai" and tugas.get("selesai", False):
            continue
        
        if pilihan == "Selesai" and not tugas.get("selesai", False):
            continue
        
        jumlah_tampil += 1
         # Kartu setiap tugas
        baris = tk.Frame(
            daftar_tugas,
            bg="white",
            padx=12,
            pady=10
        )
        baris.pack( fill="x", pady=5, padx=5)

        status = tk.BooleanVar(value=tugas["selesai"])

        deadline = tugas.get("deadline", "Belum ditentukan")
        peringatan = cek_deadline(tugas)
        
        # Warna berdasarkan prioritas
        warna_prioritas = {
             "Tinggi": "#DC2626",
             "Sedang": "#D97706",
             "Rendah": "#2563EB"
}

        warna_teks = warna_prioritas.get(
             tugas.get("prioritas", "Sedang"),
              "#334155"
)

        # Tampilan khusus jika tugas selesai
        if tugas.get("selesai", False):
            warna_teks = "#94A3B8"
            font_tugas = ("Segoe UI", 10, "overstrike")
        else:
         font_tugas = ("Segoe UI", 10)

        checkbox = tk.Checkbutton(
        baris,
        text=f'{tugas["nama"]} - Prioritas: {tugas.get("prioritas", "Sedang")} - Deadline: {deadline} ({peringatan})',
        variable=status,
        font=font_tugas,
        bg="white",
        fg=warna_teks,
        activebackground="white",
        activeforeground=warna_teks,
        selectcolor="white",
        relief="flat",
        anchor="w",
        command=lambda t=tugas, s=status: ubah_status(t, s)
)
        checkbox.pack(
            side="left",
            fill="x",
            expand=True
        )

        tombol_ubah = tk.Button(
            baris,
            text="Prioritas",
            command=lambda t=tugas: ubah_prioritas(t),
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        tombol_ubah.pack(side="right", padx=3)

        tombol_deadline = tk.Button(
            baris,
            text="Deadline",
            command=lambda t=tugas: ubah_deadline(t),
            font=("Segoe UI", 9),
            bg="#DBEAFE",
            fg="#1D4ED8",
            activebackground="#BFDBFE",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        tombol_deadline.pack(side="right", padx=3)

        tombol_hapus = tk.Button(
            baris,
            text="Hapus",
            command=lambda t=tugas: hapus_tugas(t),
            font=("Segoe UI", 9),
            bg="#FEE2E2",
            fg="#DC2626",
            activebackground="#FECACA",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        tombol_hapus.pack(side="right", padx=3)
        
    #Tampilan jika tidak ada tugas
    if jumlah_tampil == 0:
        if filter_status.get() == "Selesai":
            pesan = "Belum ada tugas yang selesai."
        elif filter_status.get() == "Belum selesai":
            pesan = "Semua tugas sudah selesai!"
        else:
            pesan = "Belum ada tugas. Yuk, tambahkan tugas pertamamu!"
            
        label_kosong = tk.Label(
        daftar_tugas,
        text=pesan,
        font=("Segoe UI", 11),
        bg="#F4F6FA",
        fg="#64748B",
        pady=30        
        )
        label_kosong.pack(fill="x")
        
#Memperbarui status tugas
def ubah_status(tugas, status):
        tugas["selesai"] = status.get()
        simpan_tugas()
        tampilkan_daftar_tugas()
        
#Menambah tugas baru
def tambah_tugas():
    popup = tk.Toplevel(window)
    popup.title("Tambah Tugas")
    popup.geometry("400x400")
    popup.resizable(False, False)
    popup.configure(bg="#F4F6FA")
    popup.transient(window)
    popup.grab_set()

    tk.Label(
        popup,
        text="Tambah Tugas Baru",
        font=("Segoe UI", 17, "bold"),
        bg="#F4F6FA",
        fg="#1E293B"
    ).pack(pady=(20, 5))

    tk.Label(
        popup,
        text="Isi detail tugas yang ingin kamu kerjakan",
        font=("Segoe UI", 9),
        bg="#F4F6FA",
        fg="#64748B"
    ).pack(pady=(0, 20))

    # Nama tugas
    tk.Label(
        popup,
        text="Nama Tugas",
        font=("Segoe UI", 10, "bold"),
        bg="#F4F6FA"
    ).pack(anchor="w", padx=35)

    entry_nama = tk.Entry(
        popup,
        font=("Segoe UI", 11),
        relief="flat"
    )
    entry_nama.pack(fill="x", padx=35, pady=(5, 15), ipady=7)

    # Deadline
    tk.Label(
        popup,
        text="Deadline (DD-MM-YYYY)",
        font=("Segoe UI", 10, "bold"),
        bg="#F4F6FA"
    ).pack(anchor="w", padx=35)

    entry_deadline = tk.Entry(
        popup,
        font=("Segoe UI", 11),
        relief="flat"
    )
    entry_deadline.pack(fill="x", padx=35, pady=(5, 15), ipady=7)

    # Prioritas
    tk.Label(
        popup,
        text="Prioritas",
        font=("Segoe UI", 10, "bold"),
        bg="#F4F6FA"
    ).pack(anchor="w", padx=35)

    pilihan_prioritas = ttk.Combobox(
        popup,
        values=["Tinggi", "Sedang", "Rendah"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    pilihan_prioritas.set("Sedang")
    pilihan_prioritas.pack(fill="x", padx=35, pady=(5, 20))

    def simpan():
        nama = entry_nama.get().strip()
        deadline = entry_deadline.get().strip()
        prioritas = pilihan_prioritas.get()

        if not nama:
            tk.Label(
                popup,
                text="Nama tugas tidak boleh kosong!",
                fg="#DC2626",
                bg="#F4F6FA"
            ).pack()
            return

        if deadline:
            try:
                datetime.strptime(deadline, "%d-%m-%Y")
            except ValueError:
                tk.Label(
                    popup,
                    text="Format deadline tidak valid!",
                    fg="#DC2626",
                    bg="#F4F6FA"
                ).pack()
                return
        else:
            deadline = "Belum ditentukan"

        daftar_data.append({
            "nama": nama,
            "selesai": False,
            "prioritas": prioritas,
            "deadline": deadline
        })

        simpan_tugas()
        tampilkan_daftar_tugas()
        perbarui_statistik()

        popup.destroy()

    tombol_frame = tk.Frame(popup, bg="#F4F6FA")
    tombol_frame.pack(pady=5)

    tk.Button(
        tombol_frame,
        text="Batal",
        command=popup.destroy,
        bg="#E2E8F0",
        fg="#334155",
        relief="flat",
        font=("Segoe UI", 10),
        padx=20,
        pady=8
    ).pack(side="left", padx=5)

    tk.Button(
        tombol_frame,
        text="Simpan Tugas",
        command=simpan,
        bg="#2563EB",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=8
    ).pack(side="left", padx=5)

    entry_nama.focus_set()
    
#Mengubah prioritas tugas yg sudah ada
def ubah_prioritas(tugas):
    pilihan = tk.Toplevel(window)
    pilihan.title("Ubah Prioritas")
    pilihan.geometry("350x200")
    pilihan.resizable(False, False)
    pilihan.configure(bg="#F4F6FA")
    pilihan.transient(window)
    pilihan.grab_set()
    
    tk.Label(
    pilihan,
    text=f'Ubah prioritas tugas',
    font=("Segoe UI", 12, "bold"),
    bg="#F4F6FA",
    fg="#1E293B"
).pack(pady=(20, 5))

    tk.Label(
    pilihan,
    text=tugas["nama"],
    font=("Segoe UI", 10),
    bg="#F4F6FA",
    fg="#64748B"
).pack(pady=5)
    
    prioritas = tk.StringVar(
        value=tugas.get("prioritas", "Sedang")
    )
    
    ttk.Combobox(
        pilihan,
        textvariable=prioritas,
        values=["Tinggi", "Sedang", "Rendah"],
        state="readonly",
        width=25
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
            command=simpan_perubahan,
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=7,
            cursor="hand2"
        ).pack(pady=12)

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
    pilihan = tk.Toplevel(window)
    pilihan.title("Ubah Deadline")
    pilihan.geometry("380x250")
    pilihan.resizable(False, False)
    pilihan.configure(bg="#F4F6FA")
    pilihan.transient(window)
    pilihan.grab_set()

    # Judul pop-up
    tk.Label(
        pilihan,
        text="Atur Deadline Tugas",
        font=("Segoe UI", 14, "bold"),
        bg="#F4F6FA",
        fg="#1E293B"
    ).pack(pady=(20, 5))

    # Nama tugas
    tk.Label(
        pilihan,
        text=tugas["nama"],
        font=("Segoe UI", 10),
        bg="#F4F6FA",
        fg="#64748B"
    ).pack(pady=5)

    # Petunjuk tanggal
    tk.Label(
        pilihan,
        text="Tanggal (DD-MM-YYYY)",
        font=("Segoe UI", 10, "bold"),
        bg="#F4F6FA",
        fg="#334155"
    ).pack(pady=(10, 5))

    input_deadline = tk.Entry(
        pilihan,
        font=("Segoe UI", 11),
        justify="center",
        relief="solid",
        bd=1
    )
    input_deadline.pack(ipady=6, padx=40, fill="x")

    deadline_lama = tugas.get("deadline", "Belum ditentukan")

    if deadline_lama != "Belum ditentukan":
        input_deadline.insert(0, deadline_lama)

    label_error = tk.Label(
        pilihan,
        text="Kosongkan jika ingin menghapus deadline",
        font=("Segoe UI", 9),
        bg="#F4F6FA",
        fg="#64748B"
    )
    label_error.pack(pady=5)

    # Tombol simpan
    def simpan_deadline():
        deadline_baru = input_deadline.get().strip()

        if deadline_baru == "":
            tugas["deadline"] = "Belum ditentukan"
        else:
            try:
                datetime.strptime(deadline_baru, "%d-%m-%Y")
            except ValueError:
                label_error.config(
                    text="Format tanggal tidak valid!",
                    fg="#DC2626"
                )
                return

            tugas["deadline"] = deadline_baru

        simpan_tugas()
        tampilkan_daftar_tugas()
        pilihan.destroy()

    tombol_frame = tk.Frame(
        pilihan,
        bg="#F4F6FA"
    )
    tombol_frame.pack(pady=12)

    tk.Button(
        tombol_frame,
        text="Batal",
        command=pilihan.destroy,
        font=("Segoe UI", 10),
        bg="#E2E8F0",
        fg="#334155",
        relief="flat",
        padx=18,
        pady=7,
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        tombol_frame,
        text="Simpan",
        command=simpan_deadline,
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        padx=18,
        pady=7,
        cursor="hand2"
    ).pack(side="left", padx=5)

    
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
    footer_frame,
    text="+ Tambah Tugas",
    command=tambah_tugas,
    font=("Segoe UI", 11, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

tombol.pack()

muat_tugas()
tampilkan_daftar_tugas()

window.mainloop()