# ============================================================
# testing.py - Modul Pengujian Program (Unit Testing)
# Menggunakan library standar Python 'unittest'.
# Berisi class TestMusikify untuk menguji seluruh fungsi pengolahan data,
# algoritma pengurutan (Merge Sort & Selection Sort), algoritma pencarian
# (Linear Search & Binary Search), serta modul validasi data secara terpisah dari UI.
# ============================================================

import unittest

try:
    from .processing import (
        Lagu,
        KoleksiMusik,
        merge_sort,
        selection_sort
    )
    from .validasi import (
        validasi_durasi,
        validasi_tahun,
        validasi_teks,
        validasi_baris_data
    )
except ImportError:
    from processing import (
        Lagu,
        KoleksiMusik,
        merge_sort,
        selection_sort
    )
    from validasi import (
        validasi_durasi,
        validasi_tahun,
        validasi_teks,
        validasi_baris_data
    )


class TestMusikify(unittest.TestCase):
    """
    Class pengujian utama untuk program Musikify.
    Seluruh pengujian terpisah dari UI untuk menjamin independensi logika backend.
    """

    def setUp(self):
        """
        Test Fixture: Menyiapkan koleksi musik dengan data sampel
        sebelum setiap test case dieksekusi.
        """
        self.koleksi = KoleksiMusik()

        # Tambahkan 5 lagu sampel variatif menggunakan **kwargs
        self.koleksi.buat_record_lagu(
            judul="Bohemian Rhapsody", artis="Queen",
            genre="Rock", durasi=354, tahun=1975
        )
        self.koleksi.buat_record_lagu(
            judul="Shape of You", artis="Ed Sheeran",
            genre="Pop", durasi=234, tahun=2017
        )
        self.koleksi.buat_record_lagu(
            judul="Blinding Lights", artis="The Weeknd",
            genre="Pop", durasi=200, tahun=2020
        )
        self.koleksi.buat_record_lagu(
            judul="Hotel California", artis="Eagles",
            genre="Rock", durasi=391, tahun=1977
        )
        self.koleksi.buat_record_lagu(
            judul="Billie Jean", artis="Michael Jackson",
            genre="Pop", durasi=294, tahun=1982
        )

    # ========================================================
    # 1. PENGUJIAN MODUL VALIDASI (validasi.py)
    # ========================================================

    def test_validasi_durasi_valid_dan_invalid(self):
        """Menguji validasi durasi (angka valid, negatif, batas > 3600, bukan angka)."""
        # Input valid
        self.assertEqual(validasi_durasi("240"), 240)
        self.assertEqual(validasi_durasi(180), 180)

        # Input negatif harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_durasi("-15")

        # Input nol harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_durasi("0")

        # Input melebihi batas 3600 detik harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_durasi("3601")

        # Input bukan angka harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_durasi("abc")

    def test_validasi_tahun_valid_dan_invalid(self):
        """Menguji batas rentang tahun rilis (1900 - 2030)."""
        # Tahun valid
        self.assertEqual(validasi_tahun("2024"), 2024)
        self.assertEqual(validasi_tahun(1975), 1975)

        # Di bawah 1900 harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_tahun("1899")

        # Di atas 2030 harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_tahun("2031")

        # Non angka harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_tahun("tahun_dua_ribu")

    def test_validasi_teks_kosong(self):
        """Menguji validasi string teks tidak boleh kosong atau spasi doang."""
        self.assertEqual(validasi_teks("  Queen  ", "Artis"), "Queen")

        # String kosong harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_teks("", "Judul")

        # String hanya spasi harus raise ValueError
        with self.assertRaises(ValueError):
            validasi_teks("    ", "Genre")

    def test_validasi_baris_data_corrupt(self):
        """Menguji fungsi parsing baris data, memastikan baris rusak dilewati (skip)."""
        # Baris valid
        hasil_valid = validasi_baris_data("Test Song|Test Artist|Rock|210|2021")
        self.assertIsNotNone(hasil_valid)
        self.assertEqual(hasil_valid["judul"], "Test Song")

        # Baris kurang kolom (rusak) harus mengembalikan None tanpa crash
        hasil_rusak = validasi_baris_data("Hanya|Dua Kolom")
        self.assertIsNone(hasil_rusak)

        # Baris dengan nilai durasi bukan angka harus mengembalikan None
        hasil_tipe_salah = validasi_baris_data("Judul|Artis|Pop|durasi_salah|2020")
        self.assertIsNone(hasil_tipe_salah)

    # ========================================================
    # 2. PENGUJIAN ENTITAS CLASS LAGU (processing.py)
    # ========================================================

    def test_objek_lagu_dan_serialisasi(self):
        """Menguji instansiasi Class Lagu, format to_line() dan to_dict()."""
        lagu = Lagu("Bohemian Rhapsody", "Queen", "Rock", 354, 1975)
        self.assertEqual(lagu.judul, "Bohemian Rhapsody")
        self.assertEqual(lagu.durasi_formatted(), "05:54")
        self.assertEqual(lagu.to_line(), "Bohemian Rhapsody|Queen|Rock|354|1975")

        # Factory method from_line
        lagu_rekonstruksi = Lagu.from_line(lagu.to_line())
        self.assertIsNotNone(lagu_rekonstruksi)
        self.assertEqual(lagu_rekonstruksi.artis, "Queen")

    # ========================================================
    # 3. PENGUJIAN FUNGSI LANJUTAN (*args, **kwargs, lambda)
    # ========================================================

    def test_penggunaan_args_tambah_banyak_lagu(self):
        """Menguji *args pada method tambah_banyak_lagu."""
        k = KoleksiMusik()
        l1 = Lagu("Song 1", "Artist 1", "Pop", 180, 2020)
        l2 = Lagu("Song 2", "Artist 2", "Jazz", 210, 2021)
        l3 = Lagu("Song 3", "Artist 3", "Rock", 240, 2022)

        jumlah = k.tambah_banyak_lagu(l1, l2, l3)
        self.assertEqual(jumlah, 3)
        self.assertEqual(len(k.daftar_lagu), 3)

    def test_penggunaan_args_hitung_total_durasi(self):
        """Menguji *args pada method hitung_total_durasi."""
        # Total dasar koleksi: 354 + 234 + 200 + 391 + 294 = 1473 detik
        total_dasar = self.koleksi.hitung_total_durasi()
        self.assertEqual(total_dasar, 1473)

        # Mengirim durasi tambahan via *args (misal ekstra 60 detik dan 40 detik)
        total_ekstra = self.koleksi.hitung_total_durasi(60, 40)
        self.assertEqual(total_ekstra, 1473 + 100)

    def test_penggunaan_kwargs_buat_record_lagu(self):
        """Menguji **kwargs pada method buat_record_lagu."""
        k = KoleksiMusik()
        lagu = k.buat_record_lagu(
            judul="As It Was",
            artis="Harry Styles",
            genre="Pop",
            durasi=167,
            tahun=2022
        )
        self.assertEqual(lagu.judul, "As It Was")
        self.assertEqual(lagu.genre, "Pop")
        self.assertEqual(len(k.daftar_lagu), 1)

    def test_penggunaan_kwargs_filter_lagu(self):
        """Menguji **kwargs pada method filter_lagu."""
        hasil_pop = self.koleksi.filter_lagu(genre="Pop")
        self.assertEqual(len(hasil_pop), 3)

        hasil_tahun = self.koleksi.filter_lagu(tahun_min=2000)
        self.assertEqual(len(hasil_tahun), 2)  # Shape of You (2017) & Blinding Lights (2020)

    def test_agregasi_dan_genre_terpopuler_lambda(self):
        """Menguji perhitungan rata-rata durasi dan pencarian genre terpopuler dengan lambda."""
        # Rata-rata: 1473 / 5 = 294.6
        self.assertAlmostEqual(self.koleksi.rata_rata_durasi(), 294.6, places=1)

        # Genre terpopuler: Pop (3 lagu) vs Rock (2 lagu)
        genre, jumlah = self.koleksi.genre_terpopuler()
        self.assertEqual(genre, "Pop")
        self.assertEqual(jumlah, 3)

    # ========================================================
    # 4. PENGUJIAN ALGORITMA PENGURUTAN (SORTING)
    # ========================================================

    def test_algoritma_merge_sort_ascending_dan_descending(self):
        """Menguji algoritma Merge Sort (Divide and Conquer - O(n log n))."""
        # Urutkan berdasarkan durasi (Ascending)
        terurut_asc = merge_sort(self.koleksi.daftar_lagu, key_func=lambda l: l.durasi, reverse=False)
        self.assertEqual(terurut_asc[0].durasi, 200)   # Blinding Lights
        self.assertEqual(terurut_asc[-1].durasi, 391)  # Hotel California

        # Urutkan berdasarkan durasi (Descending)
        terurut_desc = merge_sort(self.koleksi.daftar_lagu, key_func=lambda l: l.durasi, reverse=True)
        self.assertEqual(terurut_desc[0].durasi, 391)
        self.assertEqual(terurut_desc[-1].durasi, 200)

    def test_algoritma_selection_sort(self):
        """Menguji algoritma Selection Sort (Materi Modul 10 - O(n^2))."""
        terurut_tahun = selection_sort(self.koleksi.daftar_lagu, key_func=lambda l: l.tahun, reverse=False)
        self.assertEqual(terurut_tahun[0].tahun, 1975)   # Bohemian Rhapsody
        self.assertEqual(terurut_tahun[-1].tahun, 2020)  # Blinding Lights

    # ========================================================
    # 5. PENGUJIAN ALGORITMA PENCARIAN (SEARCHING)
    # ========================================================

    def test_algoritma_linear_search(self):
        """Menguji algoritma Linear Search (pencarian sekuensial dengan filter field)."""
        # Cari artis 'Queen'
        hasil_queen = self.koleksi.cari_lagu("Queen", field="artis")
        self.assertEqual(len(hasil_queen), 1)
        self.assertEqual(hasil_queen[0].judul, "Bohemian Rhapsody")

        # Cari substring 'california' pada semua kolom
        hasil_calif = self.koleksi.cari_lagu("california", field="semua")
        self.assertEqual(len(hasil_calif), 1)
        self.assertEqual(hasil_calif[0].artis, "Eagles")

        # Cari keyword yang tidak ada
        hasil_nihil = self.koleksi.cari_lagu("TidakAda123")
        self.assertEqual(len(hasil_nihil), 0)

    def test_algoritma_binary_search(self):
        """Menguji algoritma Binary Search (O(log n) pada judul lagu terurut)."""
        # Cari judul yang ada
        hasil_bin = self.koleksi.cari_biner_judul("Shape of You")
        self.assertIsNotNone(hasil_bin)
        self.assertEqual(hasil_bin.artis, "Ed Sheeran")

        # Cari judul yang tidak ada
        hasil_bin_gagal = self.koleksi.cari_biner_judul("Lagu Fiktif")
        self.assertIsNone(hasil_bin_gagal)


# ============================================================
# EKSEKUSI PENGUJIAN MANDIRI
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  SUITE PENGUJIAN UNIT TESTING - MUSIKIFY")
    print("=" * 60)

    # Sanity Assertions sebelum unit test runner
    assert Lagu is not None, "Class Lagu wajib terdefinisi!"
    assert KoleksiMusik is not None, "Class KoleksiMusik wajib terdefinisi!"
    assert validasi_durasi("150") == 150, "Fungsi validasi_durasi harus berfungsi!"
    assert validasi_tahun("2022") == 2022, "Fungsi validasi_tahun harus berfungsi!"
    print("[✓] Assertion Check Passed: Seluruh modul backend siap diuji.\n")

    # Jalankan seluruh unit test dengan verbosity detail
    unittest.main(verbosity=2)
