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