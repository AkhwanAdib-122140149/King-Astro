"""
File Konfigurasi Pusat untuk Game Filter Pesawat.

File ini berisi semua variabel global dan pengaturan yang digunakan di seluruh
proyek. Tujuannya adalah untuk memudahkan penyesuaian (tweaking) parameter game
seperti ukuran objek, kecepatan, durasi, path aset, dan warna tanpa harus
mengubah kode logika utama di 'game_manager.py'.
"""

# --- PENGATURAN TAMPILAN ---
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 720

# --- PENGATURAN GAME ---
GAME_DURATION_UNTIL_BOSS = 30
SCORE_PER_ENERGI = 10

# --- PATH ASET GAMBAR ---
# Pastikan semua gambar berada di dalam folder 'assets'
PESAWAT_PATH = 'assets/pesawat.png'
RINTANGAN_PATH = 'assets/rintangan.png'
ENERGI_PATH = 'assets/energi.png'
MUSUH_PATH = 'assets/musuh.png'
BACKGROUND_MUSIC_PATH = 'assets/undertale_megalovania.mp3'

# --- PENGATURAN UKURAN OBJEK ---
PESAWAT_W, PESAWAT_H = 78, 40
RINTANGAN_W, RINTANGAN_H = 60, 60
ENERGI_W, ENERGI_H = 30, 54
MUSUH_W, MUSUH_H = 150, 150
RINTANGAN_MUSUH_W, RINTANGAN_MUSUH_H = RINTANGAN_W // 2, RINTANGAN_H // 2
PEMAIN_PELURU_W, PEMAIN_PELURU_H = 25, 10

# --- PENGATURAN MEKANIK BOSS ---
BOSS_MAX_HEALTH = 3
BOSS_INVINCIBILITY_DURATION = 3.0
SEQUENCE_COOLDOWN = 1.5
SHOTS_PER_SEQUENCE = 10
SHOT_INTERVAL = 0.5
MUSUH_MOVE_SPEED = 3

# --- PENGATURAN MEKANIK PEMAIN ---
PEMAIN_SHOOT_COOLDOWN = 0.75
MOUTH_OPEN_THRESHOLD = 0.05
PEMAIN_PELURU_SPEED = 15

# --- PENGATURAN BATAS GERAKAN MUSUH (tergantung ukuran frame asli) ---
def get_musuh_boundaries(width, height):
    """Menghitung dan mengembalikan batas pergerakan untuk boss.
    
    Args:
        width (int): Lebar frame asli dari webcam.
        height (int): Tinggi frame asli dari webcam.

    Returns:
        dict: Dictionary berisi batas 'min_x', 'max_x', 'min_y', 'max_y'.
    """
    return {
        'min_x': int(width * 0.70),
        'max_x': width - MUSUH_W - 20,
        'min_y': 20,
        'max_y': height - MUSUH_H - 20
    }

# --- PENGATURAN WARNA (B, G, R) ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 100, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_GREY = (128, 128, 128)
COLOR_BOSS_BAR_BG = (200, 0, 0)
COLOR_BOSS_BAR_FG = (0, 180, 0)