import tkinter as tk

window = tk.Tk()
window.title("Taskflow")
window.geometry("800x500")

#membuat  tombol  pertama
tombol = tk.Button(window, text='Tambah Tugas')
tombol.pack()
window.mainloop()

