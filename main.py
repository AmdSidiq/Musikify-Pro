# ============================================================
# main.py - File Eksekutabel Utama Aplikasi Musikify
# Mengimpor package 'musikify' dan menjalankan antarmuka
# grafis berbasis Tkinter (GUI).
# ============================================================

from musikify import (
    inisialisasi_file,
    jalankan_aplikasi_ui,
    NAMA_FILE_DATA
)

def main():
    inisialisasi_file(NAMA_FILE_DATA)
    jalankan_aplikasi_ui()

if __name__ == '__main__':
    main()


