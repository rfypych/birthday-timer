"""
Modul untuk menghasilkan file suara klik untuk aplikasi Birthday Timer.
"""
import wave
import struct
import os
import numpy as np

def create_click_sound(filename="click.wav", duration=0.1, volume=0.5):
    """
    Membuat file suara klik yang menyenangkan.
    
    Args:
        filename: Nama file output
        duration: Durasi suara dalam detik
        volume: Volume suara (0.0 - 1.0)
    
    Returns:
        Path ke file suara yang dibuat
    """
    # Pastikan direktori sounds ada
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Parameter audio
    sample_rate = 44100  # Hz
    num_samples = int(duration * sample_rate)
    
    # Buat suara klik yang menyenangkan
    # Menggunakan kombinasi frekuensi untuk suara yang lebih menarik
    t = np.linspace(0, duration, num_samples, False)
    
    # Frekuensi dasar dan harmonik
    f1, f2, f3 = 1000, 1500, 2000
    
    # Amplitudo dengan envelope (naik cepat, turun perlahan)
    envelope = np.exp(-t * 20)  # Exponential decay
    attack = np.minimum(t * 100, 1)  # Quick attack
    
    # Kombinasikan envelope
    env = attack * envelope
    
    # Buat gelombang dengan harmonik
    wave1 = np.sin(2 * np.pi * f1 * t) * env * 0.6
    wave2 = np.sin(2 * np.pi * f2 * t) * env * 0.3
    wave3 = np.sin(2 * np.pi * f3 * t) * env * 0.1
    
    # Gabungkan gelombang
    audio = (wave1 + wave2 + wave3) * volume
    
    # Normalisasi untuk mencegah clipping
    audio = audio / np.max(np.abs(audio))
    
    # Konversi ke format yang dapat ditulis ke file WAV
    audio = (audio * 32767).astype(np.int16)
    
    # Tulis ke file WAV
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    return filename

if __name__ == "__main__":
    # Buat beberapa variasi suara klik
    create_click_sound("sounds/click.wav", duration=0.08, volume=0.5)
    create_click_sound("sounds/click_soft.wav", duration=0.05, volume=0.3)
    create_click_sound("sounds/click_loud.wav", duration=0.1, volume=0.7)
    print("File suara klik berhasil dibuat!")
