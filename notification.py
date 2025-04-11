import os
import sys
import datetime
from PIL import Image, ImageDraw

# Cek jika berada di lingkungan Windows
IS_WINDOWS = sys.platform.startswith('win')

# Import library notifikasi sesuai platform
if IS_WINDOWS:
    from win10toast import ToastNotifier
    import winreg
else:
    ToastNotifier = None  # Jika tidak di Windows, gunakan fallback ke messagebox

class BirthdayNotifier:
    """Kelas untuk mengelola notifikasi ulang tahun"""
    
    def __init__(self):
        """Inisialisasi sistem notifikasi"""
        self.toast = ToastNotifier() if IS_WINDOWS else None
        # Simpan notifikasi yang telah ditampilkan hari ini
        self.shown_notifications = set()
    
    def show_notification(self, title, message, icon_path=None, duration=10):
        """
        Menampilkan notifikasi sistem
        
        Args:
            title: Judul notifikasi
            message: Pesan notifikasi
            icon_path: Path ke file ikon (opsional)
            duration: Durasi notifikasi dalam detik (default 10 detik)
            
        Returns:
            Boolean yang menunjukkan apakah notifikasi berhasil ditampilkan
        """
        if IS_WINDOWS and self.toast:
            try:
                # Menggunakan win10toast untuk menampilkan notifikasi Windows
                icon_path = icon_path if icon_path and os.path.exists(icon_path) else None
                return self.toast.show_toast(
                    title,
                    message,
                    icon_path=icon_path,
                    duration=duration,
                    threaded=True
                )
            except Exception as e:
                print(f"Error menampilkan notifikasi: {str(e)}")
                return False
        else:
            # Fallback untuk platform non-Windows (akan menggunakan messagebox di Tkinter)
            print(f"Notifikasi: {title} - {message}")
            return False
    
    def check_birthdays(self, birthdays, days_threshold=7):
        """
        Memeriksa ulang tahun yang akan datang dan menampilkan notifikasi
        
        Args:
            birthdays: List data ulang tahun
            days_threshold: Batas hari untuk menampilkan notifikasi (default 7 hari)
            
        Returns:
            List notifikasi yang ditampilkan
        """
        notifications = []
        current_date = datetime.datetime.now()
        current_year = current_date.year
        
        for birthday in birthdays:
            try:
                # Parse tanggal ulang tahun
                day, month, year = map(int, birthday["date"].split('/'))
                
                # Hitung tanggal ulang tahun berikutnya
                next_birthday = datetime.datetime(current_year, month, day)
                if next_birthday < current_date:
                    next_birthday = datetime.datetime(current_year + 1, month, day)
                
                # Hitung selisih hari
                days_left = (next_birthday - current_date).days
                
                # Buat notifikasi jika dalam threshold
                if 0 <= days_left <= days_threshold:
                    # Buat kunci unik untuk notifikasi ini
                    notification_key = f"{birthday['id']}_{days_left}"
                    
                    # Cek apakah notifikasi sudah ditampilkan hari ini
                    if notification_key not in self.shown_notifications:
                        if days_left == 0:
                            title = "Selamat Ulang Tahun!"
                            message = f"Hari ini adalah ulang tahun {birthday['name']}!"
                        else:
                            title = "Pengingat Ulang Tahun"
                            message = f"Ulang tahun {birthday['name']} dalam {days_left} hari lagi!"
                        
                        notifications.append({
                            "title": title,
                            "message": message,
                            "key": notification_key
                        })
            except Exception as e:
                print(f"Error saat memeriksa ulang tahun: {str(e)}")
        
        return notifications
    
    def set_startup(self, app_path, app_name="BirthdayReminder"):
        """
        Mengatur aplikasi agar berjalan saat startup Windows
        
        Args:
            app_path: Path lengkap ke aplikasi
            app_name: Nama aplikasi di registry
            
        Returns:
            Boolean yang menunjukkan apakah pengaturan berhasil
        """
        if not IS_WINDOWS:
            return False
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Tambahkan ke registry
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error saat menambahkan ke startup: {str(e)}")
            return False
    
    def remove_startup(self, app_name="BirthdayReminder"):
        """
        Menghapus aplikasi dari startup Windows
        
        Args:
            app_name: Nama aplikasi di registry
            
        Returns:
            Boolean yang menunjukkan apakah penghapusan berhasil
        """
        if not IS_WINDOWS:
            return False
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Hapus dari registry
            winreg.DeleteValue(key, app_name)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error saat menghapus dari startup: {str(e)}")
            return False
    
    def create_birthday_icon(self, output_path="cake_icon.ico", size=256):
        """
        Membuat ikon kue ulang tahun untuk notifikasi
        
        Args:
            output_path: Path output untuk file ikon
            size: Ukuran ikon
            
        Returns:
            Path ke file ikon yang dibuat
        """
        try:
            # Buat gambar baru
            image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Warna-warna
            cake_color = (251, 231, 198)  # #FBE7C6
            candle_color = (255, 107, 107)  # #FF6B6B
            flame_color = (255, 206, 92)  # #FFCE5C
            
            # Buat kue (persegi panjang)
            cake_top = int(size * 0.6)
            cake_bottom = int(size * 0.9)
            draw.rectangle([(int(size * 0.1), cake_top), (int(size * 0.9), cake_bottom)], fill=cake_color, outline=(0, 0, 0))
            
            # Buat lapisan kue
            draw.line([(int(size * 0.1), int(cake_top + (cake_bottom-cake_top)/3)), 
                        (int(size * 0.9), int(cake_top + (cake_bottom-cake_top)/3))], fill=(0, 0, 0), width=2)
            draw.line([(int(size * 0.1), int(cake_top + 2*(cake_bottom-cake_top)/3)), 
                        (int(size * 0.9), int(cake_top + 2*(cake_bottom-cake_top)/3))], fill=(0, 0, 0), width=2)
            
            # Buat lilin
            candle_width = int(size * 0.1)
            candle_height = int(size * 0.3)
            candle_x = int(size / 2 - candle_width / 2)
            candle_bottom = cake_top
            candle_top = candle_bottom - candle_height
            draw.rectangle([(candle_x, candle_top), (candle_x + candle_width, candle_bottom)], 
                            fill=candle_color, outline=(0, 0, 0))
            
            # Buat api
            flame_width = candle_width + 4
            flame_height = int(size * 0.15)
            flame_x = int(size / 2 - flame_width / 2)
            flame_top = candle_top - flame_height
            draw.polygon([(flame_x, candle_top), (flame_x + flame_width, candle_top), 
                           (int(size / 2), flame_top)], fill=flame_color, outline=(0, 0, 0))
            
            # Simpan sebagai PNG terlebih dahulu
            png_path = os.path.splitext(output_path)[0] + ".png"
            image.save(png_path, format="PNG")
            
            # Gunakan PIL untuk mengonversi PNG ke ICO
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            icons = []
            
            # Buat versi ukuran berbeda
            for icon_size in icon_sizes:
                icons.append(image.resize(icon_size, Image.LANCZOS))
            
            # Simpan sebagai ICO
            icons[0].save(output_path, format="ICO", sizes=[(i.width, i.height) for i in icons], 
                         append_images=icons[1:])
            
            return output_path
        except Exception as e:
            print(f"Error saat membuat ikon: {str(e)}")
            return None
    
    def reset_daily_notifications(self):
        """Reset notifikasi harian"""
        self.shown_notifications.clear() 