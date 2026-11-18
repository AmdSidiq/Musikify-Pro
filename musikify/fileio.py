NAMA_FILE_DATA = "data_musik.txt"
NAMA_FILE_LAPORAN = "laporan_musik.txt"
HEADER_FILE = "judul|artis|genre|durasi|tahun"

def inisialisasi_file(nama_file=NAMA_FILE_DATA):
    try:
        with open(nama_file, 'x', encoding='utf-8') as file:
            file.write(HEADER_FILE + "\n")
        print(f"[+] File '{nama_file}' berhasil dibuat!")
        return True
    except FileExistsError:
        return False

def tambah_lagu(nama_file, baris_data):
    with open(nama_file, 'a', encoding='utf-8') as file:
        file.write(baris_data.strip() + "\n")
    print(f"Lagu berhasil ditambahkan ke '{nama_file}'!")

def baca_semua_lagu(nama_file=NAMA_FILE_DATA):
    daftar_baris = []
    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            for baris in file:
                baris_bersih = baris.strip()
                if baris_bersih and not baris_bersih.startswith("judul"):
                    daftar_baris.append(baris_bersih)
    except FileNotFoundError:
        print(f"File '{nama_file}' belum ditemukan. Inisialisasi file baru.")
        inisialisasi_file(nama_file)
    return daftar_baris

def tulis_laporan(nama_file, konten):
    with open(nama_file, 'w', encoding='utf-8') as file:
        file.write(konten)
    print(f"Laporan berhasil ditulis ke '{nama_file}'!")

def simpan_semua_lagu(nama_file, daftar_baris):
    with open(nama_file, 'w', encoding='utf-8') as file:
        file.write(HEADER_FILE + "\n")
        for baris in daftar_baris:
            file.write(baris.strip() + "\n")
    print(f"Data berhasil disinkronkan ke '{nama_file}'!")