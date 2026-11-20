import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

try:
    from .fileio import (inisialisasi_file, tambah_lagu, baca_semua_lagu,
                         tulis_laporan, simpan_semua_lagu,
                         NAMA_FILE_DATA, NAMA_FILE_LAPORAN)
    from .processing import Lagu, KoleksiMusik
    from .validasi import validasi_teks, validasi_durasi, validasi_tahun
except ImportError:
    from fileio import (inisialisasi_file, tambah_lagu, baca_semua_lagu,
                        tulis_laporan, simpan_semua_lagu,
                        NAMA_FILE_DATA, NAMA_FILE_LAPORAN)
    from processing import Lagu, KoleksiMusik
    from validasi import validasi_teks, validasi_durasi, validasi_tahun