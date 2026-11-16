# The Cure — Vibe Coding Visualizer 🎵💻

Animasi visualizer lirik lagu **"The Cure" — Olivia Rodrigo** (Bagian Bridge & Outro) berbasis **Python + Pygame** dengan estetika **Vibe Coding / VS Code Dark Theme**.

## ✨ Fitur Utama
- **Estetika VS Code Pitch Black (OLED `#000000`)**: Tampilan code editor modern dengan kontras tinggi.
- **Kamera Dynamic Zoom & Macro Tracking**: Kamera otomatis melakukan *zoom-in* sinematik dan meluncur ke kanan mengikuti jalannya kursor pengetikan lirik secara *real-time*.
- **Syntax Highlighting Kustom**:
  - 🔴 **Merah Darah**: Kata `why`, `you` / `"you_come"`, `"my_bloodstream"`, dan baris `// Ah - ah - ah - ah...`
  - 🟢 **Hijau Tua**: Kata `"poison"`
  - 🟠 **Orange**: Tanda kurung `()` dan kurawal `{}` sebelum *ah-ah-ah*, serta teks lirik sesudah *ah-ah-ah*
  - ⚪ **Putih**: Teks lirik sebelum *ah-ah-ah*
  - 🔴 **Merah**: Tanda kurung `()` dan kurawal `{}` sesudah *ah-ah-ah*
  - 🟡 **Kuning**: Properties / Keys (`stitch:`, `is_full_of:`, dll.)
  - 🔵 **Biru**: Functions / Methods (`cant`, `tried_so_hard`, dll.)
  - 🟣 **Ungu**: Keywords (`and`, `but`, `oh`, dll.)
- **Blinking Cursor & Highlight Bar**: Efek baris aktif dengan glow biru neon dan kursor berkedip.
- **Sinkronisasi Waktu Lagu Asli**: Waktu otomatis dihitung mulai dari menit `03:21` (Bridge).

## 🚀 Persyaratan
- Python 3.8+
- Pygame (`pip install pygame`)

## 🎮 Cara Menjalankan
```bash
python main.py
```

### ⌨️ Kontrol Keyboard
| Tombol | Fungsi |
| :--- | :--- |
| `SPACE` | Pause / Resume lirik |
| `R` | Restart langsung dari awal bridge (`03:21`) |
| `←` / `→` | Majukan / mundurkan sinkronisasi (±1 detik) jika audio di HP sedikit mendahului atau terlambat |
| `F11` | Mode Fullscreen |
| `ESC` | Keluar aplikasi |
