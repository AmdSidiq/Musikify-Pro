class Lagu:
    """
    Class untuk merepresentasikan sebuah entitas lagu.
    Menyimpan atribut judul, artis, genre, durasi (detik), dan tahun rilis.
    """

    def __init__(self, judul, artis, genre, durasi, tahun):
        self.judul = str(judul).strip()
        self.artis = str(artis).strip()
        self.genre = str(genre).strip()
        self.durasi = int(durasi)  
        self.tahun = int(tahun)

    def durasi_formatted(self):
        menit = self.durasi // 60
        detik = self.durasi % 60
        return f"{menit:02d}:{detik:02d}"

    def info_lengkap(self):
        return f"{self.judul} - {self.artis} [{self.genre}] ({self.durasi_formatted()}) ({self.tahun})"

    def to_line(self):
        return f"{self.judul}|{self.artis}|{self.genre}|{self.durasi}|{self.tahun}"

    def to_dict(self):
        return {
            "judul": self.judul,
            "artis": self.artis,
            "genre": self.genre,
            "durasi": self.durasi,
            "durasi_str": self.durasi_formatted(),
            "tahun": self.tahun
        }

    @classmethod
    def from_line(cls, baris):
        data = validasi_baris_data(baris)
        if data:
            return cls(
                judul=data["judul"],
                artis=data["artis"],
                genre=data["genre"],
                durasi=data["durasi"],
                tahun=data["tahun"]
            )
        return None

    def __repr__(self):
        return f"<Lagu: {self.judul} oleh {self.artis}>"

# ============================================================
# ALGORITMA PENGURUTAN (SORTING)
# ============================================================

def merge_sort(daftar, key_func=lambda x: x, reverse=False):
    """
    Algoritma Merge Sort (Divide and Conquer - Rekursif).
    - Memecah daftar menjadi 2 sub-daftar, mengurutkan secara rekursif, lalu menggabungkannya.
    """
    if len(daftar) <= 1:
        return list(daftar)

    tengah = len(daftar) // 2
    kiri = merge_sort(daftar[:tengah], key_func, reverse)
    kanan = merge_sort(daftar[tengah:], key_func, reverse)

    # Proses penggabungan (merge) dua sub-list terurut
    hasil = []
    i = j = 0

    while i < len(kiri) and j < len(kanan):
        kiri_val = key_func(kiri[i])
        kanan_val = key_func(kanan[j])

        # Kondisi perbandingan berdasarkan parameter reverse
        if (kiri_val <= kanan_val) if not reverse else (kiri_val >= kanan_val):
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1

    # Gabungkan sisa elemen yang belum terambil
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def selection_sort(daftar, key_func=lambda x: x, reverse=False):
    """
    Algoritma Selection Sort (Sesuai Materi Modul 10).
    - Mencari elemen minimum/maksimum dari bagian belum terurut, lalu menukarnya ke depan.
    """
    data = list(daftar)
    n = len(data)

    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            val_j = key_func(data[j])
            val_target = key_func(data[target_idx])

            if (val_j < val_target) if not reverse else (val_j > val_target):
                target_idx = j

        # Tukar elemen terkecil/terbesar ke posisi i
        if target_idx != i:
            data[i], data[target_idx] = data[target_idx], data[i]

    return data

# ============================================================
# ALGORITMA PENCARIAN (SEARCHING)
# ============================================================

def linear_search(daftar_lagu, keyword, field="semua"):
    """
    Algoritma Linear Search (Pencarian Linier berurutan satu per satu).
    - Memeriksa setiap elemen lagu secara sekuensial.
    - Mendukung filter field: 'semua', 'judul', 'artis', atau 'genre'.
    """
    kw = str(keyword).lower().strip()
    if not kw:
        return list(daftar_lagu)

    hasil = []
    for lagu in daftar_lagu:
        cocok = False
        if field == "judul":
            cocok = kw in lagu.judul.lower()
        elif field == "artis":
            cocok = kw in lagu.artis.lower()
        elif field == "genre":
            cocok = kw in lagu.genre.lower()
        else:  # Field 'semua'
            cocok = (kw in lagu.judul.lower() or
                     kw in lagu.artis.lower() or
                     kw in lagu.genre.lower())

        if cocok:
            hasil.append(lagu)

    return hasil


def binary_search_judul(daftar_lagu, target_judul):
    """
    Algoritma Binary Search (Pencarian Biner Bagi-Dua).
    - Bekerja pada daftar lagu yang telah terurut berdasarkan judul.
    - Membagi interval pencarian menjadi dua bagian secara berulang.
    - Mengembalikan objek Lagu yang cocok atau None jika tidak ditemukan.
    """
    if not daftar_lagu:
        return None

    # Pastikan data terurut berdasarkan judul secara alfabetis
    lagu_terurut = merge_sort(daftar_lagu, key_func=lambda l: l.judul.lower())
    target = str(target_judul).lower().strip()

    low = 0
    high = len(lagu_terurut) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = lagu_terurut[mid].judul.lower()

        if mid_val == target:
            return lagu_terurut[mid]  # Ditemukan tepat
        elif target in mid_val:
            # Jika target merupakan substring judul tengah
            return lagu_terurut[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None

class KoleksiMusik:
    """
    Class utama untuk mengelola koleksi lagu, agregasi data,
    serta antarmuka sorting dan searching.
    """

    def __init__(self):
        self.daftar_lagu = []

    # ========================================================
    # PENERAPAN *args - Variadic Positional Arguments
    # ========================================================
    def tambah_banyak_lagu(self, *lagu):
        """
        Menambahkan banyak objek Lagu sekaligus ke dalam koleksi menggunakan *args.
        Mengembalikan jumlah lagu yang berhasil ditambahkan.
        """
        jumlah = 0
        for item in lagu:
            if isinstance(item, Lagu):
                self.daftar_lagu.append(item)
                jumlah += 1
        return jumlah

    def hitung_total_durasi(self, *durasi_tambahan):
        """
        Menghitung akumulasi durasi seluruh lagu dalam koleksi,
        ditambah durasi ekstra opsional melalui *args.
        """
        total = sum(l.durasi for l in self.daftar_lagu)
        for ekstra in durasi_tambahan:
            if isinstance(ekstra, (int, float)):
                total += int(ekstra)
        return total

    # ========================================================
    # PENERAPAN **kwargs - Variadic Keyword Arguments
    # ========================================================
    def buat_record_lagu(self, **kwargs):
        """
        Membuat record Lagu baru dengan properti input variatif menggunakan **kwargs.
        Menyediakan nilai default aman jika atribut tertentu tidak dikirim.
        """
        lagu_baru = Lagu(
            judul=kwargs.get("judul", "Unknown Title"),
            artis=kwargs.get("artis", "Unknown Artist"),
            genre=kwargs.get("genre", "Pop"),
            durasi=kwargs.get("durasi", 180),
            tahun=kwargs.get("tahun", 2024)
        )
        self.daftar_lagu.append(lagu_baru)
        return lagu_baru

    def filter_lagu(self, **kwargs):
        """
        Menyaring koleksi lagu berdasarkan berbagai kriteria fleksibel menggunakan **kwargs.
        Contoh: filter_lagu(genre="Rock", tahun_min=2000, durasi_max=300)
        """
        hasil = list(self.daftar_lagu)

        if "genre" in kwargs and kwargs["genre"]:
            g = kwargs["genre"].lower()
            hasil = [l for l in hasil if l.genre.lower() == g]

        if "tahun_min" in kwargs and kwargs["tahun_min"] is not None:
            hasil = [l for l in hasil if l.tahun >= kwargs["tahun_min"]]

        if "tahun_max" in kwargs and kwargs["tahun_max"] is not None:
            hasil = [l for l in hasil if l.tahun <= kwargs["tahun_max"]]

        if "durasi_max" in kwargs and kwargs["durasi_max"] is not None:
            hasil = [l for l in hasil if l.durasi <= kwargs["durasi_max"]]

        return hasil

    # ========================================================
    # METODE ANALISIS & STATISTIK
    # ========================================================
    def rata_rata_durasi(self):
        """Menghitung rata-rata durasi lagu dalam detik (aman dari ZeroDivisionError)."""
        if not self.daftar_lagu:
            return 0.0
        return sum(l.durasi for l in self.daftar_lagu) / len(self.daftar_lagu)

    def lagu_per_genre(self):
        """Menghitung frekuensi kemunculan lagu untuk setiap genre musik."""
        genre_count = {}
        for lagu in self.daftar_lagu:
            genre_count[lagu.genre] = genre_count.get(lagu.genre, 0) + 1
        return genre_count

    def genre_terpopuler(self):
        """
        Mencari genre yang memiliki lagu terbanyak menggunakan lambda.
        Mengembalikan tuple (nama_genre, jumlah).
        """
        distribusi = self.lagu_per_genre()
        if not distribusi:
            return ("-", 0)
        # Penggunaan lambda untuk menentukan nilai maksimum berdasarkan value dict
        return max(distribusi.items(), key=lambda item: item[1])

    # ========================================================
    # PENCARIAN & PENGURUTAN (SORTING & SEARCHING)
    # ========================================================
    def cari_lagu(self, keyword, field="semua"):
        """Pencarian linier fleksibel pada koleksi lagu."""
        return linear_search(self.daftar_lagu, keyword, field=field)

    def cari_biner_judul(self, target_judul):
        """Pencarian biner cepat berdasarkan judul lagu."""
        return binary_search_judul(self.daftar_lagu, target_judul)

    def urutkan_lagu(self, berdasarkan="judul", reverse=False, algoritma="merge_sort"):
        """
        Mengurutkan daftar lagu menggunakan lambda sebagai key pembanding.
        Mendukung pemilihan algoritma: 'merge_sort' (default/optimasi),
        'selection_sort', atau 'python_sort' (Timsort bawaan).
        """
        key_map = {
            "judul": lambda l: l.judul.lower(),
            "artis": lambda l: l.artis.lower(),
            "genre": lambda l: l.genre.lower(),
            "durasi": lambda l: l.durasi,
            "tahun": lambda l: l.tahun
        }
        key_func = key_map.get(berdasarkan.lower(), key_map["judul"])

        if algoritma == "selection_sort":
            return selection_sort(self.daftar_lagu, key_func=key_func, reverse=reverse)
        elif algoritma == "python_sort":
            return sorted(self.daftar_lagu, key=key_func, reverse=reverse)
        else:
            # Default ke Merge Sort (O(n log n) - Optimasi Algoritma Khusus)
            return merge_sort(self.daftar_lagu, key_func=key_func, reverse=reverse)

    def filter_by_genre(self, genre):
        """
        Menyaring lagu bergenre tertentu menggunakan filter() bawaan dan lambda.
        """
        return list(filter(lambda l: l.genre.lower() == genre.lower(), self.daftar_lagu))

    # ========================================================
    # OPERASI KELOLA DATA (CRUD) & PERSISTENSI
    # ========================================================
    def tambah_lagu(self, lagu):
        """Menambahkan satu objek Lagu ke dalam koleksi."""
        if isinstance(lagu, Lagu):
            self.daftar_lagu.append(lagu)
            return True
        return False

    def hapus_lagu_by_index(self, index):
        """Menghapus lagu pada indeks tertentu dari koleksi."""
        if 0 <= index < len(self.daftar_lagu):
            return self.daftar_lagu.pop(index)
        return None

    def update_lagu_by_index(self, index, lagu_baru):
        """Memperbarui data lagu pada indeks tertentu."""
        if 0 <= index < len(self.daftar_lagu) and isinstance(lagu_baru, Lagu):
            self.daftar_lagu[index] = lagu_baru
            return True
        return False

    def muat_dari_baris(self, daftar_baris):
        """
        Merekonsiliasi data dari kumpulan baris teks file tabular.
        Mengabaikan data yang rusak tanpa menghentikan program.
        """
        self.daftar_lagu.clear()
        berhasil = 0
        for baris in daftar_baris:
            lagu = Lagu.from_line(baris)
            if lagu:
                self.daftar_lagu.append(lagu)
                berhasil += 1
        return berhasil

    def to_lines(self):
        """Mengonversi seluruh objek Lagu menjadi daftar baris string file."""
        return [l.to_line() for l in self.daftar_lagu]

    def generate_laporan(self):
        """
        Menghasilkan string laporan statistik dan daftar katalog lagu lengkap.
        """
        if not self.daftar_lagu:
            return "Koleksi musik masih kosong.\n"

        lap = "=" * 55 + "\n"
        lap += "         LAPORAN SISTEM MANAJEMEN MUSIK - MUSIKIFY\n"
        lap += "=" * 55 + "\n\n"

        total_durasi = self.hitung_total_durasi()
        rata2 = self.rata_rata_durasi()
        genre_pop, jumlah_pop = self.genre_terpopuler()

        lap += f"Total Lagu        : {len(self.daftar_lagu)} lagu\n"
        lap += f"Total Waktu Putar : {total_durasi // 60}m {total_durasi % 60:02d}s\n"
        lap += f"Rata-rata Durasi  : {int(rata2) // 60}:{int(rata2) % 60:02d}\n"
        lap += f"Genre Terpopuler  : {genre_pop} ({jumlah_pop} lagu)\n\n"

        lap += "SEBARAN DISTRIBUSI GENRE:\n" + "-" * 35 + "\n"
        for g, jml in sorted(self.lagu_per_genre().items()):
            bar = "#" * jml
            lap += f"  {g:<14}: {bar} ({jml})\n"

        lap += "\nDAFTAR KATALOG LAGU (Terurut Berdasarkan Judul):\n" + "-" * 55 + "\n"
        terurut = self.urutkan_lagu(berdasarkan="judul", reverse=False, algoritma="merge_sort")
        for i, l in enumerate(terurut, 1):
            lap += f"  {i:>2}. {l.info_lengkap()}\n"

        lap += "\n" + "=" * 55 + "\n"
        return lap

# ============================================================
# BLOK PENGUJIAN LOKAL - Hanya dieksekusi jika file di-run langsung
# ============================================================
if __name__ == '__main__':
    print("=== Pengujian Mandiri Modul processing.py ===")
    koleksi = KoleksiMusik()

    # Uji **kwargs
    koleksi.buat_record_lagu(judul="Bohemian Rhapsody", artis="Queen", genre="Rock", durasi=354, tahun=1975)
    koleksi.buat_record_lagu(judul="Shape of You", artis="Ed Sheeran", genre="Pop", durasi=234, tahun=2017)
    koleksi.buat_record_lagu(judul="Blinding Lights", artis="The Weeknd", genre="Pop", durasi=200, tahun=2020)

    # Uji *args
    l1 = Lagu("Hotel California", "Eagles", "Rock", 391, 1977)
    l2 = Lagu("Billie Jean", "Michael Jackson", "Pop", 294, 1982)
    koleksi.tambah_banyak_lagu(l1, l2)

    print(f"Total Lagu: {len(koleksi.daftar_lagu)}")
    print(f"Total Durasi (*args): {koleksi.hitung_total_durasi(60, 40)} detik")
    print(f"Rata-rata Durasi: {koleksi.rata_rata_durasi():.2f} detik")

    # Uji Sorting Merge Sort
    print("\n--- Hasil Merge Sort (by Durasi Ascending) ---")
    sorted_durasi = koleksi.urutkan_lagu(berdasarkan="durasi", reverse=False, algoritma="merge_sort")
    for s in sorted_durasi:
        print(f"  {s.durasi}s - {s.judul}")

    # Uji Searching Linear & Binary
    print("\n--- Uji Linear Search ('queen') ---")
    hasil_lin = koleksi.cari_lagu("queen")
    print(f"  Ditemukan: {[l.judul for l in hasil_lin]}")

    print("\n--- Uji Binary Search ('Shape of You') ---")
    hasil_bin = koleksi.cari_biner_judul("Shape of You")
    print(f"  Ditemukan: {hasil_bin}")

    print("\n[OK] Pengujian lokal processing.py selesai dengan sukses!")