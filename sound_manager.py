"""
Modul untuk mengelola suara dalam aplikasi Birthday Timer.
"""
import os
import sys
import threading

# Cek platform dan import library yang sesuai
if sys.platform.startswith('win'):
    try:
        import winsound
        SOUND_SYSTEM = "winsound"
    except ImportError:
        SOUND_SYSTEM = None
else:
    try:
        import pygame
        pygame.mixer.init()
        SOUND_SYSTEM = "pygame"
    except ImportError:
        SOUND_SYSTEM = None

class SoundManager:
    """
    Kelas untuk mengelola suara dalam aplikasi.
    """
    def __init__(self, sound_enabled=True):
        """
        Inisialisasi SoundManager.

        Args:
            sound_enabled: Boolean yang menunjukkan apakah suara diaktifkan
        """
        self.sound_enabled = sound_enabled
        self.sound_cache = {}

        # Cek ketersediaan sistem suara
        self.sound_available = SOUND_SYSTEM is not None

        # Cek ketersediaan file suara
        self.sound_files = {
            "click": "sounds/click.wav",
            "click_soft": "sounds/click_soft.wav",
            "click_loud": "sounds/click_loud.wav"
        }

        # Verifikasi file suara
        for sound_name, sound_path in self.sound_files.items():
            if not os.path.exists(sound_path):
                print(f"Peringatan: File suara {sound_path} tidak ditemukan.")

    def play_sound(self, sound_name, async_play=True):
        """
        Memainkan suara berdasarkan nama.

        Args:
            sound_name: Nama suara yang akan dimainkan
            async_play: Apakah suara dimainkan secara asinkron

        Returns:
            Boolean yang menunjukkan apakah suara berhasil dimainkan
        """
        if not self.sound_enabled or not self.sound_available:
            return False

        sound_path = self.sound_files.get(sound_name)
        if not sound_path or not os.path.exists(sound_path):
            return False

        if async_play:
            threading.Thread(target=self._play_sound_sync, args=(sound_path,), daemon=True).start()
            return True
        else:
            return self._play_sound_sync(sound_path)

    def _play_sound_sync(self, sound_path):
        """
        Memainkan suara secara sinkron.

        Args:
            sound_path: Path ke file suara

        Returns:
            Boolean yang menunjukkan apakah suara berhasil dimainkan
        """
        try:
            print(f"Memainkan suara: {sound_path}")
            if SOUND_SYSTEM == "winsound":
                # Gunakan flag SND_ASYNC agar tidak memblokir UI
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return True
            elif SOUND_SYSTEM == "pygame":
                if sound_path not in self.sound_cache:
                    self.sound_cache[sound_path] = pygame.mixer.Sound(sound_path)
                self.sound_cache[sound_path].play()
                return True
            return False
        except Exception as e:
            print(f"Error memainkan suara: {str(e)}")
            return False

    def enable_sound(self, enabled=True):
        """
        Mengaktifkan atau menonaktifkan suara.

        Args:
            enabled: Boolean yang menunjukkan apakah suara diaktifkan
        """
        self.sound_enabled = enabled

    def is_sound_enabled(self):
        """
        Mengecek apakah suara diaktifkan.

        Returns:
            Boolean yang menunjukkan apakah suara diaktifkan
        """
        return self.sound_enabled and self.sound_available
