# Dokumentasi Modul Pixel UI

Modul ini menyediakan komponen UI kustom dengan gaya pixel art untuk aplikasi pengingat ulang tahun.

## Kelas PixelUI

Kelas utilitas untuk membuat elemen UI bergaya pixel.

### Metode Statis

#### `create_pixel_entry(parent, width=20, font_style="Courier New", font_size=12)`
- Membuat widget entry dengan gaya pixel
- **Parameters:**
  - parent: Widget parent
  - width: Lebar entry dalam karakter
  - font_style: Jenis font
  - font_size: Ukuran font
- **Returns:** Tuple (frame, entry)

#### `create_pixel_button(parent, text, command, bg_color="#B5EAD7", width=None)`
- Membuat tombol dengan gaya pixel
- **Parameters:**
  - parent: Widget parent
  - text: Teks tombol
  - command: Fungsi callback
  - bg_color: Warna latar tombol
  - width: Lebar tombol (opsional)
- **Returns:** Button widget

#### `create_pixel_frame(parent, bg_color="#FFD1DC", padding=10)`
- Membuat frame dengan border gaya pixel
- **Parameters:**
  - parent: Widget parent
  - bg_color: Warna latar frame
  - padding: Padding internal frame
- **Returns:** Frame widget

### Fitur Desain

1. **Gaya Pixel Art**
   - Border dengan efek pixel
   - Font monospace untuk kesan retro
   - Warna-warna pastel yang menyenangkan

2. **Responsivitas**
   - Widget menyesuaikan dengan ukuran parent
   - Padding dan margin yang konsisten

3. **Kustomisasi**
   - Warna dapat disesuaikan
   - Ukuran dan padding fleksibel

### Penggunaan

```python
# Membuat entry
frame, entry = PixelUI.create_pixel_entry(root)

# Membuat tombol
button = PixelUI.create_pixel_button(
    root,
    "Klik Saya",
    lambda: print("Diklik!")
)

# Membuat frame
frame = PixelUI.create_pixel_frame(root)
```

### Konstanta Warna

- `BG_COLOR = "#FFD1DC"` - Pink pastel untuk latar
- `ACCENT_COLOR = "#FFACB7"` - Pink tua untuk aksen
- `TEXT_COLOR = "#6B5876"` - Ungu tua untuk teks
- `BUTTON_COLOR = "#B5EAD7"` - Hijau mint untuk tombol

### Tips Penggunaan

1. **Konsistensi Visual**
   - Gunakan warna yang sudah didefinisikan
   - Pertahankan padding dan margin yang konsisten

2. **Performa**
   - Hindari terlalu banyak frame bersarang
   - Gunakan grid geometry manager untuk layout kompleks

3. **Aksesibilitas**
   - Sertakan teks alternatif untuk tombol
   - Pastikan kontras warna yang cukup