import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

class PixelUI:
    """Kelas untuk membuat elemen UI bergaya pixel art"""
    
    @staticmethod
    def create_pixel_button(parent, text, command, width=120, height=40, 
                           bg_color="#B5EAD7", text_color="#6B5876", 
                           font_style="Courier New", font_size=12, bold=True):
        """
        Membuat tombol dengan tampilan pixel art
        
        Args:
            parent: Widget parent untuk tombol
            text: Teks yang ditampilkan pada tombol
            command: Fungsi yang dipanggil saat tombol diklik
            width: Lebar tombol (default 120)
            height: Tinggi tombol (default 40)
            bg_color: Warna latar tombol (default #B5EAD7)
            text_color: Warna teks tombol (default #6B5876)
            font_style: Gaya font (default Courier New)
            font_size: Ukuran font (default 12)
            bold: Apakah teks tebal atau tidak (default True)
            
        Returns:
            Frame yang berisi tombol bergaya pixel
        """
        # Buat frame luar untuk efek pixel
        frame = tk.Frame(
            parent,
            borderwidth=4,
            relief=tk.RAISED,
            bg="#000000",  # Border hitam untuk efek pixel
            width=width,
            height=height
        )
        
        # Buat tombol di dalam frame
        weight = "bold" if bold else "normal"
        button = tk.Button(
            frame,
            text=text,
            font=(font_style, font_size, weight),
            command=command,
            bg=bg_color,
            fg=text_color,
            relief=tk.FLAT,
            padx=5,
            pady=5,
            activebackground=bg_color,
            activeforeground=text_color
        )
        button.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        return frame
    
    @staticmethod
    def create_pixel_icon(size=32, color="#FFD1DC", border_color="#000000", outline_width=2):
        """
        Membuat ikon bergaya pixel
        
        Args:
            size: Ukuran ikon (default 32x32)
            color: Warna ikon (default #FFD1DC)
            border_color: Warna border (default #000000)
            outline_width: Ketebalan outline (default 2)
            
        Returns:
            PhotoImage yang berisi ikon bergaya pixel
        """
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Gambar kotak dengan outline untuk efek pixel
        draw.rectangle(
            [(outline_width, outline_width), (size-outline_width, size-outline_width)],
            fill=color,
            outline=border_color,
            width=outline_width
        )
        
        # Tambahkan efek pixel dengan gambar titik-titik di sudut
        for i in range(outline_width):
            for j in range(outline_width):
                draw.point((i, j), fill=border_color)
                draw.point((size-i-1, j), fill=border_color)
                draw.point((i, size-j-1), fill=border_color)
                draw.point((size-i-1, size-j-1), fill=border_color)
        
        photo_image = ImageTk.PhotoImage(image)
        return photo_image
    
    @staticmethod
    def create_birthday_cake_icon(size=32, cake_color="#FBE7C6", candle_color="#FF6B6B", flame_color="#FFCE5C", bg_color=None):
        """
        Membuat ikon kue ulang tahun bergaya pixel
        
        Args:
            size: Ukuran ikon (default 32x32)
            cake_color: Warna kue (default #FBE7C6)
            candle_color: Warna lilin (default #FF6B6B)
            flame_color: Warna api (default #FFCE5C)
            bg_color: Warna latar (default None - transparan)
            
        Returns:
            PhotoImage yang berisi ikon kue ulang tahun bergaya pixel
        """
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0) if bg_color is None else bg_color)
        draw = ImageDraw.Draw(image)
        
        # Buat kue (persegi panjang)
        cake_top = int(size * 0.6)
        cake_bottom = int(size * 0.9)
        draw.rectangle([(2, cake_top), (size-2, cake_bottom)], fill=cake_color, outline="#000000")
        
        # Tambahkan detail untuk kue (lapisan)
        draw.line([(2, int(cake_top + (cake_bottom-cake_top)/3)), (size-2, int(cake_top + (cake_bottom-cake_top)/3))], fill="#000000")
        draw.line([(2, int(cake_top + 2*(cake_bottom-cake_top)/3)), (size-2, int(cake_top + 2*(cake_bottom-cake_top)/3))], fill="#000000")
        
        # Buat lilin
        candle_width = int(size * 0.1)
        candle_height = int(size * 0.3)
        candle_x = int(size / 2 - candle_width / 2)
        candle_bottom = cake_top
        candle_top = candle_bottom - candle_height
        draw.rectangle([(candle_x, candle_top), (candle_x + candle_width, candle_bottom)], fill=candle_color, outline="#000000")
        
        # Buat api
        flame_width = candle_width + 2
        flame_height = int(size * 0.15)
        flame_x = int(size / 2 - flame_width / 2)
        flame_top = candle_top - flame_height
        draw.polygon(
            [(flame_x, candle_top), (flame_x + flame_width, candle_top), (flame_x + flame_width/2, flame_top)],
            fill=flame_color, outline="#000000"
        )
        
        photo_image = ImageTk.PhotoImage(image)
        return photo_image
    
    @staticmethod
    def create_pixel_entry(parent, width=20, font_style="Courier New", font_size=12, bg_color="#FFFFFF", text_color="#6B5876"):
        """
        Membuat entry field bergaya pixel
        
        Args:
            parent: Widget parent untuk entry
            width: Lebar entry dalam karakter (default 20)
            font_style: Gaya font (default Courier New)
            font_size: Ukuran font (default 12)
            bg_color: Warna latar entry (default #FFFFFF)
            text_color: Warna teks entry (default #6B5876)
            
        Returns:
            Entry bergaya pixel
        """
        # Buat frame untuk border entry
        frame = tk.Frame(
            parent,
            borderwidth=4,
            relief=tk.SUNKEN,
            bg="#000000"  # Border hitam untuk efek pixel
        )
        
        # Buat entry di dalam frame
        entry = tk.Entry(
            frame,
            width=width,
            font=(font_style, font_size),
            bg=bg_color,
            fg=text_color,
            relief=tk.FLAT,
            bd=0
        )
        entry.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        return frame, entry

    @staticmethod
    def create_pixel_title(text, size=24, color="#6B5876", outline_color="#000000", bg_color=None, pixel_size=2):
        """
        Membuat title text bergaya pixel art
        
        Args:
            text: Teks yang akan ditampilkan
            size: Ukuran font (default 24)
            color: Warna teks (default #6B5876)
            outline_color: Warna outline (default #000000)
            bg_color: Warna latar (default None - transparan)
            pixel_size: Ukuran pixel untuk efek (default 2)
            
        Returns:
            Label yang berisi text bergaya pixel
        """
        # Konversi nilai warna hex ke RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        color_rgb = hex_to_rgb(color)
        outline_rgb = hex_to_rgb(outline_color)
        
        # Ukuran huruf dan spasi
        char_width = size
        char_height = size
        spacing = int(size / 4)
        
        # Hitung ukuran gambar
        total_width = (char_width + spacing) * len(text) - spacing
        
        # Buat gambar baru
        if bg_color:
            image = Image.new("RGBA", (total_width, char_height), bg_color)
        else:
            image = Image.new("RGBA", (total_width, char_height), (0, 0, 0, 0))
        
        draw = ImageDraw.Draw(image)
        
        # Fungsi untuk menggambar karakter dengan efek pixel
        def draw_pixelated_char(x_offset, char):
            # Simplifikan dengan menggambar bentuk dasar saja
            if char == 'A':
                points = [(x_offset + char_width/2, 0), (x_offset, char_height), (x_offset + char_width, char_height)]
                draw.polygon(points, fill=color, outline=outline_color)
                # Garis tengah pada A
                draw.line([(x_offset + char_width/4, char_height/2), (x_offset + 3*char_width/4, char_height/2)], fill=outline_color, width=pixel_size)
            elif char == 'B':
                draw.rectangle([(x_offset, 0), (x_offset + 3*char_width/4, char_height)], fill=color, outline=outline_color)
                draw.ellipse([(x_offset + char_width/2, 0), (x_offset + char_width, char_height/2)], fill=color, outline=outline_color)
                draw.ellipse([(x_offset + char_width/2, char_height/2), (x_offset + char_width, char_height)], fill=color, outline=outline_color)
            else:
                # Untuk karakter lain, gambar persegi sederhana
                draw.rectangle([(x_offset, 0), (x_offset + char_width, char_height)], fill=color, outline=outline_color, width=pixel_size)
        
        # Gambar setiap karakter
        for i, char in enumerate(text):
            x = i * (char_width + spacing)
            draw_pixelated_char(x, char)
        
        # Tambahkan efek pixel dengan titik-titik
        for x in range(0, total_width, pixel_size):
            for y in range(0, char_height, pixel_size):
                current_color = image.getpixel((x, y))
                if current_color[:3] == color_rgb:
                    for dx in range(pixel_size):
                        for dy in range(pixel_size):
                            if 0 <= x+dx < total_width and 0 <= y+dy < char_height:
                                image.putpixel((x+dx, y+dy), current_color)
        
        return ImageTk.PhotoImage(image) 