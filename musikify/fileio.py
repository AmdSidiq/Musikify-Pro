# ============================================================
# fileio.py - Modul File Input/Output
# Menangani seluruh operasi file data dengan 4 mode:
# 'x' (create), 'a' (append), 'r' (read iteratif), 'w' (write/overwrite)
# ============================================================

NAMA_FILE_DATA = "data_musik.txt"
NAMA_FILE_LAPORAN = "laporan_musik.txt"
HEADER_FILE = "judul|artis|genre|durasi|tahun"

# Mode 'x' - Membuat file baru, tangani FileExistsError jika sudah ada
def inisialisasi_file(nama_file=NAMA_FILE_DATA):
    """
    Membuat file data baru pertama kali dengan mode 'x'.
    Jika file sudah ada, tangkap FileExistsError agar data tidak tertimpa.
    """
    try:
        with open(nama_file, 'x', encoding='utf-8') as file:
            file.write(HEADER_FILE + "\n")
        print(f"[+] File '{nama_file}' berhasil dibuat!")
        return True
    except FileExistsError:
        # File sudah ada, biarkan tetap ada tanpa menghapus data
        print(f"File '{nama_file}' sudah ada.")
        return False

# Mode 'a' - Menambah data record lagu baru di baris paling akhir file
def tambah_lagu(nama_file, baris_data):
    """
    Menyisipkan satu baris data lagu baru secara permanen di akhir file
    menggunakan mode 'a' (append).
    """
    with open(nama_file, 'a', encoding='utf-8') as file:
        file.write(baris_data.strip() + "\n")
    print(f"Lagu berhasil ditambahkan ke '{nama_file}'!")

# Mode 'r' - Membaca semua data secara iteratif baris per baris
def baca_semua_lagu(nama_file=NAMA_FILE_DATA):
    """
    Membaca seluruh baris data dari file menggunakan mode 'r'.
    Pembacaan dilakukan secara iteratif (for baris in file).
    Menangani FileNotFoundError jika file belum dibuat.
    """
    daftar_baris = []
    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            for baris in file: # Pembacaan iteratif baris per baris
                baris_bersih = baris.strip()
                # Lewati baris kosong dan baris header
                if baris_bersih and not baris_bersih.startswith("judul"):
                    daftar_baris.append(baris_bersih)
    except FileNotFoundError:
        print(f"File '{nama_file}' belum ditemukan. Inisialisasi file baru.")
        inisialisasi_file(nama_file)
    return daftar_baris

# Mode 'w' - Menulis laporan ke file eksternal (overwrite)
def tulis_laporan(nama_file, konten):
    """
    Menuliskan string ringkasan laporan ke file menggunakan mode 'w' (overwrite).
    """
    with open(nama_file, 'w', encoding='utf-8') as file:
        file.write(konten)
    print(f"Laporan berhasil ditulis ke '{nama_file}'!")

# Mode 'w' - Menyimpan ulang seluruh baris data (digunakan saat edit / hapus data)
def simpan_semua_lagu(nama_file, daftar_baris):
    """
    Menyimpan ulang seluruh koleksi lagu ke file tabular menggunakan mode 'w'.
    Digunakan saat ada aksi update atau hapus data melalui antarmuka UI.
    """
    with open(nama_file, 'w', encoding='utf-8') as file:
        file.write(HEADER_FILE + "\n")
        for baris in daftar_baris:
            file.write(baris.strip() + "\n")
    print(f"Data berhasil disinkronkan ke '{nama_file}'!")