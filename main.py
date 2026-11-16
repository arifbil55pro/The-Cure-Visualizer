"""
main.py - Vibe Coding Lyrics Visualizer (Python + Pygame)
Lagu: Olivia Rodrigo - The Cure (Bridge & Outro)
Fitur: Langsung mulai, Kamera Dynamic Macro Zoom & Horizontal Tracking mengikuti kursor pengetikan.
"""

import sys
import time
import math
import pygame
import lyrics

# Inisialisasi Pygame
pygame.init()
pygame.font.init()

# Konfigurasi Window
WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("the_cure.py — Olivia Rodrigo (Vibe Coding)")
clock = pygame.time.Clock()

# Inisialisasi Font (Consolas untuk feel VS Code autentik)
def get_font(size, bold=False):
    try:
        font = pygame.font.SysFont("consolas", size, bold=bold)
        if font:
            return font
    except Exception:
        pass
    return pygame.font.SysFont("monospace", size, bold=bold)

FONT_CODE_LARGE = get_font(34)
FONT_LINE_NO_LARGE = get_font(28)
FONT_UI = get_font(15)
FONT_UI_BOLD = get_font(15, bold=True)
FONT_OVERLAY = get_font(28, bold=True)

# Warna Tema VS Code (Pitch Black OLED Theme)
COLOR_BG = (0, 0, 0)                 # Background editor hitam pekat (#000000)
COLOR_LINE_BG = (0, 0, 0)            # Background kolom nomor baris hitam pekat
COLOR_LINE_BORDER = (25, 25, 32)     # Garis batas nomor baris samar
COLOR_TITLE_BAR = (0, 0, 0)          # Titlebar atas hitam pekat
COLOR_TAB_ACTIVE = (0, 0, 0)         # Tab aktif hitam pekat
COLOR_TAB_INACTIVE = (0, 0, 0)       # Tab tidak aktif hitam pekat
COLOR_STATUS_BAR = (0, 0, 0)         # Status bar bawah hitam pekat
COLOR_ACTIVE_LINE = (18, 18, 24)     # Highlight baris aktif gelap samar
COLOR_TEXT_DIM = (75, 80, 100)       # Nomor baris tidak aktif
COLOR_TEXT_BRIGHT = (255, 255, 255)  # Teks terang / aktif
COLOR_CURSOR = (97, 175, 239)        # Kursor biru menyala

# Dimensi Virtual World Canvas yang luas agar kamera bebas tracking ke kanan
WORLD_W = 3400
WORLD_H = 2200
world_surface = pygame.Surface((WORLD_W, WORLD_H))

# Layout Margin di World Canvas
MARGIN_LEFT = 500                    # Ruang napas kiri agar kamera bisa fokus ke awal baris
LINE_COL_X = MARGIN_LEFT
LINE_COL_W = 90                      # Lebar kolom nomor baris
LINE_START_X = LINE_COL_X + LINE_COL_W + 35  # Titik awal teks lirik (X = 625)
LINE_HEIGHT = 72                     # Jarak antar baris teks
START_DRAW_Y = 160                   # Posisi Y baris pertama

# Pengaturan Waktu & Sinkronisasi
start_offset = lyrics.DEFAULT_START_TIME  # 03:21 (201s)
song_timer = start_offset
playback_start_realtime = time.perf_counter()
is_paused = False
pause_realtime = 0.0

# Posisi Awal Kamera (Langsung mengarah ke baris 1)
cam_x = float(LINE_START_X + 160)
cam_y = float(START_DRAW_Y + LINE_HEIGHT // 2)
cam_zoom = 1.65

target_cam_x = cam_x
target_cam_y = cam_y
target_zoom = 1.65

def format_time(seconds: float) -> str:
    """Format detik ke MM:SS.S"""
    if seconds < 0:
        seconds = 0
    m = int(seconds // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 10)
    return f"{m:02d}:{s:02d}.{ms}"

def draw_top_chrome(surface, width):
    """Menggambar Title Bar, Tab the_cure.py, dan Breadcrumbs"""
    # 1. Title Bar
    pygame.draw.rect(surface, COLOR_TITLE_BAR, (0, 0, width, 34))
    pygame.draw.circle(surface, (239, 89, 111), (18, 17), 6)   # Merah
    pygame.draw.circle(surface, (229, 192, 123), (36, 17), 6)  # Kuning
    pygame.draw.circle(surface, (152, 195, 121), (54, 17), 6)  # Hijau

    title_text = f"the_cure.py — {lyrics.SONG_TITLE} ({lyrics.ARTIST}) — Visual Studio Code"
    title_surf = FONT_UI.render(title_text, True, (150, 155, 175))
    surface.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 8))

    # 2. Tab Bar
    pygame.draw.rect(surface, COLOR_TAB_INACTIVE, (0, 34, width, 34))
    tab_w = 175
    pygame.draw.rect(surface, COLOR_TAB_ACTIVE, (0, 34, tab_w, 34))
    pygame.draw.line(surface, (0, 122, 204), (0, 34), (tab_w, 34), 2)  # Aksen biru tab aktif
    
    # Ikon Python mini
    pygame.draw.rect(surface, (75, 139, 190), (14, 44, 7, 7))
    pygame.draw.rect(surface, (255, 212, 59), (21, 51, 7, 7))
    
    tab_title = FONT_UI_BOLD.render("the_cure.py", True, COLOR_TEXT_BRIGHT)
    surface.blit(tab_title, (34, 42))
    
    close_surf = FONT_UI.render("×", True, (160, 160, 180))
    surface.blit(close_surf, (tab_w - 20, 41))

    # 3. Breadcrumbs
    pygame.draw.rect(surface, (0, 0, 0), (0, 68, width, 24))
    pygame.draw.line(surface, (25, 25, 32), (0, 91), (width, 91), 1)
    crumb_text = "The-Cure-Visualizer  ›  lyrics  ›  the_cure.py  ›  def bridge_outro():"
    crumb_surf = FONT_UI.render(crumb_text, True, (95, 100, 120))
    surface.blit(crumb_surf, (15, 71))

def draw_bottom_status_bar(surface, width, height, current_time, active_line_no, is_paused):
    """Menggambar Status Bar VS Code di bagian bawah (All Black)"""
    bar_y = height - 26
    pygame.draw.rect(surface, COLOR_STATUS_BAR, (0, bar_y, width, 26))
    pygame.draw.line(surface, (28, 28, 35), (0, bar_y), (width, bar_y), 1)
    
    git_text = FONT_UI.render("⎇ main*  |  0 errors  0 warnings", True, (160, 165, 185))
    surface.blit(git_text, (12, bar_y + 4))
    
    status_str = "PAUSED [SPACE to resume]" if is_paused else "SYNC PLAYING (Bridge)"
    time_display = f"⏱ {format_time(current_time)} / 04:22.0  |  Ln {active_line_no}, Col 28  |  Python 3.13  |  {status_str}"
    time_surf = FONT_UI.render(time_display, True, (160, 165, 185))
    surface.blit(time_surf, (width - time_surf.get_width() - 15, bar_y + 4))

def render_tokens_to_world(surface, tokens_list, char_limit, start_pos, font, is_active):
    """
    Merender syntax highlighting ke world canvas.
    Baris yang tidak aktif diredupkan (dimmed) agar mata penonton
    benar-benar fokus ke teks dan kursor yang sedang bergerak.
    """
    x, y = start_pos
    chars_printed = 0
    dim_factor = 1.0 if is_active else 0.40
    
    for text, color_type in tokens_list:
        if chars_printed >= char_limit:
            break
            
        remaining = char_limit - chars_printed
        visible_text = text[:remaining]
        base_color = lyrics.SYNTAX_COLORS.get(color_type, lyrics.SYNTAX_COLORS["default"])
        
        color = (
            int(base_color[0] * dim_factor),
            int(base_color[1] * dim_factor),
            int(base_color[2] * dim_factor)
        )
        
        t_surf = font.render(visible_text, True, color)
        surface.blit(t_surf, (x, y))
        x += t_surf.get_width()
        chars_printed += len(visible_text)
        
    return x

def render_world_canvas(current_time):
    """
    Merender seluruh halaman kode ke virtual world canvas
    dan mengembalikan koordinat aktif untuk camera zoom & horizontal cursor tracking.
    """
    world_surface.fill(COLOR_BG)
    
    # Kolom nomor baris
    pygame.draw.rect(world_surface, COLOR_LINE_BG, (0, 0, LINE_COL_X + LINE_COL_W, WORLD_H))
    pygame.draw.line(world_surface, COLOR_LINE_BORDER, (LINE_COL_X + LINE_COL_W, 0), (LINE_COL_X + LINE_COL_W, WORLD_H), 2)
    
    active_idx = -1
    active_line_no = 24
    cursor_x = None
    cursor_y = None
    active_center_y = None
    is_actively_singing = False
    active_progress = 0.0

    # 1. Tentukan baris mana yang aktif
    for i, item in enumerate(lyrics.LYRICS_DATA):
        if item["start"] <= current_time <= item["end"]:
            active_idx = i
            active_line_no = item["line_number"]
            is_actively_singing = True
            elapsed = current_time - item["start"]
            type_duration = item["duration"] * item["type_speed"]
            active_progress = min(1.0, max(0.0, elapsed / type_duration))
            break
        elif current_time > item["end"]:
            active_idx = i
            active_line_no = item["line_number"]
            is_actively_singing = False

    # 2. Gambar setiap baris kode
    for i, item in enumerate(lyrics.LYRICS_DATA):
        line_y = START_DRAW_Y + i * LINE_HEIGHT
        is_active = (i == active_idx) and is_actively_singing
        is_past = (current_time > item["end"]) or (i < active_idx)
        
        # Highlight Baris Aktif dengan glowing accent
        if is_active:
            active_center_y = line_y + LINE_HEIGHT // 2
            hl_rect = pygame.Rect(LINE_COL_X + LINE_COL_W + 1, line_y - 8, WORLD_W - (LINE_COL_X + LINE_COL_W), LINE_HEIGHT)
            pygame.draw.rect(world_surface, COLOR_ACTIVE_LINE, hl_rect)
            pygame.draw.line(world_surface, (97, 175, 239), (LINE_COL_X + LINE_COL_W + 1, line_y - 8), (LINE_COL_X + LINE_COL_W + 1, line_y + LINE_HEIGHT - 8), 5)

        # Nomor Baris
        if is_active:
            no_color = COLOR_TEXT_BRIGHT
        elif is_past:
            no_color = COLOR_TEXT_DIM
        else:
            no_color = (40, 42, 58)
            
        no_surf = FONT_LINE_NO_LARGE.render(str(item["line_number"]), True, no_color)
        no_x = LINE_COL_X + LINE_COL_W - no_surf.get_width() - 15
        world_surface.blit(no_surf, (no_x, line_y + 4))

        # Efek Typewriter
        full_code = item["code"]
        total_chars = len(full_code)
        
        if current_time < item["start"]:
            continue
        elif current_time >= item["end"]:
            visible_chars = total_chars
        else:
            elapsed = current_time - item["start"]
            type_duration = item["duration"] * item["type_speed"]
            progress = min(1.0, max(0.0, elapsed / type_duration))
            visible_chars = int(progress * total_chars)

        tokens = item.get("tokens") or lyrics.tokenize_code(full_code, i)
        last_x = render_tokens_to_world(world_surface, tokens, visible_chars, (LINE_START_X, line_y), FONT_CODE_LARGE, is_active)

        if is_active:
            cursor_x = last_x
            cursor_y = line_y

    # Kursor Berkedip (Blinking Cursor) pada ujung teks yang sedang diketik
    if cursor_x is not None and cursor_y is not None:
        blink = (int(time.time() * 3.5) % 2) == 0
        if blink:
            cursor_rect = pygame.Rect(cursor_x + 3, cursor_y + 2, 4, 36)
            pygame.draw.rect(world_surface, COLOR_CURSOR, cursor_rect)
            # Glowing halo kursor
            glow_surf = pygame.Surface((14, 42), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (97, 175, 239, 95), (0, 0, 14, 42), border_radius=4)
            world_surface.blit(glow_surf, (cursor_x - 2, cursor_y - 1))

    # Titik tengah fallback
    if active_center_y is None:
        if active_idx != -1:
            active_center_y = START_DRAW_Y + active_idx * LINE_HEIGHT + LINE_HEIGHT // 2
        else:
            active_center_y = START_DRAW_Y + LINE_HEIGHT // 2

    return active_line_no, cursor_x, active_center_y, is_actively_singing, active_progress

def main():
    global song_timer, playback_start_realtime, is_paused, pause_realtime
    global cam_x, cam_y, cam_zoom, target_cam_x, target_cam_y, target_zoom

    running = True
    last_frame_time = time.perf_counter()

    while running:
        current_frame_time = time.perf_counter()
        dt = current_frame_time - last_frame_time
        last_frame_time = current_frame_time
        
        cur_w, cur_h = screen.get_size()
        
        # --- Handle Input Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.VIDEORESIZE:
                screen_resized = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                    if is_paused:
                        pause_realtime = time.perf_counter()
                    else:
                        playback_start_realtime += (time.perf_counter() - pause_realtime)
                        
                elif event.key == pygame.K_r:
                    # Restart instan dari 03:21
                    song_timer = start_offset
                    playback_start_realtime = time.perf_counter()
                    is_paused = False
                    cam_x = float(LINE_START_X + 160)
                    cam_y = float(START_DRAW_Y + LINE_HEIGHT // 2)
                    cam_zoom = 1.65
                    target_cam_x = cam_x
                    target_cam_y = cam_y
                    target_zoom = 1.65
                    
                elif event.key == pygame.K_LEFT:
                    # Mundurkan sinkronisasi 1 detik
                    song_timer = max(start_offset, song_timer - 1.0)
                    playback_start_realtime += 1.0
                    
                elif event.key == pygame.K_RIGHT:
                    # Majukan sinkronisasi 1 detik
                    song_timer += 1.0
                    playback_start_realtime -= 1.0
                    
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

        # Update waktu lagu
        if not is_paused:
            song_timer = start_offset + (time.perf_counter() - playback_start_realtime)

        # 1. Render World Canvas & Dapatkan Posisi Kursor & Baris Aktif
        active_line_no, cur_cursor_x, active_y, is_singing, progress = render_world_canvas(song_timer)

        # 2. Logika Kamera: Zoom In & Horizontal Tracking Mengikuti Kursor
        viewport_y = 92
        viewport_h = cur_h - viewport_y - 26
        viewport_w = cur_w

        # Target Y: memusatkan baris yang sedang aktif secara vertikal
        target_cam_y = float(active_y)

        # Target X & Zoom:
        if is_singing and (cur_cursor_x is not None):
            # Sedang aktif bernyanyi & mengetik:
            # Kamera ZOOM IN erat (1.65x - 1.78x)
            swell = math.sin(progress * math.pi) * 0.12
            target_zoom = 1.66 + swell
            
            # TRACKING KE KANAN: Kamera memusatkan kursor pengetikan
            # Kami beri sedikit offset ke kiri (-100) agar kata yang baru saja diketik tetap terbaca
            # dan penonton melihat kursor bergerak maju mengetik ke arah kanan
            target_cam_x = float(cur_cursor_x - 70)
        else:
            # Jeda antar baris:
            # Kamera sedikit rileks (zoom out halus ke 1.35x)
            # dan meluncur kembali ke sisi kiri untuk menyambut baris baru
            target_zoom = 1.35
            target_cam_x = float(LINE_START_X + 160)

        # Smooth Camera Interpolation (Lerp dinamis)
        # Sumbu X menggunakan lerp yang responsif agar kursor selalu tertangkap kamera
        lerp_x = min(1.0, 7.5 * dt)
        lerp_y = min(1.0, 6.0 * dt)
        lerp_z = min(1.0, 5.0 * dt)

        cam_x += (target_cam_x - cam_x) * lerp_x
        cam_y += (target_cam_y - cam_y) * lerp_y
        cam_zoom += (target_zoom - cam_zoom) * lerp_z

        # 3. Potong & Skala Virtual Canvas ke Viewport
        crop_w = int(viewport_w / cam_zoom)
        crop_h = int(viewport_h / cam_zoom)

        # Hitung koordinat crop agar (cam_x, cam_y) berada di tengah viewport
        crop_x = int(cam_x - crop_w // 2)
        crop_y = int(cam_y - crop_h // 2)

        # Clamp batas aman dalam world_surface
        crop_x = max(0, min(crop_x, WORLD_W - crop_w))
        crop_y = max(0, min(crop_y, WORLD_H - crop_h))

        sub_area = pygame.Rect(crop_x, crop_y, crop_w, crop_h)
        sub_surface = world_surface.subsurface(sub_area)
        zoomed_viewport = pygame.transform.smoothscale(sub_surface, (viewport_w, viewport_h))

        # Bersihkan layar dengan hitam pekat
        screen.fill((0, 0, 0))

        # Blit hasil zoom ke viewport
        screen.blit(zoomed_viewport, (0, viewport_y))

        # 4. Render Chrome VS Code (Title Bar, Tabs, Breadcrumbs, Status Bar)
        draw_top_chrome(screen, cur_w)
        draw_bottom_status_bar(screen, cur_w, cur_h, song_timer, active_line_no, is_paused)

        # 5. Overlay jika sedang di-pause
        if is_paused:
            pause_overlay = pygame.Surface((cur_w, cur_h), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 110))
            screen.blit(pause_overlay, (0, 0))
            p_text = FONT_OVERLAY.render("⏸  PAUSED — PRESS SPACE TO RESUME", True, (255, 255, 255))
            screen.blit(p_text, (cur_w // 2 - p_text.get_width() // 2, cur_h // 2 - 15))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
