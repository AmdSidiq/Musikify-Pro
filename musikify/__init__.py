# ============================================================
# __init__.py - Inisialisasi Package Musikify
# Mengekspos komponen-komponen penting dari submodul agar dapat
# diimpor langsung melalui package 'musikify'.
# ============================================================

from .fileio import (
    inisialisasi_file,
    tambah_lagu,
    baca_semua_lagu,
    tulis_laporan,
    simpan_semua_lagu,
    NAMA_FILE_DATA,
    NAMA_FILE_LAPORAN
)

from .processing import (
    Lagu,
    KoleksiMusik,
    merge_sort,
    selection_sort,
    linear_search,
    binary_search_judul
)

from .validasi import (
    validasi_durasi,
    validasi_tahun,
    validasi_teks,
    validasi_baris_data,
    validasi_pilihan_menu
)

from .ui import (
    MusikifyUI,
    jalankan_aplikasi_ui
)

__all__ = [
    "inisialisasi_file", "tambah_lagu", "baca_semua_lagu", "tulis_laporan", "simpan_semua_lagu",
    "NAMA_FILE_DATA", "NAMA_FILE_LAPORAN",
    "Lagu", "KoleksiMusik", "merge_sort", "selection_sort", "linear_search", "binary_search_judul",
    "validasi_durasi", "validasi_tahun", "validasi_teks", "validasi_baris_data", "validasi_pilihan_menu",
    "MusikifyUI", "jalankan_aplikasi_ui"
]
