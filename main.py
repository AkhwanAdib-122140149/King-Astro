"""
Titik Masuk Utama (Main Entry Point) untuk Game Filter Pesawat.

File ini bertanggung jawab untuk membuat instance dari kelas GameManager
dan menjalankan loop utama permainan. Untuk menjalankan game, eksekusi file ini
dari terminal: `python main.py`
"""

from game_manager import GameManager

if __name__ == "__main__":
    # Membuat instance dari kelas utama game
    game = GameManager()
    
    # Memulai dan menjalankan loop utama game
    game.run()