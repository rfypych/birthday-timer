import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time
import sys

# Cek jika berada di lingkungan Windows dan import library notifikasi
IS_WINDOWS = sys.platform.startswith('win')
if IS_WINDOWS:
    try:
        from win10toast import ToastNotifier
    except ImportError:
        print("Peringatan: win10toast tidak terinstal. Notifikasi tray tidak akan berfungsi.")
        ToastNotifier = None
else:
    ToastNotifier = None

# Konstanta
TITLE = "Birthday Timer"
WIDTH = 800
HEIGHT = 650 # Tinggikan sedikit untuk status bar
BG_COLOR = "#FFD1DC"  # Pink pastel
ACCENT_COLOR = "#FFACB7"  # Pink pastel lebih tua
TEXT_COLOR = "#6B5876"  # Ungu tua
BUTTON_COLOR = "#B5EAD7"  # Hijau mint pastel
FONT_STYLE = "Courier New"  # Akan digunakan sebagai font pixel-style
PRIORITY_COLOR = "#FF8FAB" # Warna baru untuk frame prioritas (lebih soft)
PRIORITY_TEXT_COLOR = "#FFFFFF" # Warna teks putih agar kontras
DEFAULT_SUBTITLE = "For Aira Jesslyn Seniara" # Subtitle default

# Fungsi untuk membuat file data jika belum ada
def create_data_file():
    if not os.path.exists("birthdays.json"):
        with open("birthdays.json", "w") as file:
            json.dump([], file)

# --- Definisi Kelas Dialog dipindahkan ke sini --- 
class BaseDialog:
    """Kelas dasar untuk dialog Toplevel yang modal."""
    def __init__(self, parent, title, callback=None, ok_text="OK", width=540, height=380):
        self.parent = parent
        self.callback = callback # Fungsi yang dipanggil dengan hasil saat OK
        self.ok_text = ok_text
        self.result = None # Hasil dialog

        self.root = tk.Toplevel(parent)
        self.root.title(title)
        self.root.configure(bg=BG_COLOR)
        self.root.geometry(f"{width}x{height}") # Ukuran default bisa di-override
        self.root.resizable(False, False)
        self.root.transient(parent) # Menggunakan parent langsung
        self.root.grab_set()

        # Posisi window dialog di tengah parent
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Label Judul Dialog
        title_label = tk.Label(self.root, text=title, font=(FONT_STYLE, 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=(10, 5))

        # Frame utama untuk body (ditempatkan di body method)
        self.initial_focus = self.body(self.root)

        # Frame untuk tombol (ditempatkan di buttonbox method)
        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self.root

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.initial_focus.focus_set()
        self.root.wait_window(self.root)

    def body(self, master):
        """Membuat body dialog (override this). Return widget awal untuk fokus."""
        # Frame utama untuk body dengan border
        body_border = tk.Frame(master, bg="#000000", bd=2, relief=tk.RAISED)
        body_border.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.form_frame = tk.Frame(body_border, bg=ACCENT_COLOR, padx=20, pady=15)
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        # Konfigurasi grid agar responsif
        self.form_frame.columnconfigure(1, weight=1)
        # Return widget yang harus fokus pertama kali (misal: entry pertama)
        return self.form_frame 

    def buttonbox(self):
        """Membuat area tombol (override this)."""
        # Frame untuk tombol, pastikan background sesuai tema
        box = tk.Frame(self.root, bg=BG_COLOR)
        box.pack(pady=(5, 15)) # Beri sedikit padding atas dan bawah

        # Tombol OK (Simpan)
        ok_frame = tk.Frame(box, bg="#000000", bd=2, relief=tk.RAISED)
        self.ok_button = tk.Button(ok_frame, text=self.ok_text, width=15, font=(FONT_STYLE, 12), command=self.ok, bg=BUTTON_COLOR, fg=TEXT_COLOR, relief=tk.RAISED, padx=10, pady=3, cursor="hand2", activebackground=self.adjust_color(BUTTON_COLOR, -20), activeforeground=TEXT_COLOR)
        self.ok_button.pack(padx=2, pady=2)
        ok_frame.pack(side=tk.LEFT, padx=10)

        # Tombol Cancel (Batal)
        cancel_frame = tk.Frame(box, bg="#000000", bd=2, relief=tk.RAISED)
        self.cancel_button = tk.Button(cancel_frame, text="Batal", width=10, font=(FONT_STYLE, 12), command=self.cancel, bg="#F0F0F0", fg=TEXT_COLOR, relief=tk.RAISED, padx=10, pady=3, cursor="hand2", activebackground="#E0E0E0", activeforeground=TEXT_COLOR)
        self.cancel_button.pack(padx=2, pady=2)
        cancel_frame.pack(side=tk.LEFT, padx=10)

        self.root.bind("<Return>", self.ok)
        self.root.bind("<Escape>", self.cancel)

    def create_labeled_entry(self, parent, label_text, row, entry_var=None, **kwargs):
        """Helper untuk membuat label dan entry."""
        label = tk.Label(parent, text=label_text, font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        label.grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        entry = tk.Entry(parent, font=(FONT_STYLE, 12), width=25, bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=entry_var, **kwargs)
        entry.grid(row=row, column=1, sticky=tk.EW, pady=5)
        return entry

    def ok(self, event=None):
        """Aksi saat tombol OK ditekan."""
        if not self.validate():
            self.initial_focus.focus_set()
            return
        
        # Proses apply HARUS dilakukan SEBELUM destroy window
        self.apply()
        
        # Panggil callback jika ada, SETELAH apply()
        if self.callback: 
            self.callback(self.result) # Kirim hasil dari apply()

        # Tutup window setelah semuanya selesai
        if self.parent: # Kembalikan fokus ke parent
             self.parent.focus_set()
        self.root.destroy() # Hancurkan window dialog
        

    def cancel(self, event=None):
        """Aksi saat tombol Batal ditekan atau window ditutup."""
        if self.parent:
             self.parent.focus_set()
        self.root.destroy()
        # Panggil callback dengan None jika dibatalkan SEBELUMNYA apply dipanggil
        if self.callback: 
            self.callback(None) 

    def validate(self):
        """Validasi input (override this). Return True jika valid."""
        return True

    def apply(self):
        """Proses data setelah validasi dan set self.result (override this)."""
        self.result = True # Default result jika tidak di-override
        pass

    # Helper adjust_color (jika diperlukan di dialog, atau akses dari parent)
    def adjust_color(self, hex_color, amount):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
        except:
            return hex_color

# --- Dialog Tambah ---
class AddBirthdayDialog(BaseDialog):
    def __init__(self, parent, callback):
        # Hapus override height, biarkan BaseDialog yang atur (atau sesuaikan jika perlu)
        super().__init__(parent, "Tambah Ulang Tahun", callback, ok_text="Simpan Data Baru") 

    def body(self, master):
        frame = super().body(master)
        self.name_entry = self.create_labeled_entry(frame, "Nama:", 0)
        self.date_entry = self.create_labeled_entry(frame, "Tanggal (DD/MM/YYYY):", 1)

        # Label utama untuk Waktu
        time_label = tk.Label(frame, text="Waktu:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        time_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 5))

        # Frame untuk menampung Spinbox Jam dan Menit secara horizontal
        time_input_frame = tk.Frame(frame, bg=ACCENT_COLOR)
        time_input_frame.grid(row=2, column=1, sticky=tk.EW, pady=(10, 5))
        
        # Label "Jam:" dan Spinbox Jam
        hour_label = tk.Label(time_input_frame, text="Jam:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        hour_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 2))
        self.hour_var = tk.IntVar(value=0)
        self.hour_spin = tk.Spinbox(time_input_frame, from_=0, to=23, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.hour_var, wrap=True, format="%02.0f")
        self.hour_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

        # Label "Menit:" dan Spinbox Menit
        minute_label = tk.Label(time_input_frame, text="Menit:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        minute_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 2))
        self.minute_var = tk.IntVar(value=0)
        self.minute_spin = tk.Spinbox(time_input_frame, from_=0, to=59, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.minute_var, wrap=True, format="%02.0f")
        self.minute_spin.grid(row=0, column=3, sticky=tk.W, padx=(0, 5))

        # Checkbox Prioritas
        self.priority_var = tk.BooleanVar()
        priority_check = tk.Checkbutton(frame, text="Jadikan Prioritas", variable=self.priority_var, font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        priority_check.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        self.initial_focus = self.name_entry
        return self.initial_focus # Kembalikan widget awal untuk fokus

    def validate(self):
        self.name = self.name_entry.get().strip()
        self.date_str = self.date_entry.get().strip()
        self.hour = self.hour_var.get()
        self.minute = self.minute_var.get()
        self.priority = self.priority_var.get()

        if not self.name or not self.date_str:
            messagebox.showwarning("Peringatan", "Nama dan tanggal harus diisi!", parent=self.root)
            return False

        try:
            day, month, year = map(int, self.date_str.split('/'))
            datetime(year, month, day) # Validasi tanggal
            if not (0 <= self.hour <= 23 and 0 <= self.minute <= 59):
                 raise ValueError("Jam atau menit tidak valid")
            return True
        except ValueError:
            messagebox.showerror("Error", "Format tanggal (DD/MM/YYYY) atau waktu (Jam: 0-23, Menit: 0-59) tidak valid.", parent=self.root)
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan validasi: {str(e)}", parent=self.root)
            return False

    def apply(self):
        # Format tanggal dan waktu sebelum disimpan
        try:
            birthday_date = datetime(int(self.date_str.split('/')[2]), int(self.date_str.split('/')[1]), int(self.date_str.split('/')[0])).strftime("%d/%m/%Y")
            birthday_time = f"{self.hour:02d}:{self.minute:02d}"
            # Set self.result yang akan dikirim ke callback
            self.result = {
                "name": self.name,
                "date": birthday_date,
                "time": birthday_time,
                "priority": self.priority
            }
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memformat data: {str(e)}", parent=self.root)
            self.result = None # Set result ke None jika gagal


# --- Dialog Edit ---
class EditBirthdayDialog(BaseDialog):
    def __init__(self, parent, initial_data, callback):
        self.initial_data = initial_data
        # Hapus override height, biarkan BaseDialog yang atur (atau sesuaikan jika perlu)
        super().__init__(parent, "Edit Ulang Tahun", callback, ok_text="Simpan Perubahan")

    def body(self, master):
        frame = super().body(master)
        self.name_var = tk.StringVar(value=self.initial_data.get("name", ""))
        self.date_var = tk.StringVar(value=self.initial_data.get("date", ""))
        try:
            initial_time = self.initial_data.get("time", "00:00").split(':')
            initial_hour = int(initial_time[0]) if len(initial_time) > 0 else 0
            initial_minute = int(initial_time[1]) if len(initial_time) > 1 else 0
        except (ValueError, IndexError):
             initial_hour, initial_minute = 0, 0 # Default jika format salah

        self.name_entry = self.create_labeled_entry(frame, "Nama:", 0, entry_var=self.name_var)
        self.date_entry = self.create_labeled_entry(frame, "Tanggal (DD/MM/YYYY):", 1, entry_var=self.date_var)

        # Label utama untuk Waktu
        time_label = tk.Label(frame, text="Waktu:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        time_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 5))

        # Frame untuk menampung Spinbox Jam dan Menit secara horizontal
        time_input_frame = tk.Frame(frame, bg=ACCENT_COLOR)
        time_input_frame.grid(row=2, column=1, sticky=tk.EW, pady=(10, 5))
        
        # Label "Jam:" dan Spinbox Jam
        hour_label = tk.Label(time_input_frame, text="Jam:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        hour_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 2))
        self.hour_var = tk.IntVar(value=initial_hour) # Use initial value
        self.hour_spin = tk.Spinbox(time_input_frame, from_=0, to=23, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.hour_var, wrap=True, format="%02.0f")
        self.hour_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

        # Label "Menit:" dan Spinbox Menit
        minute_label = tk.Label(time_input_frame, text="Menit:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        minute_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 2))
        self.minute_var = tk.IntVar(value=initial_minute) # Use initial value
        self.minute_spin = tk.Spinbox(time_input_frame, from_=0, to=59, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.minute_var, wrap=True, format="%02.0f")
        self.minute_spin.grid(row=0, column=3, sticky=tk.W, padx=(0, 5))

        # Checkbox Prioritas
        self.priority_var = tk.BooleanVar(value=self.initial_data.get("priority", False))
        priority_check = tk.Checkbutton(frame, text="Jadikan Prioritas", variable=self.priority_var, font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        priority_check.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        self.initial_focus = self.name_entry
        return self.initial_focus # Kembalikan widget awal untuk fokus

    def validate(self):
        # Validasi mirip dengan Add Dialog
        self.name = self.name_var.get().strip()
        self.date_str = self.date_var.get().strip()
        self.hour = self.hour_var.get()
        self.minute = self.minute_var.get()
        self.priority = self.priority_var.get()

        if not self.name or not self.date_str:
            messagebox.showwarning("Peringatan", "Nama dan tanggal harus diisi!", parent=self.root)
            return False

        try:
            day, month, year = map(int, self.date_str.split('/'))
            datetime(year, month, day) # Validasi tanggal
            if not (0 <= self.hour <= 23 and 0 <= self.minute <= 59):
                 raise ValueError("Jam atau menit tidak valid")
            return True
        except ValueError:
            messagebox.showerror("Error", "Format tanggal (DD/MM/YYYY) atau waktu (Jam: 0-23, Menit: 0-59) tidak valid.", parent=self.root)
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan validasi: {str(e)}", parent=self.root)
            return False

    def apply(self):
        # Format tanggal dan waktu sebelum disimpan
        try:
            birthday_date = datetime(int(self.date_str.split('/')[2]), int(self.date_str.split('/')[1]), int(self.date_str.split('/')[0])).strftime("%d/%m/%Y")
            birthday_time = f"{self.hour:02d}:{self.minute:02d}"
            # Set self.result yang akan dikirim ke callback
            self.result = {
                "id": self.initial_data.get("id"), # Sertakan ID asli
                "name": self.name,
                "date": birthday_date,
                "time": birthday_time,
                "priority": self.priority
            }
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memformat data: {str(e)}", parent=self.root)
            self.result = None # Set result ke None jika gagal

# --- Akhir class Dialog ---

# Kelas utama aplikasi
class BirthdayReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)  # Ubah ke True agar window bisa di-resize
        
        # Set minimum size untuk window
        self.root.minsize(650, 550)
        
        # Inisialisasi notifier jika di Windows
        self.toast = ToastNotifier() if IS_WINDOWS and ToastNotifier else None
        
        # Panggil fungsi untuk membuat file data
        create_data_file()
        
        # Memuat data ulang tahun
        self.birthdays = self.load_birthdays()
        
        # Notifikasi yang telah ditampilkan
        self.shown_notifications = set()
        
        # StringVar untuk timer, status, countdown prioritas, dan subtitle
        self.time_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.priority_countdown_var = tk.StringVar()
        self.priority_target_var = tk.StringVar()
        self.subtitle_var = tk.StringVar(value=DEFAULT_SUBTITLE) # StringVar untuk subtitle
        self.priority_birthday_id = None # ID dari item prioritas saat ini
        
        # Membuat UI
        self.create_ui()
        
        # Memulai timer
        self.update_time_and_countdown()
        
        # Menambahkan event handler untuk window resize
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Mulai thread untuk cek notifikasi
        self.notification_thread = threading.Thread(target=self.check_notifications, daemon=True)
        self.notification_thread.start()
        
        # Tambahkan ikon untuk window
        try:
            self.root.iconbitmap("cake_icon.ico") # Pastikan file cake_icon.ico ada
        except tk.TclError:
            print("Info: File cake_icon.ico tidak ditemukan atau tidak valid.")
        except Exception as e:
            print(f"Error saat memuat ikon: {e}")
            
    def update_time_and_countdown(self):
        """Memperbarui label waktu dan countdown prioritas"""
        now = datetime.now()
        # Update Waktu Utama
        time_str = now.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"
        try:
            self.time_var.set(time_str)
        except tk.TclError:
            return 
            
        # Update Countdown Prioritas dan Subtitle
        if self.priority_birthday_id is not None:
            target_birthday = next((b for b in self.birthdays if b.get("id") == self.priority_birthday_id), None)
            if target_birthday:
                try:
                    day, month, year = map(int, target_birthday["date"].split('/'))
                    hour, minute = map(int, target_birthday.get("time", "00:00").split(':'))
                    current_year = now.year
                    target_dt_this_year = datetime(current_year, month, day, hour, minute)
                    
                    if target_dt_this_year < now:
                        next_birthday_dt = datetime(current_year + 1, month, day, hour, minute)
                    else:
                        next_birthday_dt = target_dt_this_year
                        
                    delta = next_birthday_dt - now
                    
                    if delta.total_seconds() > 0:
                        days = delta.days
                        seconds_total = int(delta.total_seconds()) % (24 * 3600)
                        hours = seconds_total // 3600
                        minutes = (seconds_total % 3600) // 60
                        seconds = seconds_total % 60
                        milliseconds = delta.microseconds // 1000
                        
                        countdown_str = f"{days:02d} hari {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                        self.priority_countdown_var.set(countdown_str)
                        # Ubah teks target menjadi hiasan
                        self.priority_target_var.set("⏳✨ Counting Down ✨⏳") 
                        # Update subtitle dengan nama target
                        self.subtitle_var.set(f"For {target_birthday['name']}")
                        self.priority_frame.grid() 
                    else:
                        # Teks saat hari H
                        self.priority_countdown_var.set("🎉 Selamat Ulang Tahun! 🎉") 
                        # Hiasan untuk hari H
                        self.priority_target_var.set("✨🎂 Happy Birthday! 🎂✨")
                        # Update subtitle dengan nama target
                        self.subtitle_var.set(f"For {target_birthday['name']}")
                        self.priority_frame.grid()
                        
                except ValueError:
                    self.priority_countdown_var.set("Format tanggal/waktu salah")
                    self.priority_target_var.set("⚠️ Error ⚠️") # Teks error
                    self.subtitle_var.set(DEFAULT_SUBTITLE) # Kembalikan subtitle
                    self.priority_frame.grid() 
                except Exception as e:
                    print(f"Error calculating countdown: {e}")
                    self.priority_countdown_var.set("Error")
                    self.priority_target_var.set("⚠️ Error ⚠️") # Teks error
                    self.subtitle_var.set(DEFAULT_SUBTITLE) # Kembalikan subtitle
                    self.priority_frame.grid()
            else:
                 # Jika target_birthday tidak ditemukan (seharusnya jarang terjadi jika ID ada)
                 self.priority_birthday_id = None
                 self.priority_countdown_var.set("")
                 self.priority_target_var.set("")
                 self.subtitle_var.set(DEFAULT_SUBTITLE) # Kembalikan subtitle
                 self.priority_frame.grid_remove()
        else:
            # Jika tidak ada prioritas
            self.priority_countdown_var.set("")
            self.priority_target_var.set("")
            self.subtitle_var.set(DEFAULT_SUBTITLE) # Kembalikan subtitle
            self.priority_frame.grid_remove()
            
        # Panggil lagi setelah 50ms
        try:
            self.root.after(50, self.update_time_and_countdown) 
        except tk.TclError:
            pass # Jangan panggil lagi jika window sudah ditutup

    def find_and_set_priority_target(self):
        """Mencari ulang tahun prioritas terdekat dan set ID nya"""
        now = datetime.now()
        current_year = now.year
        soonest_priority = None
        min_delta = timedelta.max
        
        for bday in self.birthdays:
            if bday.get("priority", False):
                try:
                    day, month, year = map(int, bday["date"].split('/'))
                    hour, minute = map(int, bday.get("time", "00:00").split(':'))
                    target_dt_this_year = datetime(current_year, month, day, hour, minute)
                    if datetime(current_year, month, day, 23, 59, 59) < now:
                        next_birthday_dt = datetime(current_year + 1, month, day, hour, minute)
                    else:
                        next_birthday_dt = target_dt_this_year
                    
                    delta = next_birthday_dt - now
                    if delta > timedelta(0) and delta < min_delta:
                        min_delta = delta
                        soonest_priority = bday
                    elif delta <= timedelta(0) and delta > timedelta(days=-1):
                         min_delta = delta
                         soonest_priority = bday
                         break 
                except ValueError:
                    continue 
        
        if soonest_priority:
            self.priority_birthday_id = soonest_priority.get("id")
        else:
            self.priority_birthday_id = None

    def on_window_resize(self, event):
        """Menangani event resize window"""
        try:
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            if event.widget == self.root and (event.width != current_width or event.height != current_height):
                width = event.width
                if width > 650:
                    nama_width = int(width * 0.4) 
                else:
                    nama_width = 250
                self.birthday_tree.column("Nama", width=nama_width)
        except tk.TclError:
            pass
        except Exception as e:
            print(f"Error saat menyesuaikan ukuran: {str(e)}")
    
    def create_ui(self):
        main_container = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.rowconfigure(2, weight=1) # Row untuk list_container (diubah indexnya)
        main_container.columnconfigure(0, weight=1)
        
        # Header label
        header_frame = tk.Frame(main_container, bg=BG_COLOR, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_decoration = tk.Label(header_frame, text="🎂 🎈 🎁", font=(FONT_STYLE, 24), bg=BG_COLOR, fg="#FF6B6B")
        header_decoration.pack(pady=(0, 5))
        subtitle_decoration = tk.Label(header_frame, textvariable=self.subtitle_var, font=(FONT_STYLE, 16), bg=BG_COLOR, fg=TEXT_COLOR)
        subtitle_decoration.pack(pady=(0, 5))
        title_label = tk.Label(header_frame, text="✨ Birthday Timer ✨", font=(FONT_STYLE, 28, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=(0, 5))
        
        # Frame untuk Countdown Prioritas
        self.priority_frame = tk.Frame(main_container, bg="#000000", bd=2, relief=tk.RAISED)
        # Rapikan tampilan frame countdown
        priority_inner_frame = tk.Frame(self.priority_frame, bg=PRIORITY_COLOR, padx=15, pady=8)
        priority_inner_frame.pack(fill=tk.BOTH, padx=1, pady=1)
        priority_inner_frame.columnconfigure(0, weight=1) # Agar label bisa rata tengah jika perlu
        
        self.priority_target_label = tk.Label(priority_inner_frame, textvariable=self.priority_target_var, font=(FONT_STYLE, 12, "bold"), bg=PRIORITY_COLOR, fg=PRIORITY_TEXT_COLOR, anchor="center")
        self.priority_target_label.grid(row=0, column=0, sticky="ew", pady=(0,2))
        self.priority_countdown_label = tk.Label(priority_inner_frame, textvariable=self.priority_countdown_var, font=(FONT_STYLE, 20, "bold"), bg=PRIORITY_COLOR, fg=PRIORITY_TEXT_COLOR, anchor="center") # Font lebih besar
        self.priority_countdown_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.priority_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 15)) # Tambah padding bawah
        self.priority_frame.grid_remove() # Sembunyikan awalnya

        # List frame (indeks row diubah)
        list_container = tk.Frame(main_container, bg=BG_COLOR, pady=5)
        list_container.grid(row=2, column=0, sticky="nsew") 
        list_container.rowconfigure(1, weight=1) 
        list_container.columnconfigure(0, weight=1) 
        
        list_border = tk.Frame(list_container, bg="#000000", bd=2, relief=tk.RAISED)
        list_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(0,5))
        list_frame = tk.Frame(list_border, bg=BG_COLOR, padx=10, pady=10)
        list_frame.pack(fill=tk.X, padx=2, pady=2)
        list_frame.columnconfigure(0, weight=1) 
        list_label = tk.Label(list_frame, text="Daftar Ulang Tahun", font=(FONT_STYLE, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        list_label.grid(row=0, column=0)
        
        tree_container = tk.Frame(list_container, bg=BG_COLOR)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=5)
        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)
        tree_border = tk.Frame(tree_container, bg="#000000", bd=2, relief=tk.RAISED)
        tree_border.grid(row=0, column=0, sticky="nsew")
        tree_frame = tk.Frame(tree_border, bg=BG_COLOR, padx=2, pady=2)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        columns = ("Nama", "Tanggal", "Umur", "Hari Lagi")
        self.birthday_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        self.birthday_tree.grid(row=0, column=0, sticky="nsew")
        style = ttk.Style()
        style.configure("Treeview", font=(FONT_STYLE, 12), rowheight=30, background="#FFFFFF", foreground=TEXT_COLOR)
        style.configure("Treeview.Heading", font=(FONT_STYLE, 12, "bold"), background=ACCENT_COLOR, foreground=TEXT_COLOR)
        column_widths = {"Nama": 250, "Tanggal": 120, "Umur": 80, "Hari Lagi": 100}
        for col in columns:
            self.birthday_tree.heading(col, text=col)
            self.birthday_tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.birthday_tree.yview)
        self.birthday_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        action_button_frame = tk.Frame(list_container, bg=BG_COLOR, pady=12)
        action_button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(10,0))
        
        def create_pixel_button(parent, text, command, bg_color, width=10):
            btn_frame = tk.Frame(parent, bg="#000000", bd=2, relief=tk.RAISED)
            button = tk.Button(btn_frame, text=text, font=(FONT_STYLE, 12), command=command, bg=bg_color, fg=TEXT_COLOR, relief=tk.RAISED, padx=10, pady=5, width=width, cursor="hand2", activebackground=self.adjust_color(bg_color, -20), activeforeground=TEXT_COLOR)
            button.pack(padx=2, pady=2)
            return btn_frame
            
        add_button = create_pixel_button(action_button_frame, "+ Tambah", self.add_birthday_dialog, "#90EE90") 
        add_button.pack(side=tk.LEFT, padx=5)
        edit_button = create_pixel_button(action_button_frame, "Edit", self.edit_birthday, "#A0E7E5")
        edit_button.pack(side=tk.LEFT, padx=5)
        delete_button = create_pixel_button(action_button_frame, "Hapus", self.delete_birthday, "#FBE7C6")
        delete_button.pack(side=tk.LEFT, padx=5)
        refresh_button = create_pixel_button(action_button_frame, "Refresh", self.refresh_birthdays, "#B4F8C8")
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#000000", height=30, bd=2, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        status_border = tk.Frame(status_frame, bg=BG_COLOR)
        status_border.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        status_label = tk.Label(status_border, textvariable=self.status_var, font=(FONT_STYLE, 10), bg=BG_COLOR, fg=TEXT_COLOR, anchor=tk.W, padx=10)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        time_label = tk.Label(status_border, textvariable=self.time_var, font=(FONT_STYLE, 10), bg=BG_COLOR, fg=TEXT_COLOR, anchor=tk.E, padx=10)
        time_label.pack(side=tk.RIGHT)
        
        self.refresh_birthdays() 

    def add_birthday_dialog(self):
        """Membuka dialog untuk menambah data ulang tahun baru menggunakan BaseDialog."""
        def process_add_result(result):
            if result is None: return # User membatalkan
            try:
                new_birthday = {
                    "id": self.get_next_id(),
                    "name": result["name"],
                    "date": result["date"],
                    "time": result["time"],
                    "priority": result["priority"]
                }
                
                if new_birthday["priority"]:
                    for b in self.birthdays:
                        b["priority"] = False
                        
                self.birthdays.append(new_birthday)
                self.save_birthdays()
                self.refresh_birthdays() 
                self.flash_status(f"✓ Ulang tahun {new_birthday['name']} berhasil ditambahkan!")
                self.check_notification_for_birthday(new_birthday)
                
            except Exception as e:
                 messagebox.showerror("Error", f"Gagal memproses data baru: {str(e)}", parent=self.root)

        dialog = AddBirthdayDialog(self.root, process_add_result)

    def adjust_color(self, hex_color, amount):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
        except:
            return hex_color
    
    def load_birthdays(self):
        try:
            with open("birthdays.json", "r") as file:
                data = json.load(file)
                for item in data:
                    if "priority" not in item:
                        item["priority"] = False
                    if "time" not in item:
                        item["time"] = "00:00" # Default time
                return data
        except FileNotFoundError:
             return [] 
        except json.JSONDecodeError:
             messagebox.showerror("Error Data", "File birthdays.json rusak atau formatnya salah.")
             return []
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
            return []
    
    def save_birthdays(self):
        try:
            with open("birthdays.json", "w") as file:
                json.dump(self.birthdays, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    def get_next_id(self):
        if not self.birthdays:
            return 1
        return max(b.get("id", 0) for b in self.birthdays if isinstance(b.get("id"), int)) + 1
    
    def flash_status(self, message, duration=3000):
        try:
            self.status_var.set(message)
            self.root.after(duration, lambda: self.status_var.set(f"Total Data: {len(self.birthdays)}"))
        except tk.TclError:
            pass 
    
    def edit_birthday(self):
        selected_item = self.birthday_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih satu data untuk diedit!")
            return
            
        selected_iid = selected_item[0]
        item_data = self.birthday_tree.item(selected_iid)
        original_name = item_data['values'][0].replace(" ★","") 
        original_date = item_data['values'][1]
        
        item_index = -1
        birthday = None
        for index, bday in enumerate(self.birthdays):
             if bday.get('name') == original_name and bday.get('date') == original_date:
                 item_index = index
                 birthday = bday
                 break
                 
        if item_index == -1 or birthday is None:
            messagebox.showerror("Error", "Gagal menemukan data asli yang dipilih untuk diedit.")
            return
            
        def process_edit_result(result):
            if result is None: return # User membatalkan
            try:
                if result["priority"]:
                    for b in self.birthdays:
                        if b.get("id") != result.get("id"):
                            b["priority"] = False
                            
                # Update data di list self.birthdays berdasarkan ID
                found = False
                for i, b in enumerate(self.birthdays):
                     if b.get("id") == result.get("id"):
                          self.birthdays[i]["name"] = result["name"]
                          self.birthdays[i]["date"] = result["date"]
                          self.birthdays[i]["time"] = result["time"] # Simpan waktu
                          self.birthdays[i]["priority"] = result["priority"]
                          found = True
                          break
                         
                if not found:
                     messagebox.showerror("Error", "Gagal menemukan data untuk diperbarui (ID tidak cocok).", parent=self.root)
                     return

                self.save_birthdays()
                self.refresh_birthdays() 
                
                # Periksa notifikasi ulang untuk data yang diubah
                self.check_notification_for_birthday(self.birthdays[item_index]) 
                
                self.flash_status(f"✓ Data {result['name']} berhasil diperbarui!")
                
            except Exception as e:
                 messagebox.showerror("Error", f"Gagal memproses perubahan: {str(e)}", parent=self.root)

        dialog = EditBirthdayDialog(self.root, birthday, process_edit_result)

    def delete_birthday(self):
        selected_item = self.birthday_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih satu data untuk dihapus!")
            return
            
        selected_iid = selected_item[0]
        item_data = self.birthday_tree.item(selected_iid)
        original_name = item_data['values'][0].replace(" ★","")
        original_date = item_data['values'][1]
        
        item_index = -1
        deleted_was_priority = False
        deleted_id = None
        for index, bday in enumerate(self.birthdays):
             if bday.get('name') == original_name and bday.get('date') == original_date:
                 item_index = index
                 deleted_was_priority = bday.get("priority", False)
                 deleted_id = bday.get("id")
                 break
        
        if item_index == -1:
            messagebox.showerror("Error", "Gagal menemukan data yang dipilih untuk dihapus.")
            return
        
        name = self.birthdays[item_index]['name']
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus ulang tahun {name}?")
        
        if confirm:
            del self.birthdays[item_index]
            self.save_birthdays()
            if deleted_was_priority and deleted_id == self.priority_birthday_id:
                self.priority_birthday_id = None
            self.refresh_birthdays() 
            self.flash_status(f"✓ Data {name} berhasil dihapus!")
    
    def refresh_birthdays(self):
        for item in self.birthday_tree.get_children():
            self.birthday_tree.delete(item)
        
        current_date = datetime.now()
        current_year = current_date.year
        
        sorted_birthdays = []
        for birthday in self.birthdays:
            try:
                day, month, year = map(int, birthday["date"].split('/'))
                hour, minute = map(int, birthday.get("time", "00:00").split(':'))
                next_birthday_dt = datetime(current_year, month, day, hour, minute)
                if datetime(current_year, month, day, 23, 59, 59) < current_date:
                    next_birthday_dt = datetime(current_year + 1, month, day, hour, minute)
                days_left = (next_birthday_dt - current_date).days
                sorted_birthdays.append((birthday, days_left))
            except Exception as e:
                print(f"Error parsing tanggal (refresh) untuk {birthday.get('name', 'N/A')}: {e}")
                sorted_birthdays.append((birthday, float('inf'))) 
        
        sorted_birthdays.sort(key=lambda x: x[1])
        
        for i, (birthday, days_left) in enumerate(sorted_birthdays):
            try:
                day, month, year = map(int, birthday["date"].split('/'))
                hour, minute = map(int, birthday.get("time", "00:00").split(':'))
                age = current_year - year
                if (month, day) > (current_date.month, current_date.day):
                    age -= 1 
                age = max(0, age)
                if days_left < 0: days_left = 0
                
                tag = f"birthday_{i}"
                tree_iid = f"I{i+1}"
                
                display_name = birthday["name"]
                if birthday.get("priority", False):
                    display_name += " ★" 
                    
                self.birthday_tree.insert("", tk.END, iid=tree_iid, values=(display_name, birthday["date"], age, f"{days_left} hari"), tags=(tag,))
                
                if days_left == 0:
                    self.birthday_tree.tag_configure(tag, background="#FFD700") 
                elif days_left <= 7:
                    self.birthday_tree.tag_configure(tag, background="#FFB6C1") 
                elif days_left <= 30:
                    self.birthday_tree.tag_configure(tag, background="#E6E6FA") 
                    
            except Exception as e:
                 print(f"Error menampilkan data (refresh) {birthday.get('name', 'N/A')} ke treeview: {e}")
        
        self.find_and_set_priority_target()
        
        try:
            self.status_var.set(f"Total Data: {len(self.birthdays)}")
        except tk.TclError:
            pass 
    
    def show_notification_wrapper(self, title, message, birthday_id, days_left):
        notification_key = f"{birthday_id}_{days_left}"
        if notification_key not in self.shown_notifications:
            if IS_WINDOWS and self.toast:
                try:
                    icon_path = "cake_icon.ico" if os.path.exists("cake_icon.ico") else None
                    threading.Thread(target=self.toast.show_toast, 
                                     args=(title, message), 
                                     kwargs={'icon_path': icon_path, 'duration': 10, 'threaded': False}, 
                                     daemon=True).start()
                    self.shown_notifications.add(notification_key)
                except Exception as e:
                    print(f"Gagal menampilkan notifikasi tray: {e}")
                    messagebox.showinfo(title, message)
                    self.shown_notifications.add(notification_key) 
            else:
                messagebox.showinfo(title, message)
                self.shown_notifications.add(notification_key)

    def check_notification_for_birthday(self, birthday):
        current_date = datetime.now()
        current_year = current_date.year
        try:
            day, month, year = map(int, birthday["date"].split('/'))
            hour, minute = map(int, birthday.get("time", "00:00").split(':'))
            birthday_id = birthday.get("id", -1)
            next_birthday_dt = datetime(current_year, month, day, hour, minute)
            if datetime(current_year, month, day, 23, 59, 59) < current_date:
                 next_birthday_dt = datetime(current_year + 1, month, day, hour, minute)
            days_left = (next_birthday_dt - current_date).days
            
            if 0 <= days_left <= 7:
                if days_left == 0:
                    title = "Selamat Ulang Tahun!"
                    message = f"Hari ini adalah ulang tahun {birthday['name']}!"
                else:
                    title = "Pengingat Ulang Tahun"
                    message = f"Ulang tahun {birthday['name']} dalam {days_left} hari lagi!"
                self.root.after(100, self.show_notification_wrapper, title, message, birthday_id, days_left)
        except Exception as e:
            print(f"Error saat memeriksa notifikasi (check_one) {birthday.get('name', 'N/A')}: {str(e)}")
    
    def check_notifications(self):
        first_run = True
        while True:
            if first_run:
                time.sleep(5)
                first_run = False
            try:
                current_date = datetime.now()
                current_year = current_date.year
                for birthday in self.birthdays[:]: 
                    try:
                        day, month, year = map(int, birthday["date"].split('/'))
                        hour, minute = map(int, birthday.get("time", "00:00").split(':'))
                        birthday_id = birthday.get("id", -1)
                        next_birthday_dt = datetime(current_year, month, day, hour, minute)
                        if datetime(current_year, month, day, 23, 59, 59) < current_date:
                            next_birthday_dt = datetime(current_year + 1, month, day, hour, minute)
                        days_left = (next_birthday_dt - current_date).days
                        if 0 <= days_left <= 7:
                            if days_left == 0:
                                title = "Selamat Ulang Tahun!"
                                message = f"Hari ini adalah ulang tahun {birthday['name']}!"
                            else:
                                title = "Pengingat Ulang Tahun"
                                message = f"Ulang tahun {birthday['name']} dalam {days_left} hari lagi!"
                            self.root.after(100, self.show_notification_wrapper, title, message, birthday_id, days_left)
                    except Exception as e:
                        print(f"Error memproses notifikasi (check_all) {birthday.get('name','N/A')}: {e}")
                
                if current_date.hour == 0 and current_date.minute == 0:
                    self.shown_notifications.clear()
            except tk.TclError:
                break
            except Exception as e:
                print(f"Error dalam thread notifikasi: {str(e)}")
            time.sleep(3600)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif IS_WINDOWS and 'vista' in available_themes:
             style.theme_use('vista')
        app = BirthdayReminderApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error Aplikasi", f"Terjadi kesalahan fatal: {str(e)}") 