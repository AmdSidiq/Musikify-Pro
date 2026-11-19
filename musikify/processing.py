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
    - Kompleksitas Waktu: O(n log n) pada Best, Average, dan Worst Case.
    - Stabil dan sangat efisien untuk dataset berukuran besar.
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
    - Kompleksitas Waktu: O(n^2).
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