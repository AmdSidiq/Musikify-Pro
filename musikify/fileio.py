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