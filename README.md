# King-Astro
Repository ini dibuat untuk tugas besar matkul IF4021 (Teknologi Multimedia)  
Dosen Pengampu : Martin Clinton Tosima Manullang, Ph.D.  
  
Nama Tim : Pasukan King

Anggota Tim:
- Hagai Kopusi Sinulingga (122140059) Github : (https://github.com/Hagaikopusi)
- Muklis Mustaqim         (122140115) Github : (https://github.com/muklis-mustaqim-122140115)
- Akhwan Adib Al-Hakim    (122140149) Github : (https://github.com/AkhwanAdib-122140149)

 
Penjelasan Singkat: Proyek "King-Astro: Game Filter Pesawat Luar Angkasa" termasuk dalam kategori Aplikasi Komputer Visi Interaktif Real-Time. Proyek ini memanfaatkan teknologi deteksi wajah dan deteksi titik penanda wajah (facial landmark detection) yang diimplementasikan menggunakan pustaka MediaPipe. Secara umum, deteksi wajah digunakan untuk mengidentifikasi keberadaan pengguna di depan kamera secara terus-menerus, yang menjadi syarat utama agar game bisa dijalankan. Setelah wajah terdeteksi, sistem akan menggunakan posisi titik-titik penanda di wajah khususnya bagian hidung sebagai kontrol utama untuk menggerakkan pesawat. Selain itu, gerakan membuka mulut juga dideteksi dan digunakan untuk menjalankan fungsi menembak dalam game. Seluruh proses, mulai dari pengambilan gambar kamera, deteksi wajah, hingga penerjemahan gerakan wajah menjadi aksi dalam game, dilakukan secara real time. Hal ini menunjukkan kemampuan MediaPipe dalam membangun sistem pemrosesan visual yang cepat dan efisien. Konsep game ini mirip dengan aplikasi augmented reality (AR) atau filter wajah, di mana wajah pengguna dijadikan sebagai antarmuka (interface) utama untuk mengontrol elemen dalam permainan.

Referensi filter : https://vt.tiktok.com/ZSrvPcXbe/

## 📅 Logbook Mingguan

| Minggu | Tanggal         | Kegiatan                                | Progres                          |
|--------|------------------|------------------------------------------|----------------------------------|
| 1      |  24 April 2025    |  Pengajuan judul topik    |      100%       |
| 2      |  10 MEI 2025  |  Pendaftaran link Github dan pengumpulan Topik  |    100%   |
| 3      |  15 MEI 2025  | Mulai Merencanakan pembuatan code                 | 100% |
| 4      |  17 MEI 2025 | Mencari Asset untuk tampilan             |  100%   |
| 5      |  20 MEI 2025 | Mulai menerapkan code dan logika              |  100%   |
| 6      |  21 MEI 2025 | Membuat code             |  100%   |
| 7      |  24 MEI 2025 | Revisi ide dan konsep code program             |  100%   |
| 8      | 27 MEI 2025 | Melakukan Push code program di github            |  100%   |
| 9      |  27 MEI 2025 | Mulai Melakukan pengerjaan laporan              |  50%   |
| 10      |  28 MEI 2025 | Melengkapi github yang kurang             |  30%   |
| 11      |  29 MEI 2025 | Melengkapi Laporan             |  0%   |


## 📅 Instruksi instalasi dan penggunaan program
1. Menyediakan Visual Studio Code (VSCode) terlebih dahulu  
  Langkah pertama yang harus dilakukan adalah menyediakan dan menginstal Visual Studio Code (VSCode), yang merupakan code editor populer, ringan, dan mendukung berbagai bahasa pemrograman serta ekstensi pendukung.
VSCode akan berperan sebagai platform utama untuk menulis, menjalankan, dan mengelola keseluruhan kode program ini dan nantinya VSCode akan digunakan sebagai media utama untuk menjalankan program atau filter King-Astro.  
- Untuk menginstallnya secara gratis melalui situs resmi: https://code.visualstudio.com
- Setelah berhasil menginstall VSCode, maka VSCode sudah bisa dijalankan pada komputer anda  

2. Melakukan Download filter KING-Astro pada github
- Disini kita melakukan download foldernya terlebih dahulu sebelum bisa pada github pengembang yaitu (https://github.com/AkhwanAdib-122140149/King-Astro)  
- Pada tahap ini pastikan untuk membuka folder proyek KING-Astro melalui komputer anda yaitu pada menu File > Open Folder agar semua file program dan konfigurasi yang sudah di download sebelumnya dapat dikenali dengan baik.

3. Menyiapkan Virtual Environment (env)
  Sebelum menginstal dependensi , sangat disarankan untuk membuat virtual environment (env) terlebih dahulu. Virtual environment berfungsi untuk memisahkan pustaka-pustaka Python yang digunakan dalam proyek ini dari sistem Python utama, sehingga menghindari konflik versi dan menjaga lingkungan proyek tetap bersih dan terkontrol.
- Langkah-langkah membuat virtual environment:
python -m venv env (bash)  
- .\env\Scripts\activate (windows)
- source env/bin/activate (macOS/Linux)  

5. Menginstall Komponen Komponen mendukung  
  Program KING-Astro ini membutuhkan beberapa pustaka Python eksternal agar dapat berjalan dengan benar. Oleh karena itu, Anda perlu menginstal dependensi di dalam env yang sudah di install sebelumnya menggunakan pip, yang merupakan package manager untuk Python yang nantinya berguna untuk menjalankan program ini:  
- Lakukan penginstalan opencv-contrib-python==4.11.0.86 dengan menggunakan perintah (Pip install pip install opencv-contrib-python==4.11.0.86)  
- Menambahkan extension Jupyter pada VSCode dengan langsung menginstallnya pada bagian extension  
- Selanjutnya melakukan install numpy==1.26.4 dengan menggunakan perintah (pip install numpy==1.26.4)  
- Tahap berikutnya melakukan install mediapipe==0.10.21 dengan menggunakan perintah (pip install mediapipe==0.10.21)   
- Tahap terakhir melakukan install pygame==2.6.1 yang nantinya berguna untuk menjalankan filter sebagai game nya dengan perintah (pip install pygame==2.6.1)  

5. Menjalankan Program  
  Pada Tahap ini kita sudah berhasil menjalankan semua nya dan memasuki tahap terakhir dalam instruksi dan penggunaan program, dimana kita tinggal melakukan Run pada file atau program yang sudah di dwonload sebelumnya serta pastikan bahwa anda berada pada env yang sudah di install komponen komponen mendukung tadi, Maka program sudah bisa di jalankan dan selamat untuk bermain.

#Terimakasih



