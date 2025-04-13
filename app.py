import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import threading
import time
import sys
import subprocess
from tkcalendar import Calendar
import winreg
import random
from PIL import Image, ImageTk, ImageSequence
from sound_manager import SoundManager
# Fungsi sederhana untuk menggantikan fungsi terjemahan
def _(text, **kwargs):
    # Jika ada parameter format, terapkan
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

# Import winsound untuk efek suara di Windows
if sys.platform.startswith('win'):
    import winsound

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

# Konstanta untuk Testing
TEST_TITLE = "Test Mode"
TEST_MESSAGE = "Ini adalah pesan test"
TEST_DURATION = 2  # Durasi notifikasi test dalam detik

# Konstanta untuk kalender
CALENDAR_BG = "#FFFFFF"  # Warna latar kalender
CALENDAR_FG = TEXT_COLOR  # Warna teks kalender
CALENDAR_BORDER = ACCENT_COLOR  # Warna border kalender
CALENDAR_HEADER_BG = ACCENT_COLOR  # Warna latar header kalender
CALENDAR_SELECT_BG = "#B5EAD7"  # Warna latar saat tanggal dipilih

# Konstanta untuk ekspor/impor data
DEFAULT_EXPORT_FILENAME = "birthdays_backup.json"

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
            initial_hour, initial_minute = 0, 0

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
        self.hour_var = tk.IntVar(value=initial_hour)
        self.hour_spin = tk.Spinbox(time_input_frame, from_=0, to=23, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.hour_var, wrap=True, format="%02.0f")
        self.hour_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

        # Label "Menit:" dan Spinbox Menit
        minute_label = tk.Label(time_input_frame, text="Menit:", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        minute_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 2))
        self.minute_var = tk.IntVar(value=initial_minute)
        self.minute_spin = tk.Spinbox(time_input_frame, from_=0, to=59, width=3, font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR, relief=tk.SUNKEN, bd=2, textvariable=self.minute_var, wrap=True, format="%02.0f")
        self.minute_spin.grid(row=0, column=3, sticky=tk.W, padx=(0, 5))

        # Checkbox Prioritas
        self.priority_var = tk.BooleanVar(value=self.initial_data.get("priority", False))
        priority_check = tk.Checkbutton(frame, text="Jadikan Prioritas", variable=self.priority_var, font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        priority_check.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        self.initial_focus = self.name_entry
        return self.initial_focus

    def validate(self):
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
            datetime(year, month, day)
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
        try:
            birthday_date = datetime(int(self.date_str.split('/')[2]),
                                   int(self.date_str.split('/')[1]),
                                   int(self.date_str.split('/')[0])).strftime("%d/%m/%Y")
            birthday_time = f"{self.hour:02d}:{self.minute:02d}"

            # Set result yang akan dikirim ke callback dengan mempertahankan ID asli
            self.result = {
                "id": self.initial_data.get("id"),  # Pertahankan ID yang sama
                "name": self.name,
                "date": birthday_date,
                "time": birthday_time,
                "priority": self.priority
            }
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memformat data: {str(e)}", parent=self.root)
            self.result = None

# --- Dialog Ekspor/Impor ---
class ExportDialog(BaseDialog):
    def __init__(self, parent, data, callback):
        self.data = data
        super().__init__(parent, "Ekspor Data Ulang Tahun", callback, ok_text="Ekspor")

    def body(self, master):
        frame = super().body(master)

        label = tk.Label(frame, text="Ekspor data ulang tahun ke file JSON.\n\nFile ini dapat digunakan untuk backup\natau memindahkan data ke komputer lain.",
                        font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, justify=tk.LEFT)
        label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        # Checkbox untuk menambahkan metadata
        self.add_metadata_var = tk.BooleanVar(value=True)
        self.metadata_check = tk.Checkbutton(frame, text="Tambahkan metadata (tanggal ekspor, jumlah data)",
                                           variable=self.add_metadata_var,
                                           font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                           selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        self.metadata_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        return frame

    def validate(self):
        # Dapatkan lokasi file untuk menyimpan data
        self.filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=DEFAULT_EXPORT_FILENAME,
            parent=self.root
        )
        if not self.filename:
            return False
        return True

    def apply(self):
        try:
            export_data = {
                "birthdays": self.data
            }

            # Tambahkan metadata jika diminta
            if self.add_metadata_var.get():
                export_data["metadata"] = {
                    "export_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "count": len(self.data)
                }

            # Tulis data ke file
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, indent=4)

            self.result = True
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}", parent=self.root)
            self.result = False


class ImportDialog(BaseDialog):
    def __init__(self, parent, callback):
        super().__init__(parent, "Impor Data Ulang Tahun", callback, ok_text="Impor")

    def body(self, master):
        frame = super().body(master)

        label = tk.Label(frame, text="Impor data ulang tahun dari file JSON.\n\nPilih opsi impor di bawah ini:",
                        font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, justify=tk.LEFT)
        label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        # Opsi mode impor
        self.import_mode = tk.StringVar(value="merge")

        self.mode_frame = tk.Frame(frame, bg=ACCENT_COLOR)
        self.mode_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        self.replace_radio = tk.Radiobutton(self.mode_frame, text="Ganti semua data", variable=self.import_mode, value="replace",
                                          font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                          selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        self.replace_radio.grid(row=0, column=0, sticky="w", pady=2)

        self.merge_radio = tk.Radiobutton(self.mode_frame, text="Gabungkan dengan data yang ada", variable=self.import_mode, value="merge",
                                        font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                        selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR)
        self.merge_radio.grid(row=1, column=0, sticky="w", pady=2)

        # Button untuk memilih file
        self.file_frame = tk.Frame(frame, bg=ACCENT_COLOR)
        self.file_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(self.file_frame, textvariable=self.file_path_var, width=30,
                                 font=(FONT_STYLE, 12), bg="#FFFFFF", fg=TEXT_COLOR)
        self.file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.file_frame.columnconfigure(0, weight=1)

        browse_frame = tk.Frame(self.file_frame, bg="#000000", bd=2, relief=tk.RAISED)
        browse_button = tk.Button(browse_frame, text="Pilih File", font=(FONT_STYLE, 12),
                                 command=self.browse_file, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        browse_button.pack(padx=2, pady=2)
        browse_frame.grid(row=0, column=1)

        return self.file_entry

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            parent=self.root
        )
        if filename:
            self.file_path_var.set(filename)

    def validate(self):
        filename = self.file_path_var.get().strip()
        if not filename:
            messagebox.showwarning("Peringatan", "Silakan pilih file untuk diimpor.", parent=self.root)
            return False

        if not os.path.exists(filename):
            messagebox.showerror("Error", "File yang dipilih tidak ada.", parent=self.root)
            return False

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.import_data = json.load(file)

            # Verifikasi format data
            if "birthdays" not in self.import_data or not isinstance(self.import_data["birthdays"], list):
                messagebox.showerror("Error", "Format file tidak valid. File harus berisi kunci 'birthdays' dengan nilai berupa list.", parent=self.root)
                return False

            return True
        except json.JSONDecodeError:
            messagebox.showerror("Error", "File JSON tidak valid.", parent=self.root)
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file: {str(e)}", parent=self.root)
            return False

    def apply(self):
        mode = self.import_mode.get()
        imported_birthdays = self.import_data["birthdays"]

        # Set hasil yang akan dikirim ke callback
        self.result = {
            "mode": mode,
            "data": imported_birthdays
        }

# --- Akhir class Dialog ---

# --- Kelas Utilitas ---
class TextAnimator:
    """Kelas untuk menangani animasi teks"""
    def __init__(self, label, text, delay=80, loop=True):
        self.label = label
        self.full_text = text
        self.delay = delay
        self.loop = loop
        self.current_index = 0
        self.is_running = False
        self.is_forward = True
        self.after_id = None

    def start(self):
        """Memulai animasi teks"""
        self.is_running = True
        self.animate()

    def stop(self):
        """Menghentikan animasi teks"""
        self.is_running = False
        if self.after_id:
            self.label.after_cancel(self.after_id)
            self.after_id = None

    def animate(self):
        """Fungsi animasi yang akan dipanggil berulang"""
        if not self.is_running:
            return

        # Update teks
        if self.is_forward:
            self.current_index += 1
            if self.current_index > len(self.full_text):
                if self.loop:
                    self.is_forward = False
                    self.current_index = len(self.full_text)
                else:
                    self.current_index = 0
        else:
            self.current_index -= 1
            if self.current_index < 0:
                self.is_forward = True
                self.current_index = 0

        # Tampilkan teks
        display_text = self.full_text[:self.current_index]
        try:
            self.label.config(text=display_text)
            # Jadwalkan pemanggilan fungsi ini lagi
            self.after_id = self.label.after(self.delay, self.animate)
        except tk.TclError:
            # Widget sudah tidak ada
            self.is_running = False

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

        # Inisialisasi sound manager untuk efek suara
        self.sound_manager = SoundManager(sound_enabled=True)

        # Inisialisasi variabel sound_enabled_var dan sound_type_var terlebih dahulu
        self.sound_enabled_var = tk.BooleanVar(value=True) # Status suara

        # Variabel untuk jenis suara (click1, click2, atau click3)
        self.sound_type_var = tk.StringVar() # Variabel untuk jenis suara
        self.sound_type_var.set("click3") # Default: click3

        # Fungsi untuk memainkan suara klik
        def play_click_sound(event=None):
            if self.sound_enabled_var.get() and IS_WINDOWS:
                # Pilih file suara berdasarkan jenis suara yang dipilih
                sound_type = self.sound_type_var.get()
                if sound_type == "click1":
                    sound_file = "click1.wav"
                elif sound_type == "click2":
                    sound_file = "click2.wav"
                else:  # click3
                    sound_file = "click3.wav"

                sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                if os.path.exists(sound_path):
                    try:
                        print(f"Memainkan suara ASMR: {sound_path}")
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception as e:
                        print(f"Error memainkan suara ASMR: {e}")

        # Fungsi untuk memainkan suara pada semua elemen UI
        def play_sound_on_all_ui_elements():
            # Fungsi untuk memainkan suara pada semua widget
            def add_sound_to_widget(widget):
                if isinstance(widget, (tk.Button, ttk.Button, tk.Checkbutton, ttk.Checkbutton, tk.Radiobutton, ttk.Radiobutton)):
                    widget.bind("<Button-1>", play_click_sound, add="+")

                # Rekursif untuk semua child widget
                for child in widget.winfo_children():
                    add_sound_to_widget(child)

            # Tambahkan suara ke semua widget yang ada di root
            self.root.after(1000, lambda: add_sound_to_widget(self.root))

            # Tambahkan suara ke semua widget baru yang dibuat
            original_init = tk.Button.__init__
            def button_init_with_sound(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                self.bind("<Button-1>", play_click_sound, add="+")
            tk.Button.__init__ = button_init_with_sound

            original_ttk_init = ttk.Button.__init__
            def ttk_button_init_with_sound(self, *args, **kwargs):
                original_ttk_init(self, *args, **kwargs)
                self.bind("<Button-1>", play_click_sound, add="+")
            ttk.Button.__init__ = ttk_button_init_with_sound

        # Bind fungsi play_click_sound ke semua klik tombol di aplikasi
        self.root.bind_class('Button', '<Button-1>', play_click_sound, add="+")
        self.root.bind_class('TButton', '<Button-1>', play_click_sound, add="+")
        self.root.bind_class('TNotebook.Tab', '<Button-1>', play_click_sound, add="+")
        self.root.bind_class('Menu', '<Button-1>', play_click_sound, add="+")
        self.root.bind_class('Checkbutton', '<Button-1>', play_click_sound, add="+")

        # Binding khusus untuk menu
        def setup_menu_sound(menu):
            # Simpan command asli
            original_add_command = menu.add_command
            original_add_cascade = menu.add_cascade
            original_add_checkbutton = menu.add_checkbutton
            original_add_radiobutton = menu.add_radiobutton

            # Override add_command untuk menambahkan suara
            def add_command_with_sound(*args, **kwargs):
                if 'command' in kwargs and kwargs['command'] is not None:
                    original_command = kwargs['command']
                    def command_with_sound():
                        # Mainkan suara
                        if self.sound_enabled_var.get() and IS_WINDOWS:
                            # Pilih file suara berdasarkan jenis suara yang dipilih
                            sound_type = self.sound_type_var.get()
                            if sound_type == "click1":
                                sound_file = "click1.wav"
                            elif sound_type == "click2":
                                sound_file = "click2.wav"
                            else:  # click3
                                sound_file = "click3.wav"

                            sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                            if os.path.exists(sound_path):
                                try:
                                    print(f"Memainkan suara klik menu: {sound_path}")
                                    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                except Exception as e:
                                    print(f"Error memainkan suara klik menu: {e}")
                        # Jalankan command asli
                        original_command()
                    kwargs['command'] = command_with_sound
                return original_add_command(*args, **kwargs)

            # Override metode menu lainnya
            menu.add_command = add_command_with_sound

            # Lakukan hal yang sama untuk add_checkbutton dan add_radiobutton
            def add_checkbutton_with_sound(*args, **kwargs):
                if 'command' in kwargs and kwargs['command'] is not None:
                    original_command = kwargs['command']
                    def command_with_sound():
                        # Mainkan suara
                        if self.sound_enabled_var.get() and IS_WINDOWS:
                            # Pilih file suara berdasarkan jenis suara yang dipilih
                            sound_type = self.sound_type_var.get()
                            if sound_type == "click1":
                                sound_file = "click1.wav"
                            elif sound_type == "click2":
                                sound_file = "click2.wav"
                            else:  # click3
                                sound_file = "click3.wav"

                            sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                            if os.path.exists(sound_path):
                                try:
                                    print(f"Memainkan suara klik menu checkbox: {sound_path}")
                                    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                except Exception as e:
                                    print(f"Error memainkan suara klik menu checkbox: {e}")
                        # Jalankan command asli
                        original_command()
                    kwargs['command'] = command_with_sound
                return original_add_checkbutton(*args, **kwargs)

            menu.add_checkbutton = add_checkbutton_with_sound

            def add_radiobutton_with_sound(*args, **kwargs):
                if 'command' in kwargs and kwargs['command'] is not None:
                    original_command = kwargs['command']
                    def command_with_sound():
                        # Mainkan suara
                        if self.sound_enabled_var.get() and IS_WINDOWS:
                            # Pilih file suara berdasarkan jenis suara yang dipilih
                            sound_type = self.sound_type_var.get()
                            if sound_type == "click1":
                                sound_file = "click1.wav"
                            elif sound_type == "click2":
                                sound_file = "click2.wav"
                            else:  # click3
                                sound_file = "click3.wav"

                            sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                            if os.path.exists(sound_path):
                                try:
                                    print(f"Memainkan suara klik menu radio: {sound_path}")
                                    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                except Exception as e:
                                    print(f"Error memainkan suara klik menu radio: {e}")
                        # Jalankan command asli
                        original_command()
                    kwargs['command'] = command_with_sound
                return original_add_radiobutton(*args, **kwargs)

            menu.add_radiobutton = add_radiobutton_with_sound

            # Untuk submenu (cascade)
            def add_cascade_with_sound(*args, **kwargs):
                result = original_add_cascade(*args, **kwargs)
                if 'menu' in kwargs:
                    setup_menu_sound(kwargs['menu'])
                return result

            menu.add_cascade = add_cascade_with_sound

            return menu

        # Patch tk.Menu.__init__ untuk menambahkan suara ke semua menu
        original_menu_init = tk.Menu.__init__
        def menu_init_with_sound(self, *args, **kwargs):
            original_menu_init(self, *args, **kwargs)
            setup_menu_sound(self)
        tk.Menu.__init__ = menu_init_with_sound

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
        # sound_enabled_var sudah diinisialisasi sebelumnya

        # Memuat pengaturan aplikasi
        self.load_settings()

        # Membuat UI
        self.create_ui()

        # Aktifkan suara pada semua elemen UI
        play_sound_on_all_ui_elements()

        # Memulai timer
        self.update_time_and_countdown()

        # Menambahkan event handler untuk window resize
        self.root.bind("<Configure>", self.on_window_resize)

        # Inisialisasi animator untuk judul
        self.title_animator = None

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
        main_container.rowconfigure(2, weight=1) # Row untuk notebook (diubah indexnya)
        main_container.columnconfigure(0, weight=1)

        # Header label
        header_frame = tk.Frame(main_container, bg=BG_COLOR, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_decoration = tk.Label(header_frame, text="🎂 🎈 🎁", font=(FONT_STYLE, 24), bg=BG_COLOR, fg="#FF6B6B")
        header_decoration.pack(pady=(0, 5))
        subtitle_decoration = tk.Label(header_frame, textvariable=self.subtitle_var, font=(FONT_STYLE, 16), bg=BG_COLOR, fg=TEXT_COLOR)
        subtitle_decoration.pack(pady=(0, 5))

        # Judul dengan animasi
        self.title_label = tk.Label(header_frame, text="✨ Birthday Timer ✨", font=(FONT_STYLE, 28, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        self.title_label.pack(pady=(10, 0))

        # Today's Date Label
        self.date_label = tk.Label(header_frame, text=f"{time.strftime('%A, %d %B %Y')}", font=(FONT_STYLE, 14), bg=BG_COLOR, fg=TEXT_COLOR)

        # Inisialisasi animator untuk judul (dinonaktifkan)
        # self.title_animator = TextAnimator(self.title_label, "✨ Birthday Timer ✨", delay=150)
        # self.title_animator.start()

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

        # --- Styling Notebook ---
        style = ttk.Style()
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0) # Hapus border default notebook
        style.configure("TNotebook.Tab",
                        background=ACCENT_COLOR,
                        foreground=TEXT_COLOR,
                        font=(FONT_STYLE, 12, "bold"),
                        padding=[10, 5], # Padding horizontal & vertikal
                        borderwidth=2, # Tambahkan border untuk efek pixel
                        relief=tk.RAISED) # Efek timbul seperti tombol pixel

        # Styling untuk tab saat dipilih (aktif)
        style.map("TNotebook.Tab",
                  background=[("selected", BUTTON_COLOR)], # Warna berbeda saat aktif
                  foreground=[("selected", TEXT_COLOR)],
                  relief=[("selected", tk.SUNKEN)]) # Efek tenggelam saat aktif

        # Styling untuk tab saat dihover (tidak aktif)
        style.map("TNotebook.Tab",
                  background=[("!selected", "hover", self.adjust_color(ACCENT_COLOR, 15))], # Sedikit lebih terang saat hover
                  relief=[("!selected", "hover", tk.RAISED)])

        # Notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_container, style="TNotebook") # Terapkan style TNotebook
        self.notebook.grid(row=2, column=0, sticky="nsew", pady=(10, 0)) # Tambahkan padding atas

        # Binding khusus untuk tab notebook
        def play_tab_sound(event):
            if self.sound_enabled_var.get() and IS_WINDOWS:
                # Pilih file suara berdasarkan jenis suara yang dipilih
                sound_type = self.sound_type_var.get()
                if sound_type == "click1":
                    sound_file = "click1.wav"
                elif sound_type == "click2":
                    sound_file = "click2.wav"
                else:  # click3
                    sound_file = "click3.wav"

                sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                if os.path.exists(sound_path):
                    try:
                        print(f"Memainkan suara klik tab: {sound_path}")
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception as e:
                        print(f"Error memainkan suara klik tab: {e}")

        # Bind langsung ke notebook untuk menangkap klik pada tab
        self.notebook.bind("<Button-1>", play_tab_sound, add="+")

        # Tab Daftar
        self.list_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.list_tab, text="Daftar")

        # Tab Kalender
        self.calendar_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.calendar_tab, text="Kalender")

        # Tab Pengaturan
        self.settings_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.settings_tab, text="Pengaturan")

        # Tab Testing
        self.testing_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.testing_tab, text="Testing")

        # Tab Dokumentasi
        self.docs_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.docs_tab, text="Dokumentasi")

        # Isi masing-masing tab
        self.create_list_tab()
        self.create_calendar_tab()
        self.create_settings_tab()
        self.create_testing_tab()
        self.create_docs_tab()

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

    def create_docs_tab(self):
        """Membuat tab dokumentasi untuk menampilkan dokumentasi modul."""
        docs_container = self.docs_tab
        docs_container.columnconfigure(0, weight=1)
        docs_container.rowconfigure(1, weight=1)

        # Frame untuk judul
        title_border = tk.Frame(docs_container, bg="#000000", bd=2, relief=tk.RAISED)
        title_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5))
        title_frame = tk.Frame(title_border, bg=BG_COLOR, padx=10, pady=10)
        title_frame.pack(fill=tk.X, padx=2, pady=2)
        title_label = tk.Label(title_frame, text="Dokumentasi Modul", font=(FONT_STYLE, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title_label.pack()

        # Frame untuk konten dokumentasi
        docs_border = tk.Frame(docs_container, bg="#000000", bd=2, relief=tk.RAISED)
        docs_border.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        docs_frame = tk.Frame(docs_border, bg=ACCENT_COLOR)
        docs_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Configure docs_frame for expansion
        docs_frame.columnconfigure(0, weight=1)
        docs_frame.rowconfigure(0, weight=1)

        # Notebook untuk dokumentasi modul dengan style
        style = ttk.Style()
        style.configure("Docs.TNotebook", background=ACCENT_COLOR)
        style.configure("Docs.TNotebook.Tab",
                        background=BG_COLOR,
                        foreground=TEXT_COLOR,
                        font=(FONT_STYLE, 11),
                        padding=[8, 4])
        style.map("Docs.TNotebook.Tab",
                  background=[("selected", BUTTON_COLOR)],
                  foreground=[("selected", TEXT_COLOR)])

        docs_notebook = ttk.Notebook(docs_frame, style="Docs.TNotebook")
        docs_notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Binding khusus untuk tab dokumentasi
        def play_docs_tab_sound(event):
            if self.sound_enabled_var.get() and IS_WINDOWS:
                # Pilih file suara berdasarkan jenis suara yang dipilih
                sound_type = self.sound_type_var.get()
                if sound_type == "click1":
                    sound_file = "click1.wav"
                elif sound_type == "click2":
                    sound_file = "click2.wav"
                else:  # click3
                    sound_file = "click3.wav"

                sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                if os.path.exists(sound_path):
                    try:
                        print(f"Memainkan suara klik tab dokumentasi: {sound_path}")
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception as e:
                        print(f"Error memainkan suara klik tab dokumentasi: {e}")

        # Bind langsung ke docs_notebook untuk menangkap klik pada tab
        docs_notebook.bind("<Button-1>", play_docs_tab_sound, add="+")

        # Load dokumentasi dari file
        try:
            with open("docs/notification_documentation.md", "r") as f:
                notification_docs = f.read()
        except:
            notification_docs = "Dokumentasi modul notifikasi akan ditambahkan di sini."

        try:
            with open("docs/app_documentation.md", "r") as f:
                app_docs = f.read()
        except:
            app_docs = "Dokumentasi modul aplikasi akan ditambahkan di sini."

        # Tab untuk setiap modul
        modules = {
            "PixelUI": self.get_pixel_ui_docs(),
            "Notifikasi": notification_docs,
            "Aplikasi": app_docs
        }

        for module_name, content in modules.items():
            module_frame = tk.Frame(docs_notebook, bg=BG_COLOR)
            docs_notebook.add(module_frame, text=module_name)

            # Configure module_frame for expansion
            module_frame.columnconfigure(0, weight=1)
            module_frame.rowconfigure(0, weight=1)

            # Container frame for text and scrollbar
            container = tk.Frame(module_frame, bg=BG_COLOR)
            container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            container.columnconfigure(0, weight=1)
            container.rowconfigure(0, weight=1)

            # Text widget for content with proper configuration
            text_widget = tk.Text(container,
                                wrap=tk.WORD,
                                font=(FONT_STYLE, 12),
                                bg=BG_COLOR,
                                fg=TEXT_COLOR,
                                padx=10,
                                pady=10)
            text_widget.grid(row=0, column=0, sticky="nsew")

            # Scrollbar properly configured and placed
            scrollbar = ttk.Scrollbar(container,
                                    orient="vertical",
                                    command=text_widget.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            text_widget.configure(yscrollcommand=scrollbar.set)

            # Insert content and disable editing
            text_widget.insert("1.0", content)
            text_widget.configure(state="disabled")

    def get_pixel_ui_docs(self):
        """Mengambil dokumentasi untuk modul PixelUI."""
        return """Modul Pixel UI

Modul ini menyediakan komponen UI kustom dengan gaya pixel art untuk aplikasi pengingat ulang tahun.

Kelas PixelUI
------------
Kelas utilitas untuk membuat elemen UI bergaya pixel.

Metode Statis:

create_pixel_entry(parent, width=20, font_style="Courier New", font_size=12)
    Membuat widget entry dengan gaya pixel
    Parameters:
    - parent: Widget parent
    - width: Lebar entry dalam karakter
    - font_style: Jenis font
    - font_size: Ukuran font
    Returns: Tuple (frame, entry)

create_pixel_button(parent, text, command, bg_color="#B5EAD7", width=None)
    Membuat tombol dengan gaya pixel
    Parameters:
    - parent: Widget parent
    - text: Teks tombol
    - command: Fungsi callback
    - bg_color: Warna latar tombol
    - width: Lebar tombol (opsional)
    Returns: Button widget

create_pixel_frame(parent, bg_color="#FFD1DC", padding=10)
    Membuat frame dengan border gaya pixel
    Parameters:
    - parent: Widget parent
    - bg_color: Warna latar frame
    - padding: Padding internal frame
    Returns: Frame widget

Fitur Desain:
1. Gaya Pixel Art
   - Border dengan efek pixel
   - Font monospace untuk kesan retro
   - Warna-warna pastel yang menyenangkan

2. Responsivitas
   - Widget menyesuaikan dengan ukuran parent
   - Padding dan margin yang konsisten

3. Kustomisasi
   - Warna dapat disesuaikan
   - Ukuran dan padding fleksibel

Konstanta Warna:
- BG_COLOR = "#FFD1DC" - Pink pastel untuk latar
- ACCENT_COLOR = "#FFACB7" - Pink tua untuk aksen
- TEXT_COLOR = "#6B5876" - Ungu tua untuk teks
- BUTTON_COLOR = "#B5EAD7" - Hijau mint untuk tombol"""

    def create_testing_tab(self):
        """Membuat tab testing untuk pengujian fitur aplikasi."""
        test_container = self.testing_tab
        test_container.columnconfigure(0, weight=1)

        # Frame untuk judul
        title_border = tk.Frame(test_container, bg="#000000", bd=2, relief=tk.RAISED)
        title_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5))
        title_frame = tk.Frame(title_border, bg=BG_COLOR, padx=10, pady=10)
        title_frame.pack(fill=tk.X, padx=2, pady=2)
        title_label = tk.Label(title_frame, text="Menu Testing", font=(FONT_STYLE, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title_label.pack()

        # Frame untuk tombol-tombol test
        test_border = tk.Frame(test_container, bg="#000000", bd=2, relief=tk.RAISED)
        test_border.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        test_frame = tk.Frame(test_border, bg=ACCENT_COLOR, padx=20, pady=20)
        test_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Tombol-tombol test
        def create_test_button(text, command):
            btn_frame = tk.Frame(test_frame, bg="#000000", bd=2, relief=tk.RAISED)
            button = tk.Button(btn_frame, text=text, font=(FONT_STYLE, 12), command=command,
                             bg=BUTTON_COLOR, fg=TEXT_COLOR, width=30, pady=5)
            button.pack(padx=2, pady=2)
            return btn_frame

        # Test Notifikasi
        notif_test_btn = create_test_button("Test Sistem Notifikasi", self.test_notification)
        notif_test_btn.pack(pady=10)

        # Test Validasi Input
        input_test_btn = create_test_button("Test Validasi Input", self.test_input_validation)
        input_test_btn.pack(pady=10)

        # Test Operasi Data
        data_test_btn = create_test_button("Test Operasi Data", self.test_data_operations)
        data_test_btn.pack(pady=10)

        # Test Suara
        sound_test_btn = create_test_button("Test Sistem Suara", self.test_sound_direct)
        sound_test_btn.pack(pady=10)

        # Deskripsi pengujian
        desc_frame = tk.Frame(test_container, bg=BG_COLOR, pady=10)
        desc_frame.grid(row=2, column=0, sticky="ew", padx=5)
        desc_text = """Fitur Testing memungkinkan Anda menguji:
- Sistem notifikasi desktop
- Validasi input data ulang tahun
- Operasi data (tambah, ubah, hapus)
- Sistem suara klik"""
        desc_label = tk.Label(desc_frame, text=desc_text, font=(FONT_STYLE, 12),
                            bg=BG_COLOR, fg=TEXT_COLOR, justify=tk.LEFT)
        desc_label.pack()

    def create_list_tab(self):
        """Membuat tab daftar ulang tahun"""
        list_container = self.list_tab
        list_container.rowconfigure(1, weight=1)
        list_container.columnconfigure(0, weight=1)

        list_border = tk.Frame(list_container, bg="#000000", bd=2, relief=tk.RAISED)
        list_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5))
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

        # --- Fungsi untuk efek hover tombol ---
        def on_button_enter(e, button, original_bg):
            hover_color = self.adjust_color(original_bg, 20) # Buat sedikit lebih terang
            button.config(background=hover_color)

        def on_button_leave(e, button, original_bg):
            button.config(background=original_bg)
        # -------------------------------------

        def create_pixel_button(parent, text, command, bg_color, width=10):
            # Buat wrapper untuk command yang akan memainkan suara klik
            def command_with_sound():
                # Mainkan suara klik jika suara diaktifkan
                if self.sound_enabled_var.get() and IS_WINDOWS:
                    # Gunakan path absolut untuk file suara
                    # Pilih file suara berdasarkan jenis suara yang dipilih
                    sound_type = self.sound_type_var.get()
                    if sound_type == "click1":
                        sound_file = "click1.wav"
                    elif sound_type == "click2":
                        sound_file = "click2.wav"
                    else:  # click3
                        sound_file = "click3.wav"

                    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                    if os.path.exists(sound_path):
                        try:
                            # Gunakan SND_ASYNC agar tidak memblokir UI
                            print(f"Memainkan suara klik: {sound_path}")
                            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        except Exception as e:
                            print(f"Error memainkan suara klik: {e}")
                # Jalankan command asli
                command()

            btn_frame = tk.Frame(parent, bg="#000000", bd=2, relief=tk.RAISED)
            # Simpan warna asli
            original_bg_color = bg_color
            button = tk.Button(btn_frame, text=text, font=(FONT_STYLE, 12), command=command_with_sound, bg=original_bg_color, fg=TEXT_COLOR, relief=tk.RAISED, padx=10, pady=5, width=width, cursor="hand2", activebackground=self.adjust_color(original_bg_color, -20), activeforeground=TEXT_COLOR)
            button.pack(padx=2, pady=2)

            # Bind hover events
            button.bind("<Enter>", lambda e, b=button, bg=original_bg_color: on_button_enter(e, b, bg))
            button.bind("<Leave>", lambda e, b=button, bg=original_bg_color: on_button_leave(e, b, bg))

            return btn_frame

        add_button = create_pixel_button(action_button_frame, "+ Tambah", self.add_birthday_dialog, "#90EE90")
        add_button.pack(side=tk.LEFT, padx=5)
        edit_button = create_pixel_button(action_button_frame, "Edit", self.edit_birthday, "#A0E7E5")
        edit_button.pack(side=tk.LEFT, padx=5)
        delete_button = create_pixel_button(action_button_frame, "Hapus", self.delete_birthday, "#FBE7C6")
        delete_button.pack(side=tk.LEFT, padx=5)
        refresh_button = create_pixel_button(action_button_frame, "Refresh", self.refresh_birthdays, "#B4F8C8")
        refresh_button.pack(side=tk.RIGHT, padx=5)

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

    def test_notification(self):
        """Menguji sistem notifikasi dengan mengirim notifikasi test."""
        try:
            if self.toast:
                self.toast.show_toast(
                    title=TEST_TITLE,
                    msg=TEST_MESSAGE,
                    duration=TEST_DURATION,
                    threaded=True
                )
                messagebox.showinfo("Test Berhasil", "Notifikasi test berhasil dikirim!")
            else:
                messagebox.showwarning("Peringatan", "Sistem notifikasi tidak tersedia di sistem operasi ini.")
        except Exception as e:
            messagebox.showerror("Test Gagal", f"Gagal mengirim notifikasi: {e}")

    def test_input_validation(self):
        """Menguji validasi input dengan berbagai skenario."""
        test_cases = [
            {"nama": "", "tanggal": "2023-13-32", "expected": "Nama tidak boleh kosong dan format tanggal harus valid"},
            {"nama": "Test", "tanggal": "25/12/2023", "expected": "Input valid"}
        ]

        results = []
        for case in test_cases:
            try:
                # Validasi nama
                if not case["nama"]:
                    raise ValueError("Nama tidak boleh kosong")

                # Validasi tanggal
                if "/" in case["tanggal"]:
                    day, month, year = map(int, case["tanggal"].split("/"))
                    datetime(year, month, day)
                    results.append(f"Test Case: {case}\nHasil: Sesuai ekspektasi - {case['expected']}\n")
                else:
                    raise ValueError("Format tanggal harus DD/MM/YYYY")
            except ValueError as e:
                results.append(f"Test Case: {case}\nHasil: {str(e)}\n")

        # Tampilkan hasil test
        messagebox.showinfo("Hasil Test Validasi", "\n".join(results))

    def test_data_operations(self):
        """Menguji operasi data seperti menambah, mengubah, dan menghapus data."""
        test_data = {
            "id": self.get_next_id(),
            "name": "Test Person",
            "date": "25/12/2023",
            "time": "08:00",
            "priority": False
        }

        results = []
        try:
            # Test menambah data
            self.birthdays.append(test_data)
            results.append("✓ Berhasil menambah data test")

            # Test mengubah data
            for birthday in self.birthdays:
                if birthday["id"] == test_data["id"]:
                    birthday["name"] = "Updated Test Person"
                    results.append("✓ Berhasil mengubah data test")
                    break

            # Test menghapus data
            self.birthdays = [b for b in self.birthdays if b["id"] != test_data["id"]]
            results.append("✓ Berhasil menghapus data test")

            # Simpan perubahan
            self.save_birthdays()
            results.append("✓ Berhasil menyimpan perubahan")

        except Exception as e:
            results.append(f"✗ Gagal: {str(e)}")

        # Tampilkan hasil test
        messagebox.showinfo("Hasil Test Operasi Data", "\n".join(results))

        # Refresh tampilan setelah testing
        self.refresh_birthdays()

    def refresh_birthdays(self):
        """Memperbarui daftar ulang tahun di TreeView dan juga memperbarui kalender"""
        for item in self.birthday_tree.get_children():
            self.birthday_tree.delete(item)

        # PENTING: Tentukan ID prioritas TERBARU SEBELUM mengisi ulang TreeView
        self.find_and_set_priority_target()

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
                is_priority_item = birthday.get("priority", False)
                item_id = birthday.get("id")

                if is_priority_item:
                    display_name += " ★"

                self.birthday_tree.insert("", tk.END, iid=tree_iid, values=(display_name, birthday["date"], age, f"{days_left} hari"), tags=(tag,))

                # Reset background/foreground ke default (putih/TEXT_COLOR)
                self.birthday_tree.tag_configure(tag, background="#FFFFFF", foreground=TEXT_COLOR)

                # --- Highlighting Logic ---
                # Highlight berdasarkan sisa hari (tanpa highlight khusus untuk hari H)
                if 0 < days_left <= 7:
                    self.birthday_tree.tag_configure(tag, background="#FFB6C1") # Pink for <= 7 days
                elif 7 < days_left <= 30:
                    self.birthday_tree.tag_configure(tag, background="#E6E6FA") # Lavender for <= 30 days

                # Highlight khusus untuk item yang AKTIF di countdown prioritas
                if item_id == self.priority_birthday_id:
                    # Gunakan warna frame prioritas
                    self.birthday_tree.tag_configure(tag, background=PRIORITY_COLOR, foreground=PRIORITY_TEXT_COLOR)
                # Jika hari H dan BUKAN prioritas aktif, beri warna lain (misal: light yellow)
                elif days_left == 0 and item_id != self.priority_birthday_id:
                     self.birthday_tree.tag_configure(tag, background="#FFFFE0") # Light Yellow untuk hari H non-prioritas

            except Exception as e:
                 print(f"Error menampilkan data (refresh) {birthday.get('name', 'N/A')} ke treeview: {e}")

        # self.find_and_set_priority_target() # <--- Baris ini dipindahkan ke atas

        # Update kalender jika ada
        if hasattr(self, 'calendar'):
            self.update_calendar_events()

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

    def create_calendar_tab(self):
        """Membuat tab kalender ulang tahun"""
        calendar_container = self.calendar_tab
        calendar_container.rowconfigure(1, weight=1)
        calendar_container.columnconfigure(0, weight=1)

        # Frame judul untuk tab kalender
        cal_title_border = tk.Frame(calendar_container, bg="#000000", bd=2, relief=tk.RAISED)
        cal_title_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5))
        cal_title_frame = tk.Frame(cal_title_border, bg=BG_COLOR, padx=10, pady=10)
        cal_title_frame.pack(fill=tk.X, padx=2, pady=2)
        cal_title_label = tk.Label(cal_title_frame, text="Kalender Ulang Tahun", font=(FONT_STYLE, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        cal_title_label.pack()

        # Frame utama untuk calendar
        cal_content_frame = tk.Frame(calendar_container, bg=BG_COLOR)
        cal_content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        cal_content_frame.columnconfigure(0, weight=2)  # Kolom kalender
        cal_content_frame.columnconfigure(1, weight=1)  # Kolom info
        cal_content_frame.rowconfigure(0, weight=1)

        # Frame untuk kalender
        cal_border = tk.Frame(cal_content_frame, bg="#000000", bd=2, relief=tk.RAISED)
        cal_border.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        cal_inner_frame = tk.Frame(cal_border, bg=ACCENT_COLOR, padx=10, pady=10)
        cal_inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Inisialisasi kalender
        current_date = datetime.now()
        self.calendar = Calendar(cal_inner_frame,
                               selectmode='day',
                               year=current_date.year,
                               month=current_date.month,
                               day=current_date.day,
                               font=(FONT_STYLE, 10),
                               background=CALENDAR_BG,
                               foreground=CALENDAR_FG,
                               bordercolor=CALENDAR_BORDER,
                               headersbackground=CALENDAR_HEADER_BG,
                               selectbackground=CALENDAR_SELECT_BG,
                               cursor="hand2")
        self.calendar.pack(fill=tk.BOTH, expand=True)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_select)

        # Frame untuk info ulang tahun
        info_border = tk.Frame(cal_content_frame, bg="#000000", bd=2, relief=tk.RAISED)
        info_border.grid(row=0, column=1, sticky="nsew")
        self.info_frame = tk.Frame(info_border, bg=ACCENT_COLOR, padx=10, pady=10)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Judul info
        info_title = tk.Label(self.info_frame, text="Informasi Ulang Tahun", font=(FONT_STYLE, 14, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        info_title.pack(pady=(0, 10))

        # Daftar ulang tahun untuk tanggal yang dipilih
        self.birthday_info_frame = tk.Frame(self.info_frame, bg=ACCENT_COLOR)
        self.birthday_info_frame.pack(fill=tk.BOTH, expand=True)

        # Label saat tidak ada ulang tahun
        self.no_birthday_label = tk.Label(self.birthday_info_frame, text="Tidak ada ulang tahun\npada tanggal ini",
                                       font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, justify=tk.CENTER)
        self.no_birthday_label.pack(expand=True)

        # Update kalender dengan tanda ulang tahun
        self.update_calendar_events()

    def create_settings_tab(self):
        """Membuat tab pengaturan aplikasi"""
        settings_container = self.settings_tab
        settings_container.rowconfigure(1, weight=1)
        settings_container.columnconfigure(0, weight=1)

        # Frame judul untuk tab pengaturan
        settings_title_border = tk.Frame(settings_container, bg="#000000", bd=2, relief=tk.RAISED)
        settings_title_border.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5))
        settings_title_frame = tk.Frame(settings_title_border, bg=BG_COLOR, padx=10, pady=10)
        settings_title_frame.pack(fill=tk.X, padx=2, pady=2)
        settings_title_label = tk.Label(settings_title_frame, text="Pengaturan Aplikasi", font=(FONT_STYLE, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        settings_title_label.pack()

        # Frame utama untuk pengaturan dengan scrollbar
        settings_content_border = tk.Frame(settings_container, bg="#000000", bd=2, relief=tk.RAISED)
        settings_content_border.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Tambahkan canvas dan scrollbar untuk scrolling
        canvas = tk.Canvas(settings_content_border, bg=ACCENT_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(settings_content_border, orient="vertical", command=canvas.yview)
        settings_content = tk.Frame(canvas, bg=ACCENT_COLOR, padx=20, pady=20)

        # Konfigurasi canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y", padx=0, pady=2)

        # Tambahkan frame ke canvas
        canvas_frame = canvas.create_window((0, 0), window=settings_content, anchor="nw")

        # Fungsi untuk mengatur ukuran canvas
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_frame, width=event.width)

        # Fungsi untuk scroll dengan mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind event untuk mengatur ukuran canvas dan mouse wheel
        canvas.bind("<Configure>", configure_canvas)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux
        settings_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))





        # --- Pengaturan Data ---
        data_frame = tk.Frame(settings_content, bg=ACCENT_COLOR, pady=10)
        data_frame.pack(fill=tk.X, anchor=tk.N)

        data_label = tk.Label(data_frame, text="Backup & Restore Data", font=(FONT_STYLE, 14, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        data_label.pack(anchor=tk.W)

        data_desc = tk.Label(data_frame, text="Ekspor data ulang tahun untuk backup atau impor dari file backup",
                                font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        data_desc.pack(anchor=tk.W, pady=(0, 10))

        data_buttons_frame = tk.Frame(data_frame, bg=ACCENT_COLOR)
        data_buttons_frame.pack(anchor=tk.W)

        def create_data_button(parent, text, command, bg_color):
            # Buat wrapper untuk command yang akan memainkan suara klik
            def command_with_sound():
                # Mainkan suara klik jika suara diaktifkan
                if self.sound_enabled_var.get() and IS_WINDOWS:
                    # Pilih file suara berdasarkan jenis suara yang dipilih
                    sound_type = self.sound_type_var.get()
                    if sound_type == "click1":
                        sound_file = "click1.wav"
                    elif sound_type == "click2":
                        sound_file = "click2.wav"
                    else:  # click3
                        sound_file = "click3.wav"

                    # Gunakan path absolut untuk file suara
                    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                    if os.path.exists(sound_path):
                        try:
                            # Gunakan SND_ASYNC agar tidak memblokir UI
                            print(f"Memainkan suara klik: {sound_path}")
                            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        except Exception as e:
                            print(f"Error memainkan suara klik: {e}")
                # Jalankan command asli
                command()

            btn_frame = tk.Frame(parent, bg="#000000", bd=2, relief=tk.RAISED)
            button = tk.Button(btn_frame, text=text, font=(FONT_STYLE, 12), command=command_with_sound,
                              bg=bg_color, fg=TEXT_COLOR, relief=tk.RAISED, padx=10, pady=5,
                              cursor="hand2", activebackground=self.adjust_color(bg_color, -20), activeforeground=TEXT_COLOR)
            button.pack(padx=2, pady=2)

            return btn_frame

        export_button = create_data_button(data_buttons_frame, "Ekspor Data", self.export_data, "#A0E7E5")
        export_button.pack(side=tk.LEFT, padx=(0, 10))

        import_button = create_data_button(data_buttons_frame, "Impor Data", self.import_data, "#B4F8C8")
        import_button.pack(side=tk.LEFT)

        ttk.Separator(settings_content, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)

        # --- Pengaturan Suara ---
        sound_frame = tk.Frame(settings_content, bg=ACCENT_COLOR, pady=10)
        sound_frame.pack(fill=tk.X, anchor=tk.N)

        sound_label = tk.Label(sound_frame, text="Pengaturan Suara", font=(FONT_STYLE, 14, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        sound_label.pack(anchor=tk.W)

        sound_desc = tk.Label(sound_frame, text="Aktifkan atau nonaktifkan efek suara dalam aplikasi",
                                font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        sound_desc.pack(anchor=tk.W, pady=(0, 10))

        # Buat frame khusus untuk checkbox agar lebih rapi dan terlihat jelas
        sound_checkbox_container = tk.Frame(sound_frame, bg=ACCENT_COLOR, padx=5, pady=5, bd=1, relief=tk.GROOVE)
        sound_checkbox_container.pack(anchor=tk.W, fill=tk.X)

        # Gunakan frame untuk checkbox agar lebih rapi
        sound_check = tk.Checkbutton(sound_checkbox_container, text="Aktifkan Suara", variable=self.sound_enabled_var,
                                    font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                    selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
                                    command=self.toggle_sound, padx=10, pady=5)
        sound_check.pack(anchor=tk.W, padx=10, pady=5)

        # Frame untuk pilihan jenis suara
        sound_type_frame = tk.Frame(sound_frame, bg=ACCENT_COLOR, padx=5, pady=5, bd=1, relief=tk.GROOVE)
        sound_type_frame.pack(anchor=tk.W, fill=tk.X, pady=(10, 0))

        sound_type_label = tk.Label(sound_type_frame, text=_("sound_type"), font=(FONT_STYLE, 12),
                                   bg=ACCENT_COLOR, fg=TEXT_COLOR, padx=10, pady=5)
        sound_type_label.pack(anchor=tk.W)

        # Radio button untuk gaya suara
        click1_radio = tk.Radiobutton(sound_type_frame, text=_("sound_click1"), variable=self.sound_type_var,
                                     value="click1", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                     selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
                                     command=self.change_sound_type, padx=10, pady=5)
        click1_radio.pack(anchor=tk.W, padx=20)

        click2_radio = tk.Radiobutton(sound_type_frame, text=_("sound_click2"), variable=self.sound_type_var,
                                     value="click2", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                     selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
                                     command=self.change_sound_type, padx=10, pady=5)
        click2_radio.pack(anchor=tk.W, padx=20)

        click3_radio = tk.Radiobutton(sound_type_frame, text=_("sound_click3"), variable=self.sound_type_var,
                                     value="click3", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                                     selectcolor=BG_COLOR, activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
                                     command=self.change_sound_type, padx=10, pady=5)
        click3_radio.pack(anchor=tk.W, padx=20)

        # Tombol untuk test suara
        sound_test_frame = tk.Frame(sound_frame, bg=ACCENT_COLOR, pady=10)
        sound_test_frame.pack(anchor=tk.W)

        test_sound_button = create_data_button(sound_test_frame, "Test Suara", self.test_sound, "#FFB6C1")
        test_sound_button.pack(side=tk.LEFT)

        ttk.Separator(settings_content, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)

        # --- Informasi Aplikasi ---
        info_frame = tk.Frame(settings_content, bg=ACCENT_COLOR, pady=10)
        info_frame.pack(fill=tk.X, anchor=tk.N)

        info_label = tk.Label(info_frame, text="Tentang Aplikasi", font=(FONT_STYLE, 14, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        info_label.pack(anchor=tk.W)

        version_label = tk.Label(info_frame, text="Birthday Timer Versi 2.0", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        version_label.pack(anchor=tk.W, pady=2)

        creator_label = tk.Label(info_frame, text="Dibuat oleh: @rfypych", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        creator_label.pack(anchor=tk.W, pady=2)

        # Gunakan tahun saat ini secara dinamis
        current_year = datetime.now().year
        copyright_label = tk.Label(info_frame, text=f"© {current_year} All Rights Reserved", font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        copyright_label.pack(anchor=tk.W, pady=2)

    def update_calendar_events(self):
        """Memperbarui kalender dengan menandai tanggal-tanggal ulang tahun"""
        # Konfigurasi tag dan hapus semua tanda sebelumnya (reset kalender)
        try:
            # Ganti dengan metode yang tepat untuk menghapus tag pada kalender
            # Jika _reset_day_tags() tidak ada, kita akan membuat ulang tag pada hari-hari yang diperlukan
            current_date = datetime.now().date()
            year = current_date.year
            month = current_date.month
            # Hapus tag pada seluruh hari di bulan ini
            for day in range(1, 32):
                try:
                    self.calendar.calevent_remove('all', day, month, year)
                except:
                    # Jika hari tidak valid untuk bulan ini, lanjutkan
                    pass
        except Exception as e:
            print(f"Error saat mereset calendar: {e}")

        # Dictionary untuk menyimpan data ulang tahun berdasarkan tanggal
        self.calendar_events = {}

        # Tandai tanggal-tanggal ulang tahun
        current_date = datetime.now().date()
        current_year = current_date.year

        for birthday in self.birthdays:
            try:
                day, month, year = map(int, birthday["date"].split('/'))
                birthday_date = datetime(current_year, month, day).date()

                # Jika ulang tahun sudah lewat tahun ini, tampilkan untuk tahun depan
                if birthday_date < current_date:
                    birthday_date = datetime(current_year + 1, month, day).date()

                # Format tanggal untuk dictionary
                date_str = birthday_date.strftime("%Y-%m-%d")

                # Tambahkan ke dictionary event
                if date_str not in self.calendar_events:
                    self.calendar_events[date_str] = []
                self.calendar_events[date_str].append(birthday)

                # Tentukan tag berdasarkan prioritas dan tanggal
                tag_type = 'priority' if birthday.get("priority", False) else 'birthday'
                if birthday_date == current_date:
                    tag_type = 'today_birthday'

                # Tambahkan event pada kalender menggunakan calevent_create
                # Format: calevent_create(date, text, tags)
                event_text = birthday.get("name", "Ulang Tahun")

                # Konfigurasi warna untuk tag
                if tag_type == 'today_birthday':
                    self.calendar.tag_config('today_birthday', background='#AFEEEE', foreground='black')
                    self.calendar.calevent_create(birthday_date, event_text, 'today_birthday')
                elif tag_type == 'priority':
                    self.calendar.tag_config('priority', background='#FFD700', foreground='white')
                    self.calendar.calevent_create(birthday_date, event_text, 'priority')
                else:
                    self.calendar.tag_config('birthday', background='#FFB6C1', foreground='black')
                    self.calendar.calevent_create(birthday_date, event_text, 'birthday')

            except ValueError:
                print(f"Format tanggal tidak valid untuk {birthday.get('name', 'N/A')}")
            except Exception as e:
                print(f"Error menampilkan ulang tahun di kalender: {e}")

    def on_calendar_select(self, event=None):
        """Handler ketika tanggal di kalender dipilih"""
        selected_date = self.calendar.selection_get()
        date_str = selected_date.strftime("%Y-%m-%d")

        # Bersihkan frame info sebelum menambahkan yang baru
        for widget in self.birthday_info_frame.winfo_children():
            widget.destroy()

        # Cek apakah ada ulang tahun pada tanggal yang dipilih
        if date_str not in self.calendar_events or not self.calendar_events[date_str]:
            # Tampilkan pesan tidak ada ulang tahun
            self.no_birthday_label = tk.Label(self.birthday_info_frame, text="Tidak ada ulang tahun\npada tanggal ini",
                                           font=(FONT_STYLE, 12), bg=ACCENT_COLOR, fg=TEXT_COLOR, justify=tk.CENTER)
            self.no_birthday_label.pack(expand=True)
            return

        # Tampilkan daftar ulang tahun pada tanggal yang dipilih
        for i, birthday_data in enumerate(self.calendar_events[date_str]):
            is_today = (selected_date == datetime.now().date())
            is_priority = birthday_data.get("priority", False)
            item_id = birthday_data.get("id") # Get the ID of the birthday being displayed

            bg_color = "#FFFFFF" # Default background (putih)
            fg_color = TEXT_COLOR # Default text color
            icon = ""

            # --- Logika Penentuan Style Baru ---
            tag = 'birthday' # Default tag
            if is_priority:
                tag = 'priority'
            if is_today: # Jika tanggal yg dipilih = hari ini, override tag
                tag = 'today_birthday'

            # Tetapkan warna dan ikon berdasarkan tag final
            if tag == 'today_birthday':
                bg_color = "#AFEEEE" # Ubah dari Gold menjadi PaleTurquoise (Biru Muda)
                icon = " 🎂🎀 " # Tambahkan ikon pita
                fg_color = TEXT_COLOR # Pastikan teks kontras
            elif tag == 'priority':
                bg_color = "#FFD700" # Warna Emas untuk Prioritas
                icon = " ⭐"
                fg_color = TEXT_COLOR # Ubah dari PRIORITY_TEXT_COLOR menjadi TEXT_COLOR agar kontras
            else: # tag == 'birthday'
                 # Warna berdasarkan kedekatan untuk ultah biasa
                 try:
                     day, month, year = map(int, birthday_data["date"].split('/'))
                     hour, minute = map(int, birthday.get("time", "00:00").split(':'))
                     current_dt = datetime.now()
                     target_dt_this_year = datetime(current_dt.year, month, day, hour, minute)
                     if datetime(current_dt.year, month, day, 23, 59, 59) < current_dt:
                         next_birthday_dt = datetime(current_dt.year + 1, month, day, hour, minute)
                     else:
                         next_birthday_dt = target_dt_this_year
                     days_left = (next_birthday_dt - current_dt).days
                     if days_left < 0: days_left = 0

                     if 0 < days_left <= 7:
                         bg_color = "#FFB6C1" # Pink
                     elif 7 < days_left <= 30:
                          bg_color = "#E6E6FA" # Lavender
                     # else: bg_color tetap default putih
                 except:
                      pass # Biarkan bg_color putih jika ada error parsing
                 icon = ""
                 fg_color = TEXT_COLOR

            # Buat frame info untuk masing-masing ulang tahun
            if tag == 'today_birthday':
                # Frame khusus untuk ulang tahun hari ini dengan dekorasi
                outer_frame = tk.Frame(self.birthday_info_frame, bg="#FF6B6B", bd=4, relief=tk.GROOVE)  # Warna oranye cerah untuk border
                outer_frame.pack(fill=tk.X, expand=False, pady=5)
                event_frame = tk.Frame(outer_frame, bg=bg_color, pady=8, padx=8)  # Padding lebih besar
                event_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            else:
                # Frame biasa untuk ulang tahun lainnya
                event_frame = tk.Frame(self.birthday_info_frame, bg=bg_color, pady=5, padx=5, bd=1, relief=tk.RAISED)
                event_frame.pack(fill=tk.X, expand=False, pady=5)

            # Tampilkan nama dengan ikon khusus jika perlu
            name = birthday_data["name"]
            name_with_icon = f"{name}{icon}"

            name_label = tk.Label(event_frame, text=name_with_icon, font=(FONT_STYLE, 12, "bold"),
                                bg=bg_color, fg=fg_color) # Gunakan fg_color yg ditentukan
            name_label.pack(anchor=tk.W)

            # Tampilkan tanggal lahir dan umur
            try:
                day, month, year = map(int, birthday_data["date"].split('/'))
                current_year = datetime.now().year
                age = current_year - year
                if (month, day) > (datetime.now().month, datetime.now().day):
                    age -= 1
                age = max(0, age)

                date_label = tk.Label(event_frame, text=f"Tanggal Lahir: {day}/{month}/{year}", font=(FONT_STYLE, 10),
                                   bg=bg_color, fg=fg_color) # Gunakan fg_color
                date_label.pack(anchor=tk.W)

                age_label = tk.Label(event_frame, text=f"Umur: {age} tahun", font=(FONT_STYLE, 10),
                                 bg=bg_color, fg=fg_color) # Gunakan fg_color
                age_label.pack(anchor=tk.W)

                time_label = tk.Label(event_frame, text=f"Waktu Notifikasi: {birthday_data.get('time', '00:00')}", font=(FONT_STYLE, 10),
                                  bg=bg_color, fg=fg_color) # Gunakan fg_color
                time_label.pack(anchor=tk.W)
            except Exception as e:
                print(f"Error menampilkan detail tanggal lahir: {e}")

    def export_data(self):
        """Membuka dialog untuk mengekspor data ulang tahun"""
        def process_export_result(result):
            if result:
                self.flash_status("✓ Data berhasil diekspor!")

        dialog = ExportDialog(self.root, self.birthdays, process_export_result)

    def import_data(self):
        """Membuka dialog untuk mengimpor data ulang tahun"""
        def process_import_result(result):
            if not result:
                return

            try:
                mode = result["mode"]
                imported_data = result["data"]

                if mode == "replace":
                    # Ganti semua data
                    self.birthdays = imported_data.copy()
                else:  # mode == "merge"
                    # Gabungkan data, hapus duplikat berdasarkan ID
                    # Buat dictionary dari data yang ada untuk memudahkan pencarian ID
                    existing_ids = {b.get("id"): i for i, b in enumerate(self.birthdays) if "id" in b}

                    for imported_item in imported_data:
                        if "id" in imported_item and imported_item["id"] in existing_ids:
                            # Update data yang sudah ada
                            self.birthdays[existing_ids[imported_item["id"]]] = imported_item
                        else:
                            # Tambahkan data baru dengan ID baru jika tidak ada ID
                            if "id" not in imported_item:
                                imported_item["id"] = self.get_next_id()
                            self.birthdays.append(imported_item)

                # Simpan perubahan
                self.save_birthdays()

                # Refresh tampilan
                self.refresh_birthdays()
                self.update_calendar_events()

                # Tampilkan pesan sukses
                self.flash_status(f"✓ Berhasil mengimpor {len(imported_data)} data!")

            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengimpor data: {str(e)}")

        dialog = ImportDialog(self.root, process_import_result)



    def toggle_sound(self):
        """Mengaktifkan atau menonaktifkan efek suara"""
        try:
            enabled = self.sound_enabled_var.get()

            # Mainkan suara test jika diaktifkan
            if enabled:
                # Pilih file suara berdasarkan jenis suara yang dipilih
                sound_type = self.sound_type_var.get()
                if sound_type == "click1":
                    sound_file = "click1.wav"
                elif sound_type == "click2":
                    sound_file = "click2.wav"
                else:  # click3
                    sound_file = "click3.wav"

                # Gunakan path absolut untuk file suara
                sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                if os.path.exists(sound_path) and IS_WINDOWS:
                    try:
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception as e:
                        print(f"Error memainkan suara toggle: {e}")
                self.flash_status(_("sound_enabled"))
            else:
                self.flash_status(_("sound_disabled"))

            # Simpan pengaturan
            self.save_settings()
        except Exception as e:
            messagebox.showerror(_("error"), f"Gagal mengubah pengaturan suara: {str(e)}")

    def change_sound_type(self):
        """Mengubah jenis suara ASMR"""
        try:
            sound_type = self.sound_type_var.get()

            # Mainkan suara test jika suara diaktifkan
            if self.sound_enabled_var.get():
                if sound_type == "click1":
                    sound_file = "click1.wav"
                    self.flash_status(_("sound_changed_click1"))
                elif sound_type == "click2":
                    sound_file = "click2.wav"
                    self.flash_status(_("sound_changed_click2"))
                else:  # click3
                    sound_file = "click3.wav"
                    self.flash_status(_("sound_changed_click3"))

                # Gunakan path absolut untuk file suara
                sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds", sound_file)
                if os.path.exists(sound_path) and IS_WINDOWS:
                    try:
                        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    except Exception as e:
                        print(f"Error memainkan suara saat mengubah jenis: {e}")

            # Simpan pengaturan
            self.save_settings()
        except Exception as e:
            messagebox.showerror(_("error"), _("error_change_sound", error=str(e)))



    def save_settings(self):
        """Menyimpan pengaturan aplikasi"""
        try:
            settings = {
                "sound_enabled": self.sound_enabled_var.get(),
                "sound_type": self.sound_type_var.get()
            }

            with open("settings.json", "w") as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        """Memuat pengaturan aplikasi"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as file:
                    settings = json.load(file)

                    # Terapkan pengaturan
                    if "sound_enabled" in settings:
                        self.sound_enabled_var.set(settings["sound_enabled"])

                    if "sound_type" in settings:
                        self.sound_type_var.set(settings["sound_type"])
        except Exception as e:
            print(f"Error loading settings: {e}")

    def test_sound(self):
        """Menguji efek suara ASMR"""
        try:
            # Mainkan semua suara secara berurutan
            if not self.sound_enabled_var.get():
                messagebox.showinfo("Info", "Suara sedang dinonaktifkan. Aktifkan suara terlebih dahulu.")
                return

            # Gunakan path absolut untuk file suara
            base_dir = os.path.dirname(os.path.abspath(__file__))

            # Pilih jenis suara berdasarkan pengaturan
            sound_type = self.sound_type_var.get()
            if sound_type == "click1":
                sound_file = "click1.wav"
                sound_name = _("sound_click1").replace(":", "")
            elif sound_type == "click2":
                sound_file = "click2.wav"
                sound_name = _("sound_click2").replace(":", "")
            else:  # click3
                sound_file = "click3.wav"
                sound_name = _("sound_click3").replace(":", "")

            # Tampilkan dialog informasi
            messagebox.showinfo(_("test_sound_title"), _("test_sound_message", sound_name=sound_name))

            # Mainkan suara yang dipilih
            sound_path = os.path.join(base_dir, "sounds", sound_file)
            if os.path.exists(sound_path) and IS_WINDOWS:
                try:
                    print(f"Memainkan suara: {sound_path}")
                    winsound.PlaySound(sound_path, winsound.SND_FILENAME)
                except Exception as e:
                    print(f"Error memainkan suara: {e}")
            self.flash_status(_("test_sound_success"))
        except Exception as e:
            messagebox.showerror(_("error"), _("error_sound", error=str(e)))

    def test_sound_direct(self):
        """Menguji efek suara ASMR secara langsung tanpa SoundManager"""
        try:
            # Pilih jenis suara berdasarkan pengaturan
            sound_type = self.sound_type_var.get()
            if sound_type == "click1":
                sound_file = "click1.wav"
                sound_name = _("sound_click1").replace(":", "")
            elif sound_type == "click2":
                sound_file = "click2.wav"
                sound_name = _("sound_click2").replace(":", "")
            else:  # click3
                sound_file = "click3.wav"
                sound_name = _("sound_click3").replace(":", "")

            # Tampilkan dialog informasi
            messagebox.showinfo(_("test_sound_title"), _("test_sound_message", sound_name=sound_name))

            # Gunakan path absolut untuk file suara
            base_dir = os.path.dirname(os.path.abspath(__file__))

            # Periksa keberadaan file suara
            sound_path = os.path.join(base_dir, "sounds", sound_file)

            if not os.path.exists(sound_path):
                messagebox.showwarning(_("warning"), _("file_not_found", files=sound_path))
                return

            # Mainkan suara (langsung, bukan async)
            if IS_WINDOWS:
                try:
                    print(f"Memainkan suara: {sound_path}")
                    winsound.PlaySound(sound_path, winsound.SND_FILENAME)
                except Exception as e:
                    print(f"Error memainkan suara: {e}")

                self.flash_status(_("test_sound_success"))
            else:
                messagebox.showinfo(_("info"), _("sound_not_supported"))
        except Exception as e:
            messagebox.showerror(_("error"), _("error_sound", error=str(e)))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        style = ttk.Style()
        # Gunakan theme 'clam' yang mendukung kostumisasi warna lebih baik
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif IS_WINDOWS and 'vista' in available_themes:
             style.theme_use('vista')

        # Konfigurasi khusus untuk DateEntry/Calendar jika digunakan
        style.configure('my.DateEntry', fieldbackground=CALENDAR_BG,
                       background=CALENDAR_HEADER_BG, foreground=CALENDAR_FG)

        app = BirthdayReminderApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error Aplikasi", f"Terjadi kesalahan fatal: {str(e)}")