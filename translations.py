"""
Modul untuk menangani terjemahan multi-bahasa dalam aplikasi Birthday Timer.
"""

# Dictionary untuk terjemahan
TRANSLATIONS = {
    "id": {  # Bahasa Indonesia
        # Tab titles
        "tab_list": "Daftar",
        "tab_calendar": "Kalender",
        "tab_settings": "Pengaturan",
        "tab_testing": "Testing",
        "tab_docs": "Dokumentasi",

        # Main UI
        "app_title": "Birthday Timer",
        "counting_down": "Counting Down",
        "days": "hari",
        "hours": "jam",
        "minutes": "menit",
        "seconds": "detik",

        # List tab
        "birthday_list": "Daftar Ulang Tahun",
        "name": "Nama",
        "date": "Tanggal",
        "age": "Umur",
        "days_left": "Hari Lagi",
        "add": "+ Tambah",
        "edit": "Edit",
        "delete": "Hapus",
        "refresh": "Refresh",

        # Calendar tab
        "birthday_calendar": "Kalender Ulang Tahun",
        "birthday_info": "Informasi Ulang Tahun",
        "no_birthdays": "Tidak ada ulang tahun pada tanggal ini",

        # Settings tab
        "app_settings": "Pengaturan Aplikasi",
        "language_settings": "Pengaturan Bahasa",
        "language_desc": "Pilih bahasa yang digunakan dalam aplikasi",
        "language_id": "Bahasa Indonesia",
        "language_en": "English",
        "startup_settings": "Jalankan Pada Startup Windows",
        "startup_desc": "Aplikasi akan otomatis berjalan saat Windows dinyalakan",
        "enable": "Aktifkan",
        "sound_settings": "Pengaturan Suara",
        "sound_desc": "Aktifkan atau nonaktifkan efek suara dalam aplikasi",
        "enable_sound": "Aktifkan Suara",
        "sound_type": "Gaya Suara:",
        "sound_click1": "Gaya Klik 1",
        "sound_click2": "Gaya Klik 2",
        "sound_click3": "Gaya Klik 3",
        "test_sound": "Test Suara",
        "data_settings": "Backup & Restore Data",
        "data_desc": "Ekspor data ulang tahun untuk backup atau impor dari file backup",
        "export_data": "Ekspor Data",
        "import_data": "Impor Data",
        "about_app": "Tentang Aplikasi",
        "version": "Birthday Timer Versi 2.0",
        "creator": "Dibuat oleh: Rofikul",
        "copyright": "© 2023 All Rights Reserved",

        # Testing tab
        "testing_menu": "Menu Testing",
        "test_notification": "Test Notifikasi",
        "test_validation": "Test Validasi Input",
        "test_data_operations": "Test Operasi Data",
        "test_sound_system": "Test Sistem Suara",
        "testing_desc": "Fitur Testing memungkinkan Anda menguji:\n- Sistem notifikasi desktop\n- Validasi input data ulang tahun\n- Operasi data (tambah, ubah, hapus)\n- Sistem suara klik",

        # Documentation tab
        "app_docs": "Dokumentasi Aplikasi",
        "pixelui_docs": "PixelUI",
        "notification_docs": "Notifikasi",
        "app_usage_docs": "Aplikasi",

        # Dialog
        "add_birthday": "Tambah Ulang Tahun",
        "edit_birthday": "Edit Ulang Tahun",
        "save_new": "Simpan Data Baru",
        "save_changes": "Simpan Perubahan",
        "cancel": "Batal",
        "name_label": "Nama:",
        "date_label": "Tanggal Lahir:",
        "time_label": "Waktu Notifikasi:",
        "priority_label": "Prioritas:",

        # Messages
        "birthday_added": "✓ Ulang tahun {name} berhasil ditambahkan!",
        "birthday_edited": "✓ Ulang tahun {name} berhasil diubah!",
        "birthday_deleted": "✓ Ulang tahun {name} berhasil dihapus!",
        "birthdays_refreshed": "✓ Daftar ulang tahun berhasil diperbarui!",
        "sound_enabled": "✓ Efek suara diaktifkan!",
        "sound_disabled": "✓ Efek suara dinonaktifkan!",
        "sound_changed_click1": "✓ Gaya suara diubah ke Gaya Klik 1!",
        "sound_changed_click2": "✓ Gaya suara diubah ke Gaya Klik 2!",
        "sound_changed_click3": "✓ Gaya suara diubah ke Gaya Klik 3!",
        "language_changed": "✓ Bahasa berhasil diubah ke Bahasa Indonesia!",
        "startup_enabled": "✓ Autostart diaktifkan!",
        "startup_disabled": "✓ Autostart dinonaktifkan!",
        "test_sound_title": "Test Suara",
        "test_sound_message": "Klik OK untuk mendengarkan suara {sound_name}.",
        "test_sound_complete": "Test suara {sound_name} selesai. Apakah Anda menyukai suara ASMR ini?",
        "sound_disabled_info": "Suara sedang dinonaktifkan. Aktifkan suara terlebih dahulu.",
        "sound_not_supported": "Fitur suara hanya didukung di Windows.",
        "file_not_found": "Beberapa file suara tidak ditemukan:\n{files}",
        "error": "Error",
        "error_sound": "Gagal menjalankan test suara: {error}",
        "error_play_sound": "Gagal memainkan suara: {error}",
        "error_change_sound": "Gagal mengubah jenis suara: {error}",
        "error_change_language": "Gagal mengubah bahasa: {error}",
        "restart_required": "Aplikasi perlu di-restart untuk menerapkan perubahan bahasa. Restart sekarang?",
        "error_load_data": "Gagal memuat data: {error}",
        "error_save_data": "Gagal menyimpan data: {error}",
        "error_process_data": "Gagal memproses data baru: {error}",
        "error_data_file": "File birthdays.json rusak atau formatnya salah.",
        "error_app": "Terjadi kesalahan fatal: {error}",
        "confirm_delete": "Hapus Ulang Tahun",
        "confirm_delete_message": "Apakah Anda yakin ingin menghapus ulang tahun {name}?",
        "export_success": "✓ Data berhasil diekspor ke {filename}!",
        "import_success": "✓ Data berhasil diimpor dari {filename}!",
        "export_error": "Gagal mengekspor data: {error}",
        "import_error": "Gagal mengimpor data: {error}",
        "select_file": "Pilih File",
        "json_files": "File JSON",
        "all_files": "Semua File",
        "save_as": "Simpan Sebagai",
        "info": "Info",
        "warning": "Peringatan",
        "notification_title": "Pengingat Ulang Tahun",
        "notification_today": "Hari ini adalah ulang tahun {name}! Selamat ulang tahun!",
        "notification_days": "Ulang tahun {name} dalam {days} hari lagi!",
        "test_notification_title": "Test Notifikasi",
        "test_notification_message": "Ini adalah test notifikasi dari Birthday Timer.",
        "test_notification_success": "✓ Test notifikasi berhasil dijalankan!",
        "test_validation_success": "✓ Test validasi berhasil dijalankan!",
        "test_data_success": "✓ Test operasi data berhasil dijalankan!",
        "test_sound_success": "✓ Test suara ASMR berhasil dijalankan!"
    },
    "en": {  # English
        # Tab titles
        "tab_list": "List",
        "tab_calendar": "Calendar",
        "tab_settings": "Settings",
        "tab_testing": "Testing",
        "tab_docs": "Documentation",

        # Main UI
        "app_title": "Birthday Timer",
        "counting_down": "Counting Down",
        "days": "days",
        "hours": "hours",
        "minutes": "minutes",
        "seconds": "seconds",

        # List tab
        "birthday_list": "Birthday List",
        "name": "Name",
        "date": "Date",
        "age": "Age",
        "days_left": "Days Left",
        "add": "+ Add",
        "edit": "Edit",
        "delete": "Delete",
        "refresh": "Refresh",

        # Calendar tab
        "birthday_calendar": "Birthday Calendar",
        "birthday_info": "Birthday Information",
        "no_birthdays": "No birthdays on this date",

        # Settings tab
        "app_settings": "Application Settings",
        "language_settings": "Language Settings",
        "language_desc": "Choose the language used in the application",
        "language_id": "Bahasa Indonesia",
        "language_en": "English",
        "startup_settings": "Run on Windows Startup",
        "startup_desc": "Application will automatically run when Windows starts",
        "enable": "Enable",
        "sound_settings": "Sound Settings",
        "sound_desc": "Enable or disable sound effects in the application",
        "enable_sound": "Enable Sound",
        "sound_type": "Sound Style:",
        "sound_click1": "Click Style 1",
        "sound_click2": "Click Style 2",
        "sound_click3": "Click Style 3",
        "test_sound": "Test Sound",
        "data_settings": "Backup & Restore Data",
        "data_desc": "Export birthday data for backup or import from backup file",
        "export_data": "Export Data",
        "import_data": "Import Data",
        "about_app": "About Application",
        "version": "Birthday Timer Version 2.0",
        "creator": "Created by: Rofikul",
        "copyright": "© 2023 All Rights Reserved",

        # Testing tab
        "testing_menu": "Testing Menu",
        "test_notification": "Test Notification",
        "test_validation": "Test Input Validation",
        "test_data_operations": "Test Data Operations",
        "test_sound_system": "Test Sound System",
        "testing_desc": "Testing features allow you to test:\n- Desktop notification system\n- Birthday input validation\n- Data operations (add, edit, delete)\n- Click sound system",

        # Documentation tab
        "app_docs": "Application Documentation",
        "pixelui_docs": "PixelUI",
        "notification_docs": "Notification",
        "app_usage_docs": "Application",

        # Dialog
        "add_birthday": "Add Birthday",
        "edit_birthday": "Edit Birthday",
        "save_new": "Save New Data",
        "save_changes": "Save Changes",
        "cancel": "Cancel",
        "name_label": "Name:",
        "date_label": "Birth Date:",
        "time_label": "Notification Time:",
        "priority_label": "Priority:",

        # Messages
        "birthday_added": "✓ {name}'s birthday has been added successfully!",
        "birthday_edited": "✓ {name}'s birthday has been edited successfully!",
        "birthday_deleted": "✓ {name}'s birthday has been deleted successfully!",
        "birthdays_refreshed": "✓ Birthday list has been refreshed successfully!",
        "sound_enabled": "✓ Sound effects enabled!",
        "sound_disabled": "✓ Sound effects disabled!",
        "sound_changed_click1": "✓ Sound style changed to Click Style 1!",
        "sound_changed_click2": "✓ Sound style changed to Click Style 2!",
        "sound_changed_click3": "✓ Sound style changed to Click Style 3!",
        "language_changed": "✓ Language changed to English successfully!",
        "startup_enabled": "✓ Autostart enabled!",
        "startup_disabled": "✓ Autostart disabled!",
        "test_sound_title": "Sound Test",
        "test_sound_message": "Click OK to listen to {sound_name} sound.",
        "test_sound_complete": "Sound test for {sound_name} completed. Did you like this ASMR sound?",
        "sound_disabled_info": "Sound is currently disabled. Please enable sound first.",
        "sound_not_supported": "Sound feature is only supported on Windows.",
        "file_not_found": "Some sound files were not found:\n{files}",
        "error": "Error",
        "error_sound": "Failed to run sound test: {error}",
        "error_play_sound": "Failed to play sound: {error}",
        "error_change_sound": "Failed to change sound type: {error}",
        "error_change_language": "Failed to change language: {error}",
        "restart_required": "The application needs to be restarted to apply language changes. Restart now?",
        "error_load_data": "Failed to load data: {error}",
        "error_save_data": "Failed to save data: {error}",
        "error_process_data": "Failed to process new data: {error}",
        "error_data_file": "The birthdays.json file is corrupted or has an invalid format.",
        "error_app": "A fatal error occurred: {error}",
        "confirm_delete": "Delete Birthday",
        "confirm_delete_message": "Are you sure you want to delete {name}'s birthday?",
        "export_success": "✓ Data exported successfully to {filename}!",
        "import_success": "✓ Data imported successfully from {filename}!",
        "export_error": "Failed to export data: {error}",
        "import_error": "Failed to import data: {error}",
        "select_file": "Select File",
        "json_files": "JSON Files",
        "all_files": "All Files",
        "save_as": "Save As",
        "info": "Info",
        "warning": "Warning",
        "notification_title": "Birthday Reminder",
        "notification_today": "Today is {name}'s birthday! Happy birthday!",
        "notification_days": "{name}'s birthday is in {days} days!",
        "test_notification_title": "Test Notification",
        "test_notification_message": "This is a test notification from Birthday Timer.",
        "test_notification_success": "✓ Notification test run successfully!",
        "test_validation_success": "✓ Validation test run successfully!",
        "test_data_success": "✓ Data operations test run successfully!",
        "test_sound_success": "✓ ASMR sound test run successfully!"
    }
}

class Translator:
    """Kelas untuk menangani terjemahan teks."""

    def __init__(self, language="id"):
        """
        Inisialisasi translator.

        Args:
            language: Kode bahasa ("id" untuk Indonesia, "en" untuk English)
        """
        self.language = language
        self.translations = TRANSLATIONS

    def set_language(self, language):
        """
        Mengubah bahasa yang digunakan.

        Args:
            language: Kode bahasa ("id" untuk Indonesia, "en" untuk English)

        Returns:
            Boolean yang menunjukkan apakah bahasa berhasil diubah
        """
        if language in self.translations:
            self.language = language
            return True
        return False

    def get_text(self, key, **kwargs):
        """
        Mendapatkan teks terjemahan berdasarkan kunci.

        Args:
            key: Kunci terjemahan
            **kwargs: Parameter untuk format string

        Returns:
            Teks terjemahan
        """
        if self.language in self.translations and key in self.translations[self.language]:
            text = self.translations[self.language][key]
            if kwargs:
                try:
                    return text.format(**kwargs)
                except KeyError:
                    return text
            return text
        return key  # Kembalikan kunci jika terjemahan tidak ditemukan

# Inisialisasi translator global
translator = Translator()

# Fungsi helper untuk mendapatkan terjemahan
def get_text(key, **kwargs):
    """
    Mendapatkan teks terjemahan berdasarkan kunci.

    Args:
        key: Kunci terjemahan
        **kwargs: Parameter untuk format string

    Returns:
        Teks terjemahan
    """
    return translator.get_text(key, **kwargs)

# Alias untuk get_text
_ = get_text
