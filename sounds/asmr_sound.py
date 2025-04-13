"""
Modul untuk menghasilkan file suara ASMR untuk aplikasi Birthday Timer.
"""
import wave
import struct
import os
import numpy as np
import random

def create_mechanical_keyboard_sound(filename="keyboard_click.wav", volume=0.7):
    """
    Membuat file suara keyboard mekanik yang ASMR.
    
    Args:
        filename: Nama file output
        volume: Volume suara (0.0 - 1.0)
    
    Returns:
        Path ke file suara yang dibuat
    """
    # Pastikan direktori sounds ada
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Parameter audio
    sample_rate = 44100  # Hz
    duration = 0.12  # Durasi suara dalam detik
    num_samples = int(duration * sample_rate)
    
    # Buat suara keyboard mekanik
    t = np.linspace(0, duration, num_samples, False)
    
    # Komponen suara keyboard mekanik
    # 1. Suara "click" awal (high frequency)
    f_click = random.uniform(2000, 3000)  # Frekuensi click
    
    # 2. Suara "thock" setelahnya (low frequency)
    f_thock = random.uniform(100, 300)  # Frekuensi thock
    
    # Envelope untuk click (cepat naik, cepat turun)
    click_attack = 0.001  # Waktu naik dalam detik
    click_decay = 0.03   # Waktu turun dalam detik
    click_env = np.zeros_like(t)
    click_env[t < click_attack] = t[t < click_attack] / click_attack
    click_env[(t >= click_attack) & (t < click_attack + click_decay)] = \
        1.0 - (t[(t >= click_attack) & (t < click_attack + click_decay)] - click_attack) / click_decay
    
    # Envelope untuk thock (sedikit delay, lebih lama)
    thock_delay = 0.01  # Delay sebelum thock dalam detik
    thock_attack = 0.01  # Waktu naik dalam detik
    thock_decay = 0.08   # Waktu turun dalam detik
    thock_env = np.zeros_like(t)
    thock_env[(t >= thock_delay) & (t < thock_delay + thock_attack)] = \
        (t[(t >= thock_delay) & (t < thock_delay + thock_attack)] - thock_delay) / thock_attack
    thock_env[(t >= thock_delay + thock_attack) & (t < thock_delay + thock_attack + thock_decay)] = \
        1.0 - (t[(t >= thock_delay + thock_attack) & (t < thock_delay + thock_attack + thock_decay)] - thock_delay - thock_attack) / thock_decay
    
    # Tambahkan sedikit noise untuk membuat suara lebih realistis
    noise = np.random.normal(0, 0.1, num_samples)
    noise_env = np.exp(-t * 20)  # Exponential decay untuk noise
    
    # Buat gelombang dengan harmonik
    click_wave = np.sin(2 * np.pi * f_click * t) * click_env * 0.7
    thock_wave = np.sin(2 * np.pi * f_thock * t) * thock_env * 0.9
    
    # Tambahkan harmonik untuk membuat suara lebih kaya
    click_wave += np.sin(2 * np.pi * f_click * 1.5 * t) * click_env * 0.2
    thock_wave += np.sin(2 * np.pi * f_thock * 2 * t) * thock_env * 0.3
    
    # Gabungkan semua komponen
    audio = click_wave + thock_wave + noise * noise_env * 0.2
    
    # Terapkan volume
    audio = audio * volume
    
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

def create_stone_tap_sound(filename="stone_tap.wav", volume=0.6):
    """
    Membuat file suara ketukan batu yang ASMR.
    
    Args:
        filename: Nama file output
        volume: Volume suara (0.0 - 1.0)
    
    Returns:
        Path ke file suara yang dibuat
    """
    # Pastikan direktori sounds ada
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Parameter audio
    sample_rate = 44100  # Hz
    duration = 0.15  # Durasi suara dalam detik
    num_samples = int(duration * sample_rate)
    
    # Buat suara ketukan batu
    t = np.linspace(0, duration, num_samples, False)
    
    # Komponen suara ketukan batu
    # 1. Suara "tap" awal (mid frequency)
    f_tap = random.uniform(500, 800)  # Frekuensi tap
    
    # 2. Suara resonansi setelahnya (low frequency)
    f_resonance = random.uniform(80, 150)  # Frekuensi resonansi
    
    # Envelope untuk tap (sangat cepat naik, cepat turun)
    tap_attack = 0.002  # Waktu naik dalam detik
    tap_decay = 0.04   # Waktu turun dalam detik
    tap_env = np.zeros_like(t)
    tap_env[t < tap_attack] = t[t < tap_attack] / tap_attack
    tap_env[(t >= tap_attack) & (t < tap_attack + tap_decay)] = \
        1.0 - (t[(t >= tap_attack) & (t < tap_attack + tap_decay)] - tap_attack) / tap_decay
    
    # Envelope untuk resonansi (sedikit delay, lebih lama)
    res_delay = 0.005  # Delay sebelum resonansi dalam detik
    res_attack = 0.02  # Waktu naik dalam detik
    res_decay = 0.12   # Waktu turun dalam detik
    res_env = np.zeros_like(t)
    res_env[(t >= res_delay) & (t < res_delay + res_attack)] = \
        (t[(t >= res_delay) & (t < res_delay + res_attack)] - res_delay) / res_attack
    res_env[(t >= res_delay + res_attack) & (t < res_delay + res_attack + res_decay)] = \
        1.0 - (t[(t >= res_delay + res_attack) & (t < res_delay + res_attack + res_decay)] - res_delay - res_attack) / res_decay
    
    # Tambahkan sedikit noise untuk membuat suara lebih realistis
    noise = np.random.normal(0, 0.05, num_samples)
    noise_env = np.exp(-t * 30)  # Exponential decay untuk noise
    
    # Buat gelombang dengan harmonik
    tap_wave = np.sin(2 * np.pi * f_tap * t) * tap_env * 0.8
    res_wave = np.sin(2 * np.pi * f_resonance * t) * res_env * 0.7
    
    # Tambahkan harmonik untuk membuat suara lebih kaya
    tap_wave += np.sin(2 * np.pi * f_tap * 1.7 * t) * tap_env * 0.15
    res_wave += np.sin(2 * np.pi * f_resonance * 2.3 * t) * res_env * 0.2
    
    # Gabungkan semua komponen
    audio = tap_wave + res_wave + noise * noise_env * 0.1
    
    # Terapkan volume
    audio = audio * volume
    
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

def create_all_asmr_sounds():
    """
    Membuat semua variasi suara ASMR.
    """
    # Buat suara keyboard mekanik
    create_mechanical_keyboard_sound("sounds/click.wav", volume=0.7)
    create_mechanical_keyboard_sound("sounds/click_soft.wav", volume=0.5)
    create_mechanical_keyboard_sound("sounds/click_loud.wav", volume=0.9)
    
    # Buat suara ketukan batu
    create_stone_tap_sound("sounds/stone_tap.wav", volume=0.6)
    create_stone_tap_sound("sounds/stone_tap_soft.wav", volume=0.4)
    create_stone_tap_sound("sounds/stone_tap_loud.wav", volume=0.8)
    
    print("File suara ASMR berhasil dibuat!")

if __name__ == "__main__":
    create_all_asmr_sounds()
