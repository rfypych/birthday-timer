import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time
from PIL import Image, ImageTk

# Import modul pixel_ui dan notification
from pixel_ui import PixelUI
from notification import BirthdayNotifier

# Konstanta
TITLE = "Pengingat Ulang Tahun Aira"
WIDTH = 800
HEIGHT = 600
BG_COLOR = "#FFD1DC"  # Pink pastel
ACCENT_COLOR = "#FFACB7"  # Pink pastel lebih tua
TEXT_COLOR = "#6B5876"  # Ungu tua
BUTTON_COLOR = "#B5EAD7"  # Hijau mint pastel
FONT_STYLE = "Courier New"  # Akan digunakan sebagai font pixel-style

# Fungsi untuk membuat file data jika belum ada
def create_data_file():
    if not os.path.exists("birthdays.json"):
        with open("birthdays.json", "w") as file:
            json.dump([], file)

# Kelas utama aplikasi
class BirthdayReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Inisialisasi notifier
        self.notifier = BirthdayNotifier()
        
        # Panggil fungsi untuk membuat file data
        create_data_file()
        
        # Membuat icon kue ulang tahun
        icon_path = "cake_icon.ico"
        if not os.path.exists(icon_path):
            icon_path = self.notifier.create_birthday_icon(icon_path)
            
        # Set ikon aplikasi jika berhasil dibuat
        if icon_path and os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Memuat data ulang tahun
        self.birthdays = self.load_birthdays()
        
        # Membuat UI
        self.create_ui()
        
        # Mulai thread untuk cek notifikasi
        self.notification_thread = threading.Thread(target=self.check_notifications, daemon=True)
        self.notification_thread.start()
    
    def create_ui(self):
        # Header label
        header_frame = tk.Frame(self.root, bg=BG_COLOR, pady=20)
        header_frame.pack(fill=tk.X)
        
        # Judul dengan gaya pixel art
        pixel_title = tk.Label(
            header_frame, 
            text="✨ Pengingat Ulang Tahun ✨", 
            font=(FONT_STYLE, 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        pixel_title.pack()
        
        subtitle_label = tk.Label(
            header_frame, 
            text="Untuk Aira Jesslyn Seniara", 
            font=(FONT_STYLE, 16),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        subtitle_label.pack(pady=5)
        
        # Form untuk menambahkan ulang tahun
        input_frame = tk.Frame(self.root, bg=ACCENT_COLOR, padx=20, pady=20)
        input_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Gunakan entry gaya pixel
        name_label = tk.Label(
            input_frame, 
            text="Nama:", 
            font=(FONT_STYLE, 12),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR
        )
        name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Menggunakan entry gaya pixel
        name_frame, self.name_entry = PixelUI.create_pixel_entry(
            input_frame, 
            width=30, 
            font_style=FONT_STYLE, 
            font_size=12
        )
        name_frame.grid(row=0, column=1, padx=10, pady=5)
        
        date_label = tk.Label(
            input_frame, 
            text="Tanggal (DD/MM/YYYY):", 
            font=(FONT_STYLE, 12),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR
        )
        date_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Menggunakan entry gaya pixel
        date_frame, self.date_entry = PixelUI.create_pixel_entry(
            input_frame, 
            width=30, 
            font_style=FONT_STYLE, 
            font_size=12
        )
        date_frame.grid(row=1, column=1, padx=10, pady=5)
        
        # Buat tombol bergaya pixel
        save_button = PixelUI.create_pixel_button(
            input_frame, 
            "Simpan", 
            self.add_birthday,
            bg_color=BUTTON_COLOR
        )
        save_button.grid(row=2, column=0, columnspan=2, pady=15)
        
        # List ulang tahun
        list_frame = tk.Frame(self.root, bg=BG_COLOR, padx=50, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        list_label = tk.Label(
            list_frame, 
            text="Daftar Ulang Tahun", 
            font=(FONT_STYLE, 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        list_label.pack(pady=10)
        
        # Treeview untuk menampilkan daftar ulang tahun
        columns = ("Nama", "Tanggal", "Umur", "Hari Lagi")
        self.birthday_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Mengatur style untuk treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        font=(FONT_STYLE, 10),
                        rowheight=25,
                        background="#FFFFFF",
                        foreground=TEXT_COLOR)
        style.configure("Treeview.Heading", 
                        font=(FONT_STYLE, 10, "bold"),
                        background=ACCENT_COLOR,
                        foreground=TEXT_COLOR)
        
        # Mengatur heading kolom
        for col in columns:
            self.birthday_tree.heading(col, text=col)
            self.birthday_tree.column(col, width=int(WIDTH/5), anchor=tk.CENTER)
        
        # Menambahkan scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.birthday_tree.yview)
        self.birthday_tree.configure(yscrollcommand=scrollbar.set)
        
        self.birthday_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tombol-tombol operasi
        button_frame = tk.Frame(list_frame, bg=BG_COLOR, pady=10)
        button_frame.pack(fill=tk.X)
        
        edit_button = PixelUI.create_pixel_button(
            button_frame, 
            "Edit", 
            self.edit_birthday,
            bg_color="#A0E7E5"  # Biru pastel
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = PixelUI.create_pixel_button(
            button_frame, 
            "Hapus", 
            self.delete_birthday,
            bg_color="#FBE7C6"  # Kuning pastel
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = PixelUI.create_pixel_button(
            button_frame, 
            "Refresh", 
            self.refresh_birthdays,
            bg_color="#B4F8C8"  # Hijau pastel
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Tambahkan tombol untuk startup aplikasi
        startup_button = PixelUI.create_pixel_button(
            button_frame,
            "Jalankan Saat Startup",
            self.toggle_startup,
            bg_color="#FFCE5C"  # Oranye pastel
        )
        startup_button.pack(side=tk.RIGHT, padx=20)
        
        # Update list ulang tahun
        self.refresh_birthdays()
    
    def load_birthdays(self):
        try:
            with open("birthdays.json", "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
            return []
    
    def save_birthdays(self):
        try:
            with open("birthdays.json", "w") as file:
                json.dump(self.birthdays, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")
    
    def add_birthday(self):
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()
        
        if not name or not date_str:
            messagebox.showwarning("Peringatan", "Nama dan tanggal harus diisi!")
            return
        
        try:
            # Validasi format tanggal
            day, month, year = map(int, date_str.split('/'))
            birthday_date = datetime(year, month, day).strftime("%d/%m/%Y")
            
            # Tambahkan data baru
            new_birthday = {
                "id": len(self.birthdays) + 1,
                "name": name,
                "date": birthday_date
            }
            
            self.birthdays.append(new_birthday)
            self.save_birthdays()
            self.refresh_birthdays()
            
            # Reset form
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            
            messagebox.showinfo("Sukses", f"Ulang tahun {name} berhasil ditambahkan!")
            
            # Tampilkan notifikasi jika ulang tahun dalam 7 hari
            self.check_notification_for_birthday(new_birthday)
            
        except ValueError:
            messagebox.showerror("Error", "Format tanggal tidak valid. Gunakan format DD/MM/YYYY")
    
    def edit_birthday(self):
        selected_item = self.birthday_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih satu data untuk diedit!")
            return
        
        item_index = int(selected_item[0].replace('I', '')) - 1
        if 0 <= item_index < len(self.birthdays):
            birthday = self.birthdays[item_index]
            
            # Buat jendela edit
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Ulang Tahun")
            edit_window.configure(bg=BG_COLOR)
            edit_window.geometry("400x200")
            edit_window.resizable(False, False)
            
            # Form edit
            edit_frame = tk.Frame(edit_window, bg=ACCENT_COLOR, padx=20, pady=20)
            edit_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            tk.Label(
                edit_frame, 
                text="Nama:", 
                font=(FONT_STYLE, 12),
                bg=ACCENT_COLOR,
                fg=TEXT_COLOR
            ).grid(row=0, column=0, sticky=tk.W, pady=5)
            
            # Menggunakan entry gaya pixel
            name_frame, name_entry = PixelUI.create_pixel_entry(
                edit_frame, 
                width=25, 
                font_style=FONT_STYLE, 
                font_size=12
            )
            name_entry.insert(0, birthday["name"])
            name_frame.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(
                edit_frame, 
                text="Tanggal (DD/MM/YYYY):", 
                font=(FONT_STYLE, 12),
                bg=ACCENT_COLOR,
                fg=TEXT_COLOR
            ).grid(row=1, column=0, sticky=tk.W, pady=5)
            
            # Menggunakan entry gaya pixel
            date_frame, date_entry = PixelUI.create_pixel_entry(
                edit_frame, 
                width=25, 
                font_style=FONT_STYLE, 
                font_size=12
            )
            date_entry.insert(0, birthday["date"])
            date_frame.grid(row=1, column=1, padx=10, pady=5)
            
            # Fungsi untuk menyimpan perubahan
            def save_changes():
                try:
                    # Validasi format tanggal
                    new_name = name_entry.get().strip()
                    new_date_str = date_entry.get().strip()
                    day, month, year = map(int, new_date_str.split('/'))
                    new_date = datetime(year, month, day).strftime("%d/%m/%Y")
                    
                    if not new_name or not new_date_str:
                        messagebox.showwarning("Peringatan", "Nama dan tanggal harus diisi!")
                        return
                    
                    # Update data
                    self.birthdays[item_index]["name"] = new_name
                    self.birthdays[item_index]["date"] = new_date
                    self.save_birthdays()
                    self.refresh_birthdays()
                    
                    # Periksa apakah perlu notifikasi setelah update
                    self.check_notification_for_birthday(self.birthdays[item_index])
                    
                    edit_window.destroy()
                    messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                    
                except ValueError:
                    messagebox.showerror("Error", "Format tanggal tidak valid. Gunakan format DD/MM/YYYY")
            
            # Tombol simpan
            save_btn = PixelUI.create_pixel_button(
                edit_frame,
                "Simpan Perubahan",
                save_changes,
                bg_color=BUTTON_COLOR
            )
            save_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    def delete_birthday(self):
        selected_item = self.birthday_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih satu data untuk dihapus!")
            return
        
        item_index = int(selected_item[0].replace('I', '')) - 1
        if 0 <= item_index < len(self.birthdays):
            confirm = messagebox.askyesno(
                "Konfirmasi", 
                f"Hapus ulang tahun {self.birthdays[item_index]['name']}?"
            )
            
            if confirm:
                del self.birthdays[item_index]
                # Update IDs untuk konsistensi
                for i, birthday in enumerate(self.birthdays):
                    birthday["id"] = i + 1
                self.save_birthdays()
                self.refresh_birthdays()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    
    def refresh_birthdays(self):
        # Hapus semua item di treeview
        for item in self.birthday_tree.get_children():
            self.birthday_tree.delete(item)
        
        # Hitung hari yang tersisa dan umur
        current_date = datetime.now()
        current_year = current_date.year
        
        for i, birthday in enumerate(self.birthdays):
            day, month, year = map(int, birthday["date"].split('/'))
            birth_date = datetime(year, month, day)
            
            # Hitung umur
            age = current_year - year
            
            # Hitung hari tersisa
            next_birthday = datetime(current_year, month, day)
            if next_birthday < current_date:
                next_birthday = datetime(current_year + 1, month, day)
                age += 1  # Umur pada saat ulang tahun berikutnya
            
            days_left = (next_birthday - current_date).days
            
            # Pilih warna untuk highlight jika ulang tahun dekat
            tag = f"birthday_{i}"
            
            self.birthday_tree.insert(
                "",
                tk.END,
                iid=f"I{i+1}",
                values=(birthday["name"], birthday["date"], age, f"{days_left} hari"),
                tags=(tag,)
            )
            
            # Warnai baris sesuai kedekatan ulang tahun
            if days_left == 0:
                self.birthday_tree.tag_configure(tag, background="#FFD700")  # Gold untuk hari ini
            elif days_left <= 7:
                self.birthday_tree.tag_configure(tag, background="#FFB6C1")  # Light pink untuk minggu ini
            elif days_left <= 30:
                self.birthday_tree.tag_configure(tag, background="#E6E6FA")  # Lavender untuk bulan ini
    
    def check_notification_for_birthday(self, birthday):
        """Periksa apakah perlu menampilkan notifikasi untuk satu data ulang tahun"""
        current_date = datetime.now()
        current_year = current_date.year
        
        try:
            day, month, year = map(int, birthday["date"].split('/'))
            
            next_birthday = datetime(current_year, month, day)
            if next_birthday < current_date:
                next_birthday = datetime(current_year + 1, month, day)
            
            days_left = (next_birthday - current_date).days
            
            # Notifikasi jika ulang tahun dalam 7 hari atau hari ini
            if 0 <= days_left <= 7:
                # Buat kunci unik untuk notifikasi ini
                notification_key = f"{birthday['id']}_{days_left}"
                
                # Cek apakah notifikasi sudah ditampilkan
                if notification_key not in self.notifier.shown_notifications:
                    if days_left == 0:
                        title = "Selamat Ulang Tahun!"
                        message = f"Hari ini adalah ulang tahun {birthday['name']}!"
                    else:
                        title = "Pengingat Ulang Tahun"
                        message = f"Ulang tahun {birthday['name']} dalam {days_left} hari lagi!"
                    
                    # Tampilkan notifikasi
                    icon_path = "cake_icon.ico" if os.path.exists("cake_icon.ico") else None
                    self.notifier.show_notification(title, message, icon_path)
                    self.notifier.shown_notifications.add(notification_key)
        except Exception as e:
            print(f"Error saat memeriksa notifikasi: {str(e)}")
    
    def check_notifications(self):
        """Fungsi yang berjalan di thread terpisah untuk memeriksa notifikasi secara berkala"""
        while True:
            # Cek notifikasi untuk semua ulang tahun
            notifications = self.notifier.check_birthdays(self.birthdays)
            
            for notification in notifications:
                # Tampilkan notifikasi
                icon_path = "cake_icon.ico" if os.path.exists("cake_icon.ico") else None
                self.notifier.show_notification(
                    notification["title"], 
                    notification["message"], 
                    icon_path
                )
                # Tandai notifikasi telah ditampilkan
                self.notifier.shown_notifications.add(notification["key"])
            
            # Reset notifikasi pada tengah malam
            current_time = datetime.now()
            if current_time.hour == 0 and current_time.minute == 0:
                self.notifier.reset_daily_notifications()
            
            # Refresh tampilan
            self.root.after(0, self.refresh_birthdays)
            
            # Cek setiap jam
            time.sleep(3600)
    
    def toggle_startup(self):
        """Toggle pengaturan startup aplikasi"""
        # Dapatkan path aplikasi
        app_path = os.path.abspath(sys.argv[0])
        
        # Periksa apakah sudah terdaftar di startup
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, "BirthdayReminder")
                is_registered = True
            except:
                is_registered = False
            winreg.CloseKey(key)
        except:
            is_registered = False
        
        if is_registered:
            # Jika sudah terdaftar, hapus dari startup
            if self.notifier.remove_startup():
                messagebox.showinfo("Info", "Aplikasi berhasil dihapus dari startup Windows.")
            else:
                messagebox.showerror("Error", "Gagal menghapus aplikasi dari startup Windows.")
        else:
            # Jika belum terdaftar, tambahkan ke startup
            if self.notifier.set_startup(app_path):
                messagebox.showinfo("Info", "Aplikasi akan berjalan otomatis saat Windows startup.")
            else:
                messagebox.showerror("Error", "Gagal menambahkan aplikasi ke startup Windows.")

if __name__ == "__main__":
    import sys
    root = tk.Tk()
    app = BirthdayReminderApp(root)
    root.mainloop() 