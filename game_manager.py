import cv2
import numpy as np
import mediapipe as mp
import random
import time
from config import *
import pygame

class GameManager:
    """
    Kelas utama yang mengelola semua logika, status, dan alur permainan.

    Kelas ini bertanggung jawab untuk inisialisasi, menjalankan loop utama,
    memperbarui status semua objek game, menggambar di layar, dan menangani
    input dari pemain.
    """
    def __init__(self):
        """
        Menginisialisasi GameManager.

        Mempersiapkan webcam, model MediaPipe, memuat semua aset gambar,
        dan mengatur ulang status game ke kondisi awal.
        """
        self._init_camera_and_mediapipe()
        self._load_assets()
        # --- BARU: Inisialisasi Pygame Mixer dan putar musik ---
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
            pygame.mixer.music.set_volume(0.5) # Atur volume (0.0 hingga 1.0)
            pygame.mixer.music.play(-1) # Angka -1 berarti musik akan diulang terus-menerus
        except pygame.error as e:
            print(f"Error memuat atau memutar musik: {e}")
        # --- AKHIR BLOK BARU ---
        self.reset()

    def _init_camera_and_mediapipe(self):
        """Inisialisasi webcam dan model MediaPipe Face Mesh."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Tidak bisa membuka kamera.")
            exit()
        
        self.original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def _load_assets(self):
        """Memuat semua aset gambar yang dibutuhkan untuk game."""
        try:
            self.pesawat_img = self._load_single_asset(PESAWAT_PATH)
            self.rintangan_img = self._load_single_asset(RINTANGAN_PATH)
            self.energi_img = self._load_single_asset(ENERGI_PATH)
            self.musuh_img = self._load_single_asset(MUSUH_PATH)
        except (FileNotFoundError, TypeError) as e:
            print(f"Error: {e}"); exit()

    def _load_single_asset(self, path):
        """
        Memuat satu file gambar dan memvalidasinya.

        Args:
            path (str): Path menuju file gambar.

        Returns:
            np.ndarray: Gambar yang dimuat oleh OpenCV.

        Raises:
            FileNotFoundError: Jika file tidak ditemukan di path yang diberikan.
            TypeError: Jika gambar tidak memiliki alpha channel (bukan format transparan).
        """
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None: raise FileNotFoundError(f"File tidak ditemukan di path: {path}")
        if img.shape[2] != 4: raise TypeError(f"Gambar '{path}' harus memiliki alpha channel.")
        return img

    def reset(self):
        """Mereset semua status permainan ke kondisi awal untuk memulai game baru."""
        self.score = 0
        self.game_over = False
        self.victory = False
        self.start_time = time.time()
        
        self.peluru_pemain_list = []
        self.rintangan_list = []
        self.energi_list = []
        
        self.musuh_muncul = False
        self.musuh_obj = None
        self.musuh_target_pos = None
        self.musuh_boundaries = get_musuh_boundaries(self.original_width, self.original_height)

        self.is_in_sequence = False
        self.shots_fired_in_sequence = 0
        self.last_shot_time = 0
        self.last_sequence_time = 0
        
        self.boss_health = BOSS_MAX_HEALTH
        self.boss_is_invincible = False
        self.boss_hit_time = 0
        
        self.last_pemain_shot_time = 0
        
        self.last_rintangan_spawn = time.time()
        self.last_energi_spawn = time.time()

    def _update_player(self, results):
        """
        Memperbarui posisi pesawat pemain dan menangani input tembakan.

        Args:
            results: Objek hasil deteksi dari MediaPipe Face Mesh.
        """
        self.pesawat_pos = {'x': 0, 'y': 0, 'w': PESAWAT_W, 'h': PESAWAT_H}
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0].landmark
            hidung = face_landmarks[1]
            self.pesawat_pos['x'] = int(hidung.x * self.original_width) - (self.pesawat_pos['w'] // 2)
            self.pesawat_pos['y'] = int(hidung.y * self.original_height) - (self.pesawat_pos['h'] // 2)
            
            lip_atas, lip_bawah = face_landmarks[13], face_landmarks[14]
            lip_distance = abs(lip_atas.y - lip_bawah.y)
            if lip_distance > MOUTH_OPEN_THRESHOLD and time.time() - self.last_pemain_shot_time > PEMAIN_SHOOT_COOLDOWN:
                peluru_baru = {'x': self.pesawat_pos['x'] + self.pesawat_pos['w'], 'y': self.pesawat_pos['y'] + self.pesawat_pos['h'] // 2 - PEMAIN_PELURU_H // 2}
                self.peluru_pemain_list.append(peluru_baru)
                self.last_pemain_shot_time = time.time()

    def _update_player_projectiles(self):
        """Memperbarui posisi peluru pemain dan mendeteksi tabrakan dengan bos."""
        for p in self.peluru_pemain_list[:]:
            p['x'] += PEMAIN_PELURU_SPEED
            if p['x'] > self.original_width:
                self.peluru_pemain_list.remove(p)
                continue
            
            if self.musuh_muncul and self.boss_health > 0 and not self.boss_is_invincible:
                if (p['x'] < self.musuh_obj['x'] + self.musuh_obj['w'] and
                    p['x'] + PEMAIN_PELURU_W > self.musuh_obj['x'] and
                    p['y'] < self.musuh_obj['y'] + self.musuh_obj['h'] and
                    p['y'] + PEMAIN_PELURU_H > self.musuh_obj['y']):
                    
                    self.boss_health -= 1
                    self.boss_is_invincible = True
                    self.boss_hit_time = time.time()
                    self.peluru_pemain_list.remove(p)
                    
                    if self.boss_health <= 0:
                        self.victory, self.game_over = True, True
                        self.rintangan_list.clear()
                    break

    def _update_pre_boss_phase(self):
        """Menangani logika permainan sebelum bos muncul (spawn rintangan & energi)."""
        if time.time() - self.last_rintangan_spawn > random.uniform(1.5, 3):
            self._create_rintangan(); self.last_rintangan_spawn = time.time()
        if time.time() - self.last_energi_spawn > random.uniform(1, 2.5):
            self._create_energi(); self.last_energi_spawn = time.time()

        for e in self.energi_list[:]:
            e['x'] -= 4 
            if (self.pesawat_pos['x'] < e['x'] + e['w'] and self.pesawat_pos['x'] + self.pesawat_pos['w'] > e['x'] and
                self.pesawat_pos['y'] < e['y'] + e['h'] and self.pesawat_pos['y'] + self.pesawat_pos['h'] > e['y']):
                self.score += SCORE_PER_ENERGI; self.energi_list.remove(e)
            if e['x'] < -e['w']: self.energi_list.remove(e)

    def _update_boss_phase(self):
        """Menangani semua logika yang terkait dengan bos (gerakan, serangan, status)."""
        if self.musuh_target_pos:
            dx, dy = self.musuh_target_pos['x'] - self.musuh_obj['x'], self.musuh_target_pos['y'] - self.musuh_obj['y']
            distance = np.sqrt(dx**2 + dy**2)
            if distance < MUSUH_MOVE_SPEED: self.musuh_target_pos = self._get_new_musuh_target()
            else: self.musuh_obj['x'] += int(dx / distance * MUSUH_MOVE_SPEED); self.musuh_obj['y'] += int(dy / distance * MUSUH_MOVE_SPEED)
        
        self.musuh_obj['x'] = max(self.musuh_boundaries['min_x'], min(self.musuh_obj['x'], self.musuh_boundaries['max_x']))
        self.musuh_obj['y'] = max(self.musuh_boundaries['min_y'], min(self.musuh_obj['y'], self.musuh_boundaries['max_y']))

        if self.boss_is_invincible and time.time() - self.boss_hit_time > BOSS_INVINCIBILITY_DURATION:
            self.boss_is_invincible = False

        if self.boss_health > 0:
            if not self.is_in_sequence:
                if time.time() - self.last_sequence_time > SEQUENCE_COOLDOWN:
                    self.is_in_sequence, self.shots_fired_in_sequence, self.last_shot_time = True, 0, time.time() - SHOT_INTERVAL 
            else:
                if self.shots_fired_in_sequence < SHOTS_PER_SEQUENCE:
                    if time.time() - self.last_shot_time > SHOT_INTERVAL:
                        pos_y = random.randint(0, self.original_height - RINTANGAN_MUSUH_H)
                        self.rintangan_list.append({'x': self.musuh_obj['x'], 'y': pos_y, 'w': RINTANGAN_MUSUH_W, 'h': RINTANGAN_MUSUH_H, 'type': 'musuh_bullet'})
                        self.shots_fired_in_sequence, self.last_shot_time = self.shots_fired_in_sequence + 1, time.time()
                else: self.is_in_sequence, self.last_sequence_time = False, time.time()

    def _update_obstacles(self):
        """Memperbarui posisi rintangan dan mendeteksi tabrakan dengan pemain."""
        for r in self.rintangan_list[:]:
            r['x'] -= 7 if r.get('type') == 'musuh_bullet' else 5
            if (self.pesawat_pos['x'] < r['x'] + r['w'] and self.pesawat_pos['x'] + self.pesawat_pos['w'] > r['x'] and
                self.pesawat_pos['y'] < r['y'] + r['h'] and self.pesawat_pos['y'] + self.pesawat_pos['h'] > r['y']):
                if not self.victory: self.game_over = True 
            if r['x'] < -r['w']: self.rintangan_list.remove(r)
    
    def _draw_ui(self, frame):
        """
        Menggambar semua elemen User Interface (UI) ke layar.

        Args:
            frame (np.ndarray): Frame game tempat UI akan digambar.
        """
        elapsed_time = time.time() - self.start_time
        progress_to_boss = min(1.0, elapsed_time / GAME_DURATION_UNTIL_BOSS)
        bar_width_val = int(progress_to_boss * (self.original_width - 40))
        bar_color = COLOR_BOSS_BAR_BG if self.musuh_muncul else COLOR_BOSS_BAR_FG
        cv2.rectangle(frame, (20, 20), (20 + bar_width_val, 40), bar_color, -1)
        cv2.rectangle(frame, (20, 20), (self.original_width - 20, 40), COLOR_GREY, 2)
        text_bar = "LAWAN BOSS!" if self.musuh_muncul else "Menuju Boss"
        cv2.putText(frame, text_bar, (self.original_width // 2 - 70, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_BLACK, 2)

        cv2.putText(frame, f"SCORE: {self.score}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_YELLOW, 2)
        if self.musuh_muncul and not self.victory:
            cv2.putText(frame, "Buka Mulut untuk Menembak!", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLOR_WHITE, 2)

        if self.game_over:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, self.original_height // 2 - 100), (self.original_width, self.original_height // 2 + 100), COLOR_BLACK, -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            end_text, end_color = ("VICTORY!", COLOR_GREEN) if self.victory else ("GAME OVER", COLOR_RED)
            cv2.putText(frame, end_text, (self.original_width // 2 - 180, self.original_height // 2 - 50), cv2.FONT_HERSHEY_TRIPLEX, 2, end_color, 3)
            cv2.putText(frame, f"Final Score: {self.score}", (self.original_width // 2 - 150, self.original_height // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, COLOR_WHITE, 3)
            cv2.putText(frame, "Tekan 'R' untuk Mulai Lagi", (self.original_width // 2 - 220, self.original_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 2)

    def _draw_boss_health_bar(self, frame):
        """
        Menggambar bilah nyawa (health bar) milik bos.

        Args:
            frame (np.ndarray): Frame game tempat bilah nyawa akan digambar.
        """
        if self.musuh_muncul and self.boss_health > 0:
            bar_w, bar_h, bar_x, bar_y = MUSUH_W, 15, self.musuh_obj['x'], self.musuh_obj['y'] - 15 - 5
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), COLOR_RED, -1)
            current_health_w = int(bar_w * (self.boss_health / BOSS_MAX_HEALTH))
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + current_health_w, bar_y + bar_h), COLOR_GREEN, -1)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), COLOR_WHITE, 2)

    def run(self):
        """Loop utama permainan."""
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success: break
            
            frame = cv2.flip(frame, 1)
            results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if not self.game_over:
                self._update_player(results)
                self._update_player_projectiles()

                elapsed_time = time.time() - self.start_time
                if not self.musuh_muncul and elapsed_time > GAME_DURATION_UNTIL_BOSS:
                    self.musuh_muncul = True
                    self.musuh_obj = {'x': self.musuh_boundaries['max_x'], 'y': self.original_height // 2 - MUSUH_H // 2, 'w': MUSUH_W, 'h': MUSUH_H}
                    self.musuh_target_pos = self._get_new_musuh_target()
                    self.rintangan_list.clear(); self.energi_list.clear()

                if self.musuh_muncul: self._update_boss_phase()
                else: self._update_pre_boss_phase()
                
                self._update_obstacles()
            
            # --- Menggambar semua elemen ke frame ---
            for p in self.peluru_pemain_list:
                cv2.rectangle(frame, (p['x'], p['y']), (p['x'] + PEMAIN_PELURU_W, p['y'] + PEMAIN_PELURU_H), COLOR_BLUE, -1)
            for e in self.energi_list:
                self._overlay_image(frame, self.energi_img, e['x'], e['y'], e['w'], e['h'])
            for r in self.rintangan_list:
                self._overlay_image(frame, self.rintangan_img, r['x'], r['y'], r['w'], r['h'])
            
            self._overlay_image(frame, self.pesawat_img, self.pesawat_pos['x'], self.pesawat_pos['y'], self.pesawat_pos['w'], self.pesawat_pos['h'])
            
            if self.musuh_muncul and self.musuh_obj:
                draw_boss = not (self.boss_is_invincible and int(time.time() * 10) % 2 == 0)
                if draw_boss and self.boss_health > 0:
                    self._overlay_image(frame, self.musuh_img, self.musuh_obj['x'], self.musuh_obj['y'], self.musuh_obj['w'], self.musuh_obj['h'])
                self._draw_boss_health_bar(frame)
            
            self._draw_ui(frame)

            frame_tampilan = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Game Filter Pesawat", frame_tampilan)
            
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q'): break
            if self.game_over and key == ord('r'): self.reset()

        # --- BARU: Hentikan musik dan mixer saat game ditutup ---
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        # --- AKHIR BLOK BARU ---
        self.cap.release()
        cv2.destroyAllWindows()
        
    def _overlay_image(self, background, overlay, x, y, w, h):
        """Menempelkan gambar transparan (overlay) ke atas gambar latar (background)."""
        # (Implementasi detail tetap sama)
        if w <= 0 or h <= 0: return
        overlay_resized = cv2.resize(overlay, (w, h))
        if overlay_resized.shape[2] < 4: return
        alpha_channel = overlay_resized[:, :, 3] / 255.0
        y1, y2, x1, x2 = max(0, y), min(background.shape[0], y + h), max(0, x), min(background.shape[1], x + w)
        overlay_roi_h, overlay_roi_w = y2 - y1, x2 - x1
        if overlay_roi_h <= 0 or overlay_roi_w <= 0: return
        background_roi = background[y1:y2, x1:x2]
        overlay_rgb_roi = overlay_resized[0:overlay_roi_h, 0:overlay_roi_w, 0:3]
        alpha = alpha_channel[0:overlay_roi_h, 0:overlay_roi_w]
        for c in range(3):
            background_roi[:, :, c] = (1.0 - alpha) * background_roi[:, :, c] + alpha * overlay_rgb_roi[:, :, c]
    
    def _create_rintangan(self):
        """Membuat objek rintangan baru di luar layar sebelah kanan."""
        min_y, max_y = 75, self.original_height - 75 - RINTANGAN_H
        y_pos = random.randint(min_y, max_y) if min_y < max_y else self.original_height // 2
        self.rintangan_list.append({'x': self.original_width, 'y': y_pos, 'w': RINTANGAN_W, 'h': RINTANGAN_H, 'type': 'normal'})

    def _create_energi(self):
        """Membuat objek energi baru di luar layar sebelah kanan."""
        min_y, max_y = 75, self.original_height - 75 - ENERGI_H
        y_pos = random.randint(min_y, max_y) if min_y < max_y else self.original_height // 2
        self.energi_list.append({'x': self.original_width, 'y': y_pos, 'w': ENERGI_W, 'h': ENERGI_H})
        
    def _get_new_musuh_target(self):
        """Menghasilkan posisi target acak baru untuk pergerakan bos."""
        target_x = random.randint(self.musuh_boundaries['min_x'], self.musuh_boundaries['max_x'])
        target_y = random.randint(self.musuh_boundaries['min_y'], self.musuh_boundaries['max_y'])
        return {'x': target_x, 'y': target_y}