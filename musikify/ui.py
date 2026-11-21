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

def interpolasi_warna(warna1, warna2, t):
    """
    Menghitung interpolasi linier warna antara warna1 dan warna2 dalam format hex (#RRGGBB).
    Parameter t bernilai 0.0 sampai 1.0.
    """
    r1, g1, b1 = int(warna1[1:3], 16), int(warna1[3:5], 16), int(warna1[5:7], 16)
    r2, g2, b2 = int(warna2[1:3], 16), int(warna2[3:5], 16), int(warna2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class MusikifyUI:
    """
    Class Antarmuka Pengguna Grafis (GUI) utama untuk aplikasi Musikify.
    """

    # Palet Warna
    GRAD_RED = "#FF0000"    # Merah (Start Gradient)
    GRAD_ORANGE = "#FF8C00"   # Orange (Mid Gradient)
    GRAD_YELLOW = "#FFDD00"     # Kuning (End Gradient)

    BG_MAIN = "#FFF8DE"       # Background Utama
    BG_CARD = "#FFFFFF"       # Background Frame/Panel: Dark Slate Blue
    BG_INPUT = "#C2C2C2"      # Background Input Box: Deep Slate
    TEXT_LIGHT = "#000000"    # Teks Putih Utama
    TEXT_MUTED = "#94A3B8"    # Teks Abu-abu/Slate Sekunder

    ACCENT_GREEN = "#10B981"  # Aksen Hijau (Tombol aksi utama/tambah)
    ACCENT_CYAN = "#00B4D8"   # Aksen Cyan/Biru Muda (Binary Search)
    ACCENT_BLUE = "#2563EB"   # Aksen Biru (Sort & Laporan)
    ACCENT_RED = "#EF4444"    # Aksen Merah (Tombol Hapus)

    ROW_EVEN = "#FFFFFF"      # Baris genap tabel Treeview
    ROW_ODD = "#CFCFCF"       # Baris ganjil tabel Treeview

    def __init__(self, root):
        self.root = root
        self.root.title("Musikify")
        self.root.geometry("1040x700")
        self.root.minsize(880, 580)
        self.root.configure(bg=self.BG_MAIN)

        # Inisialisasi objek logika KoleksiMusik
        self.koleksi = KoleksiMusik()
        self.data_terfilter = []  # List penampung data yang sedang ditampilkan di tabel

        # Status pengurutan per kolom (kolom: reverse_bool)
        self.sort_status = {
            "No": False, "Judul": False, "Artis": False,
            "Genre": False, "Durasi": False, "Tahun": False
        }

        # Konfigurasi TTK Style
        self._konfigurasi_tema()

        # Bangun Komponen Antarmuka
        self._buat_banner_gradasi_header()
        self._buat_panel_ringkasan()
        self._buat_panel_kontrol()
        self._buat_tabel_tabular()
        self._buat_panel_aksi_bawah()
        self._buat_status_bar()

        # Inisialisasi file fisik dan muat data pertama kali
        self._muat_data_dari_file()

    # ========================================================
    # KONFIGURASI TEMA & STYLE
    # ========================================================
    def _konfigurasi_tema(self):
        """Mengatur styling widget ttk agar bernuansa gradasi gelap & modern."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview Styling
        self.style.configure(
            "Treeview",
            background=self.ROW_EVEN,
            foreground=self.TEXT_LIGHT,
            rowheight=29,
            fieldbackground=self.ROW_EVEN,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        self.style.map(
            "Treeview",
            background=[("selected", self.GRAD_ORANGE)],
            foreground=[("selected", "#000000")]
        )

        # Treeview Heading
        self.style.configure(
            "Treeview.Heading",
            background="#FFFFFF",
            foreground="#000000",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=7
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#E2E8F0")],
            foreground=[("active", "#000000")]
        )

        # Combobox Styling
        self.style.configure(
            "TCombobox",
            fieldbackground=self.BG_INPUT,
            background=self.BG_CARD,
            foreground=self.TEXT_LIGHT,
            arrowcolor=self.GRAD_RED
        )

    # ========================================================
    # BANNER GRADASI MERAH KE KUNING (HEADER)
    # ========================================================
    def _buat_banner_gradasi_header(self):
        """
        Membuat banner header interaktif dengan gradasi halus dari Merah ke Kuning.
        Menggambar gradasi secara dinamis menggunakan tk.Canvas.
        """
        self.header_canvas = tk.Canvas(self.root, height=75, bg=self.BG_MAIN, highlightthickness=0)
        self.header_canvas.pack(fill=tk.X, padx=0, pady=0)

        # Event binding agar gradasi menyesuaikan lebar jendela saat di-resize
        self.header_canvas.bind("<Configure>", self._gambar_gradasi_header)

    def _gambar_gradasi_header(self, event=None):
        """Menggambar garis-garis gradasi horizontal dari Merah ke Kuning."""
        w = self.header_canvas.winfo_width()
        h = self.header_canvas.winfo_height()

        if w <= 1:
            w = 1040
        if h <= 1:
            h = 75

        self.header_canvas.delete("all")

        # Menggambar 120 pita vertikal gradasi halus (Merah -> Orange -> Kuning)
        steps = 120
        step_w = w / steps
        for i in range(steps):
            t = i / steps
            warna = interpolasi_warna(self.GRAD_RED, self.GRAD_YELLOW, t)
            x0 = i * step_w
            x1 = (i + 1) * step_w + 1
            self.header_canvas.create_rectangle(x0, 0, x1, h, fill=warna, outline=warna)

        # Tambahkan teks judul aplikasi di atas kanvas gradasi
        self.header_canvas.create_text(
            25, 26,
            anchor=tk.W,
            text="MUSIKIFY",
            font=("Segoe UI", 21, "bold"),
            fill="#FFFFFF"
        )
        self.header_canvas.create_text(
            27, 52,
            anchor=tk.W,
            text="Sistem Manajemen Koleksi Musik",
            font=("Segoe UI", 10),
            fill="#E0F2FE"
        )

    # ========================================================
    # PANEL RINGKASAN DATA
    # ========================================================
    def _buat_panel_ringkasan(self):
        """Menampilkan 4 kartu ringkasan dengan border dan teks berwarna hitam."""
        self.summary_frame = tk.Frame(self.root, bg=self.BG_MAIN, padx=20, pady=8)
        self.summary_frame.pack(fill=tk.X)

        # Kartu 1: Total Lagu
        c1 = tk.Frame(self.summary_frame, bg=self.BG_CARD, highlightbackground="#000000",
                      highlightthickness=1, padx=14, pady=6)
        c1.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        tk.Label(c1, text="TOTAL KATALOG", font=("Segoe UI", 8, "bold"), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W)
        self.lbl_total_lagu = tk.Label(c1, text="0 Lagu", font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD)
        self.lbl_total_lagu.pack(anchor=tk.W)

        # Kartu 2: Total Durasi
        c2 = tk.Frame(self.summary_frame, bg=self.BG_CARD, highlightbackground="#000000",
                      highlightthickness=1, padx=14, pady=6)
        c2.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        tk.Label(c2, text="AKUMULASI WAKTU", font=("Segoe UI", 8, "bold"), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W)
        self.lbl_total_durasi = tk.Label(c2, text="0m 0s", font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD)
        self.lbl_total_durasi.pack(anchor=tk.W)

        # Kartu 3: Rata-rata Durasi
        c3 = tk.Frame(self.summary_frame, bg=self.BG_CARD, highlightbackground="#000000",
                      highlightthickness=1, padx=14, pady=6)
        c3.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        tk.Label(c3, text="RATA-RATA DURASI", font=("Segoe UI", 8, "bold"), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W)
        self.lbl_rata_durasi = tk.Label(c3, text="00:00", font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD)
        self.lbl_rata_durasi.pack(anchor=tk.W)

        # Kartu 4: Genre Terpopuler
        c4 = tk.Frame(self.summary_frame, bg=self.BG_CARD, highlightbackground="#000000",
                      highlightthickness=1, padx=14, pady=6)
        c4.pack(side=tk.LEFT, padx=(0, 0), expand=True, fill=tk.X)
        tk.Label(c4, text="GENRE TERPOPULER", font=("Segoe UI", 8, "bold"), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W)
        self.lbl_top_genre = tk.Label(c4, text="-", font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD)
        self.lbl_top_genre.pack(anchor=tk.W)

    # ========================================================
    # PANEL KONTROL (PENCARIAN DATA)
    # ========================================================
    def _buat_panel_kontrol(self):
        """Membuat panel kotak pencarian data lagu."""
        control_frame = tk.Frame(self.root, bg=self.BG_CARD, padx=16, pady=9)
        control_frame.pack(fill=tk.X, padx=20, pady=(4, 10))

        # --- SEKSI PENCARIAN (SEARCHING) ---
        lbl_cari = tk.Label(control_frame, text="🔍 Cari:", font=("Segoe UI", 10, "bold"),
                            fg=self.TEXT_LIGHT, bg=self.BG_CARD)
        lbl_cari.pack(side=tk.LEFT, padx=(0, 8))

        self.entry_cari = tk.Entry(control_frame, font=("Segoe UI", 10), bg=self.BG_INPUT,
                                   fg=self.TEXT_LIGHT, insertbackground="white", width=30, relief="flat")
        self.entry_cari.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)
        self.entry_cari.bind("<Return>", lambda e: self.aksi_cari_linear(tampilkan_popup=True))
        self.entry_cari.bind("<KeyRelease>", lambda e: self.aksi_cari_linear(tampilkan_popup=False))

        self.cmb_field_cari = ttk.Combobox(
            control_frame, values=["Semua Kolom", "Judul", "Artis", "Genre"],
            state="readonly", width=14
        )
        self.cmb_field_cari.set("Semua Kolom")
        self.cmb_field_cari.pack(side=tk.LEFT, padx=(0, 8))
        self.cmb_field_cari.bind("<<ComboboxSelected>>", lambda e: self.aksi_cari_linear(tampilkan_popup=False))

        # Hint interaktif sorting
        lbl_hint = tk.Label(
            control_frame,
            text="Tip: Klik header kolom tabel untuk mengurutkan (Merge Sort)",
            font=("Segoe UI", 8, "italic"),
            fg="#64748B",
            bg=self.BG_CARD
        )
        lbl_hint.pack(side=tk.RIGHT, padx=(8, 0))

    # ========================================================
    # TABEL TABULAR DATA (TREEVIEW)
    # ========================================================
    def _buat_tabel_tabular(self):
        """Membuat tabel ttk.Treeview untuk menyajikan data secara tabular."""
        table_container = tk.Frame(self.root, bg=self.BG_MAIN)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Definisi Kolom Tabel
        kolom = ("No", "Judul", "Artis", "Genre", "Durasi", "Tahun")
        self.tree = ttk.Treeview(table_container, columns=kolom, show="headings", selectmode="browse")

        # Konfigurasi Header & Lebar Kolom
        lebar_kolom = {
            "No": 50,
            "Judul": 280,
            "Artis": 220,
            "Genre": 140,
            "Durasi": 110,
            "Tahun": 90
        }

        for col in kolom:
            self.tree.heading(
                col,
                text=col,
                anchor=tk.CENTER if col in ("No", "Genre", "Durasi", "Tahun") else tk.W,
                command=lambda c=col: self._klik_header_kolom(c)
            )
            self.tree.column(
                col,
                width=lebar_kolom[col],
                anchor=tk.CENTER if col in ("No", "Genre", "Durasi", "Tahun") else tk.W
            )

        # Scrollbar Vertikal & Horizontal
        vsb = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Tag warna alternating rows
        self.tree.tag_configure("genap", background=self.ROW_EVEN, foreground="#000000")
        self.tree.tag_configure("ganjil", background=self.ROW_ODD, foreground="#000000")

    # ========================================================
    # PANEL AKSI BAWAH (CRUD, REPORT, STATS, TEST)
    # ========================================================
    def _buat_panel_aksi_bawah(self):
        """Membuat tombol-tombol aksi utama di bagian bawah tabel."""
        btn_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 8))

        # Tombol Tambah Lagu (Hijau Emerald)
        btn_tambah = tk.Button(
            btn_frame, text="➕ Tambah Lagu", font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT_GREEN, fg="#000000", activebackground="#059669",
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self.dialog_tambah_lagu
        )
        btn_tambah.pack(side=tk.LEFT, padx=(0, 8))

        # Tombol Hapus Lagu (Merah Coral)
        btn_hapus = tk.Button(
            btn_frame, text="🗑️ Hapus Terpilih", font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_RED, fg="#FFFFFF", activebackground="#DC2626",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.aksi_hapus_lagu
        )
        btn_hapus.pack(side=tk.LEFT, padx=(0, 8))

        # Tombol Statistik & Visualisasi (Toska / Cyan)
        btn_stats = tk.Button(
            btn_frame, text="📊 Visualisasi Statistik", font=("Segoe UI", 9, "bold"),
            bg="#0284C7", fg="#FFFFFF", activebackground="#0369A1",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.dialog_visualisasi_statistik
        )
        btn_stats.pack(side=tk.LEFT, padx=(0, 8))

        # Tombol Generate Laporan (Biru Royal)
        btn_laporan = tk.Button(
            btn_frame, text="📄 Generate Laporan ('w')", font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_BLUE, fg="#FFFFFF", activebackground="#1D4ED8",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.aksi_generate_laporan
        )
        btn_laporan.pack(side=tk.LEFT, padx=(0, 8))

        # Tombol Jalankan Unit Test (Indigo)
        btn_test = tk.Button(
            btn_frame, text="🧪 Jalankan Unit Test", font=("Segoe UI", 9, "bold"),
            bg="#4F46E5", fg="#FFFFFF", activebackground="#4338CA",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.dialog_jalankan_unittest
        )
        btn_test.pack(side=tk.RIGHT, padx=(8, 0))

        # Tombol Muat Ulang File (Dark Slate)
        btn_reload = tk.Button(
            btn_frame, text="🔄 Reload File ('r')", font=("Segoe UI", 9),
            bg="#334155", fg="#FFFFFF", activebackground="#475569",
            relief="flat", cursor="hand2", padx=10, pady=6,
            command=self._muat_data_dari_file
        )
        btn_reload.pack(side=tk.RIGHT)

    # ========================================================
    # STATUS BAR
    # ========================================================
    def _buat_status_bar(self):
        """Membuat status bar di bagian paling bawah jendela."""
        self.status_var = tk.StringVar(value="Siap.")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 9), fg=self.TEXT_MUTED, bg="#060C18",
            anchor=tk.W, padx=15, pady=4
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ========================================================
    # LOGIKA FILE HANDLING & PEMUATAN DATA (MODES 'x', 'r')
    # ========================================================
    def _muat_data_dari_file(self):
        """
        Memuat data dari file persisten data_musik.txt.
        Menangani try/except untuk FileNotFoundError dan ValueError
        agar antarmuka pengguna TIDAK mendadak crash saat file rusak/hilang.
        """
        try:
            # Pastikan file ada dengan mode 'x' jika pertama kali
            inisialisasi_file(NAMA_FILE_DATA)

            # Baca seluruh baris dengan mode 'r' (iteratif)
            daftar_baris = baca_semua_lagu(NAMA_FILE_DATA)

            # Muat ke dalam objek KoleksiMusik
            jumlah = self.koleksi.muat_dari_baris(daftar_baris)
            self.data_terfilter = list(self.koleksi.daftar_lagu)

            # Render data ke tabel
            self._render_tabel(self.data_terfilter)
            self._update_panel_ringkasan()

            self.status_var.set(f"Berhasil memuat {jumlah} lagu dari '{NAMA_FILE_DATA}'.")
        except FileNotFoundError as e:
            messagebox.showwarning("File Belum Ada", f"File data belum ditemukan:\n{e}\nFile baru telah diinisialisasi.")
            self.status_var.set("File baru diinisialisasi.")
        except Exception as e:
            messagebox.showerror("Error Pembacaan", f"Terjadi kesalahan saat memuat file data:\n{e}")
            self.status_var.set("Gagal memuat data dari file.")

    # ========================================================
    # RENDERING TABULAR DATA
    # ========================================================
    def _render_tabel(self, daftar_tampil):
        """Merender list objek Lagu ke dalam ttk.Treeview."""
        # Bersihkan tabel lama
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Masukkan data baris per baris
        for i, lagu in enumerate(daftar_tampil, 1):
            tag = "genap" if i % 2 == 0 else "ganjil"
            self.tree.insert(
                "",
                tk.END,
                values=(i, lagu.judul, lagu.artis, lagu.genre, lagu.durasi_formatted(), lagu.tahun),
                tags=(tag,)
            )

    def _update_panel_ringkasan(self):
        """Memperbarui informasi metrik pada card ringkasan atas."""
        total_lagu = len(self.koleksi.daftar_lagu)
        total_durasi = self.koleksi.hitung_total_durasi()
        rata_durasi = self.koleksi.rata_rata_durasi()
        top_genre, jml_top = self.koleksi.genre_terpopuler()

        menit_tot = total_durasi // 60
        detik_tot = total_durasi % 60
        menit_avg = int(rata_durasi) // 60
        detik_avg = int(rata_durasi) % 60

        self.lbl_total_lagu.config(text=f"{total_lagu} Lagu")
        self.lbl_total_durasi.config(text=f"{menit_tot}m {detik_tot:02d}s")
        self.lbl_rata_durasi.config(text=f"{menit_avg:02d}:{detik_avg:02d}")
        self.lbl_top_genre.config(text=f"{top_genre} ({jml_top} lagu)")

    # ========================================================
    # AKSI PENCARIAN (LINEAR SEARCH & BINARY SEARCH)
    # ========================================================
    def aksi_cari_linear(self, tampilkan_popup=False):
        """Menjalankan Linear Search berdasarkan input keyword dan field."""
        keyword = self.entry_cari.get().strip()
        field_pilihan = self.cmb_field_cari.get()

        field_map = {
            "Semua Kolom": "semua",
            "Judul": "judul",
            "Artis": "artis",
            "Genre": "genre"
        }
        field = field_map.get(field_pilihan, "semua")

        if not keyword:
            self.data_terfilter = list(self.koleksi.daftar_lagu)
            self._render_tabel(self.data_terfilter)
            self.status_var.set("Menampilkan seluruh data.")
            return

        # Panggil fungsi linear_search
        hasil = self.koleksi.cari_lagu(keyword, field=field)
        self.data_terfilter = hasil
        self._render_tabel(self.data_terfilter)

        self.status_var.set(
            f"Linear Search '{keyword}' pada [{field_pilihan}]: ditemukan {len(hasil)} dari {len(self.koleksi.daftar_lagu)} lagu."
        )

        if not hasil and tampilkan_popup:
            messagebox.showinfo("Hasil Pencarian", f"Tidak ditemukan lagu yang cocok dengan kata kunci: '{keyword}'")

    def aksi_cari_binary(self):
        """
        Menjalankan Binary Search berdasarkan Judul Lagu.
        Mencari lagu secara efisien O(log n) pada data yang telah diurutkan.
        """
        keyword = self.entry_cari.get().strip()
        if not keyword:
            messagebox.showwarning("Peringatan", "Silakan masukkan kata kunci judul untuk Binary Search!")
            return

        lagu_ditemukan = self.koleksi.cari_biner_judul(keyword)

        if lagu_ditemukan:
            self.data_terfilter = [lagu_ditemukan]
            self._render_tabel(self.data_terfilter)
            self.status_var.set(f"Binary Search berhasil menemukan: {lagu_ditemukan.info_lengkap()}")
            messagebox.showinfo(
                "Lagu Ditemukan (Binary Search)",
                f"Lagu Berhasil Ditemukan!\n\n"
                f"Judul  : {lagu_ditemukan.judul}\n"
                f"Artis  : {lagu_ditemukan.artis}\n"
                f"Genre  : {lagu_ditemukan.genre}\n"
                f"Durasi : {lagu_ditemukan.durasi_formatted()} ({lagu_ditemukan.durasi} detik)\n"
                f"Tahun  : {lagu_ditemukan.tahun}"
            )
        else:
            messagebox.showinfo("Tidak Ditemukan", f"Binary Search: Lagu dengan judul '{keyword}' tidak ditemukan!")
            self.status_var.set(f"Binary Search: '{keyword}' tidak ditemukan.")

    # ========================================================
    # AKSI PENGURUTAN (SORTING - MERGE SORT & SELECTION SORT)
    # ========================================================
    def aksi_urutkan_data(self):
        """Mengurutkan data tampilan berdasarkan kolom dan algoritma yang dipilih."""
        if not hasattr(self, 'cmb_sort_col'):
            return

        kriteria = self.cmb_sort_col.get().lower()
        algo_pilihan = self.cmb_sort_algo.get()
        is_desc = self.var_descending.get()

        algo_code = "merge_sort"
        if "Selection" in algo_pilihan:
            algo_code = "selection_sort"
        elif "Timsort" in algo_pilihan:
            algo_code = "python_sort"

        # Pemanggilan method dengan Keyword Argument eksplisit
        hasil_urut = self.koleksi.urutkan_lagu(
            berdasarkan=kriteria,
            reverse=is_desc,
            algoritma=algo_code
        )

        self.data_terfilter = hasil_urut
        self._render_tabel(self.data_terfilter)

        arah = "Z-A (Descending)" if is_desc else "A-Z (Ascending)"
        self.status_var.set(f"Diurutkan berdasarkan [{kriteria.upper()}] ({arah}) menggunakan {algo_pilihan}.")

    def _klik_header_kolom(self, col):
        """Fitur interaktif: klik header kolom untuk mengurutkan data seketika."""
        if col == "No":
            return

        col_name = col.lower()
        self.sort_status[col] = not self.sort_status[col]
        is_desc = self.sort_status[col]

        # Update combobox jika ada
        if hasattr(self, 'cmb_sort_col'):
            self.cmb_sort_col.set(col)
        if hasattr(self, 'var_descending'):
            self.var_descending.set(is_desc)

        # Jalankan pengurutan dengan Merge Sort (O(n log n))
        hasil = self.koleksi.urutkan_lagu(berdasarkan=col_name, reverse=is_desc, algoritma="merge_sort")
        self.data_terfilter = hasil
        self._render_tabel(self.data_terfilter)

        arah = "▼ Descending" if is_desc else "▲ Ascending"
        self.status_var.set(f"Tabel diurutkan berdasar [{col}] {arah} (Merge Sort).")

    def aksi_reset_tampilan(self):
        """Mengembalikan tampilan tabel ke kondisi semula."""
        self.entry_cari.delete(0, tk.END)
        self.cmb_field_cari.set("Semua Kolom")
        if hasattr(self, 'cmb_sort_col'):
            self.cmb_sort_col.set("Judul")
        if hasattr(self, 'var_descending'):
            self.var_descending.set(False)
        self.data_terfilter = list(self.koleksi.daftar_lagu)
        self._render_tabel(self.data_terfilter)
        self.status_var.set("Tampilan di-reset ke seluruh data.")

    # ========================================================
    # DIALOG TAMBAH LAGU BARU (MODES 'a' - APPEND)
    # ========================================================
    def dialog_tambah_lagu(self):
        """
        Membuka jendela dialog popup untuk menambah lagu baru.
        Menerapkan validasi ketat (try/except) untuk menangani ValueError dari modul validasi.py.
        """
        modal = tk.Toplevel(self.root)
        modal.title("➕ Tambah Lagu Baru")
        modal.geometry("450x370")
        modal.resizable(False, False)
        modal.configure(bg=self.BG_CARD)
        modal.transient(self.root)
        modal.grab_set()

        # Posisi tengah
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 225
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 185
        modal.geometry(f"+{x}+{y}")

        title_lbl = tk.Label(
            modal, text="MASUKKAN DATA LAGU BARU",
            font=("Segoe UI", 12, "bold"), fg=self.TEXT_LIGHT, bg=self.BG_CARD
        )
        title_lbl.pack(pady=(16, 14))

        form_frame = tk.Frame(modal, bg=self.BG_CARD)
        form_frame.pack(padx=25, fill=tk.X)

        fields = [
            ("Judul Lagu:", "e_judul"),
            ("Nama Artis:", "e_artis"),
            ("Genre Musik:", "e_genre"),
            ("Durasi (detik):", "e_durasi"),
            ("Tahun Rilis:", "e_tahun")
        ]

        entries = {}

        for i, (label_text, var_name) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label_text, font=("Segoe UI", 9, "bold"),
                           fg=self.TEXT_LIGHT, bg=self.BG_CARD, anchor=tk.W)
            lbl.grid(row=i, column=0, sticky=tk.W, pady=6)

            if var_name == "e_genre":
                ent = ttk.Combobox(
                    form_frame,
                    values=["Pop", "Rock", "Jazz", "R&B", "Hip-Hop", "Indie", "EDM", "Dangdut", "Classical", "Other"],
                    font=("Segoe UI", 9), width=24
                )
                ent.set("Pop")
            else:
                ent = tk.Entry(form_frame, font=("Segoe UI", 9), bg=self.BG_INPUT,
                               fg=self.TEXT_LIGHT, insertbackground="white", width=26, relief="flat")

            ent.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=6)
            entries[var_name] = ent

        entries["e_judul"].focus_set()

        def simpan_lagu():
            try:
                # Validasi menggunakan modul validasi.py
                judul = validasi_teks(entries["e_judul"].get(), "Judul Lagu")
                artis = validasi_teks(entries["e_artis"].get(), "Nama Artis")
                genre = validasi_teks(entries["e_genre"].get(), "Genre Musik")
                durasi = validasi_durasi(entries["e_durasi"].get())
                tahun = validasi_tahun(entries["e_tahun"].get())

                # Buat objek Lagu
                lagu_baru = Lagu(judul, artis, genre, durasi, tahun)

                # Simpan permanen ke file fisik dengan mode 'a' (append)
                tambah_lagu(NAMA_FILE_DATA, lagu_baru.to_line())

                # Tambahkan ke objek KoleksiMusik di memori
                self.koleksi.tambah_lagu(lagu_baru)
                self.data_terfilter = list(self.koleksi.daftar_lagu)

                # Perbarui antarmuka
                self._render_tabel(self.data_terfilter)
                self._update_panel_ringkasan()

                self.status_var.set(f"Berhasil menambah lagu: {lagu_baru.info_lengkap()}")
                messagebox.showinfo("Sukses", f"Lagu berhasil disimpan ke file data!\n\n{lagu_baru.info_lengkap()}")
                modal.destroy()

            except ValueError as ve:
                # Tangkap eksepsi validasi agar UI tidak crash
                messagebox.showerror("Validasi Gagal", str(ve))

        # Tombol Simpan & Batal
        btn_box = tk.Frame(modal, bg=self.BG_CARD)
        btn_box.pack(pady=20)

        btn_save = tk.Button(
            btn_box, text="💾 Simpan Lagu ('a')", font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_GREEN, fg="#000000", activebackground="#059669",
            relief="flat", cursor="hand2", padx=12, pady=5, command=simpan_lagu
        )
        btn_save.pack(side=tk.LEFT, padx=8)

        btn_cancel = tk.Button(
            btn_box, text="Batal", font=("Segoe UI", 9),
            bg="#334155", fg="#FFFFFF", activebackground="#475569",
            relief="flat", cursor="hand2", padx=12, pady=5, command=modal.destroy
        )
        btn_cancel.pack(side=tk.LEFT, padx=8)

    # ========================================================
    # AKSI HAPUS LAGU (DENGAN SINKRONISASI FILE 'w')
    # ========================================================
    def aksi_hapus_lagu(self):
        """Menghapus baris lagu yang sedang dipilih di tabel."""
        terpilih = self.tree.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Silakan pilih baris lagu yang ingin dihapus pada tabel!")
            return

        item = self.tree.item(terpilih[0])
        values = item["values"]
        judul_hapus = str(values[1])
        artis_hapus = str(values[2])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus lagu berikut?\n\n"
            f"🎵 {judul_hapus} - {artis_hapus}\n\n"
            "Data akan dihapus permanen dari file 'data_musik.txt'."
        )

        if konfirmasi:
            # Cari indeks lagu pada koleksi
            idx_ditemukan = None
            for idx, l in enumerate(self.koleksi.daftar_lagu):
                if l.judul == judul_hapus and l.artis == artis_hapus:
                    idx_ditemukan = idx
                    break

            if idx_ditemukan is not None:
                self.koleksi.hapus_lagu_by_index(idx_ditemukan)

                # Simpan ulang file data dengan mode 'w'
                simpan_semua_lagu(NAMA_FILE_DATA, self.koleksi.to_lines())

                # Perbarui antarmuka
                self.data_terfilter = list(self.koleksi.daftar_lagu)
                self._render_tabel(self.data_terfilter)
                self._update_panel_ringkasan()

                self.status_var.set(f"Lagu '{judul_hapus}' berhasil dihapus.")
                messagebox.showinfo("Dihapus", f"Lagu '{judul_hapus}' telah dihapus dari koleksi.")

    # ========================================================
    # DIALOG VISUALISASI STATISTIK
    # ========================================================
    def dialog_visualisasi_statistik(self):
        """
        Menampilkan jendela popup analisis data dan grafik batang horizontal
        berwarna gradasi Hijau hingga Biru.
        """
        if not self.koleksi.daftar_lagu:
            messagebox.showinfo("Koleksi Kosong", "Belum ada lagu untuk divisualisasikan.")
            return

        modal = tk.Toplevel(self.root)
        modal.title("Visualisasi Statistik Koleksi Musik")
        modal.geometry("580x500")
        modal.resizable(False, False)
        modal.configure(bg=self.BG_CARD)
        modal.transient(self.root)

        # Header Visualisasi
        header_lbl = tk.Label(
            modal, text="ANALISIS & VISUALISASI DATA KOLEKSI",
            font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD
        )
        header_lbl.pack(pady=(15, 10))

        # Statistik Utama
        total_lagu = len(self.koleksi.daftar_lagu)
        total_durasi = self.koleksi.hitung_total_durasi()
        rata_durasi = self.koleksi.rata_rata_durasi()
        top_genre, jml_top = self.koleksi.genre_terpopuler()

        stats_box = tk.LabelFrame(
            modal, text=" Ringkasan Metrik ", font=("Segoe UI", 9, "bold"),
            fg="#000000", bg=self.BG_CARD, padx=14, pady=8
        )
        stats_box.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(stats_box, text=f"• Total Katalog Lagu : {total_lagu} lagu",
                 font=("Segoe UI", 9), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W, pady=2)
        tk.Label(stats_box, text=f"• Akumulasi Durasi  : {total_durasi // 60}m {total_durasi % 60:02d}s ({total_durasi} detik)",
                 font=("Segoe UI", 9), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W, pady=2)
        tk.Label(stats_box, text=f"• Rata-rata Durasi  : {int(rata_durasi) // 60}:{int(rata_durasi) % 60:02d}",
                 font=("Segoe UI", 9), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W, pady=2)
        tk.Label(stats_box, text=f"• Genre Dominan     : {top_genre} ({jml_top} lagu - {jml_top / total_lagu * 100:.1f}%)",
                 font=("Segoe UI", 9, "bold"), fg="#000000", bg=self.BG_CARD).pack(anchor=tk.W, pady=2)

        # Visualisasi Distribusi Genre
        vis_box = tk.LabelFrame(
            modal, text=" Visualisasi Distribusi Genre ",
            font=("Segoe UI", 9, "bold"), fg="#000000", bg=self.BG_CARD, padx=14, pady=8
        )
        vis_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        distribusi = self.koleksi.lagu_per_genre()
        max_jml = max(distribusi.values()) if distribusi else 1
        sorted_genres = sorted(distribusi.items(), key=lambda x: x[1], reverse=True)
        total_items = max(len(sorted_genres) - 1, 1)

        for idx, (g, jml) in enumerate(sorted_genres):
            row_frame = tk.Frame(vis_box, bg=self.BG_CARD)
            row_frame.pack(fill=tk.X, pady=4)

            # Warna batang visualisasi hitam
            warna_bar = "#000000"

            # Label Genre
            pct = (jml / total_lagu) * 100
            lbl_g = tk.Label(row_frame, text=f"{g:<12}", font=("Segoe UI", 9, "bold"),
                             fg="#000000", bg=self.BG_CARD, width=12, anchor=tk.W)
            lbl_g.pack(side=tk.LEFT)

            # Canvas Bar
            canvas_bar = tk.Canvas(row_frame, width=280, height=18, bg=self.BG_INPUT, highlightthickness=0)
            canvas_bar.pack(side=tk.LEFT, padx=6)

            # Hitung lebar batang
            bar_width = int((jml / max_jml) * 276)
            canvas_bar.create_rectangle(2, 2, 2 + bar_width, 16, fill=warna_bar, outline="")

            # Label Angka & Persentase
            lbl_val = tk.Label(row_frame, text=f"{jml} ({pct:.0f}%)", font=("Segoe UI", 9, "bold"),
                               fg="#000000", bg=self.BG_CARD, width=9, anchor=tk.W)
            lbl_val.pack(side=tk.LEFT)

        btn_tutup = tk.Button(
            modal, text="Tutup", font=("Segoe UI", 9),
            bg="#334155", fg="#FFFFFF", activebackground="#475569",
            relief="flat", cursor="hand2", padx=15, pady=4, command=modal.destroy
        )
        btn_tutup.pack(pady=(0, 15))

    # ========================================================
    # GENERATE LAPORAN KE FILE (MODE 'w')
    # ========================================================
    def aksi_generate_laporan(self):
        """Menghasilkan laporan teks dan menyimpannya ke laporan_musik.txt (mode 'w')."""
        if not self.koleksi.daftar_lagu:
            messagebox.showwarning("Peringatan", "Koleksi kosong. Tidak ada data untuk dilaporkan.")
            return

        konten_laporan = self.koleksi.generate_laporan()

        # Tulis ke file fisik dengan mode 'w'
        tulis_laporan(NAMA_FILE_LAPORAN, konten_laporan)
        self.status_var.set(f"Laporan berhasil dicetak ke '{NAMA_FILE_LAPORAN}'.")

        # Tampilkan Jendela Preview Laporan
        modal = tk.Toplevel(self.root)
        modal.title(f"Preview Laporan - {NAMA_FILE_LAPORAN}")
        modal.geometry("640x520")
        modal.configure(bg=self.BG_CARD)
        modal.transient(self.root)

        txt_preview = scrolledtext.ScrolledText(
            modal, font=("Consolas", 10), bg="#FFFFFF", fg="#000000",
            insertbackground="black", padx=10, pady=10, relief="solid", borderwidth=1
        )
        txt_preview.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        txt_preview.insert(tk.END, konten_laporan)
        txt_preview.configure(state="disabled")

        btn_close = tk.Button(
            modal, text="Tutup", font=("Segoe UI", 9),
            bg="#334155", fg="#FFFFFF", relief="flat", padx=12, pady=4,
            command=modal.destroy
        )
        btn_close.pack(pady=(0, 10))

    # ========================================================
    # JALANKAN UNIT TEST DARI UI
    # ========================================================
    def dialog_jalankan_unittest(self):
        """
        Menjalankan pengujian otomatis unittest langsung dari antarmuka UI
        dan menampilkan laporannya
        """
        import io
        import unittest

        try:
            from .testing import TestMusikify
        except ImportError:
            from testing import TestMusikify

        modal = tk.Toplevel(self.root)
        modal.title("🧪 Hasil Pengujian Otomatis (Unittest Runner)")
        modal.geometry("680x480")
        modal.configure(bg=self.BG_CARD)
        modal.transient(self.root)

        lbl = tk.Label(
            modal, text="HASIL EKSEKUSI PENGUJIAN UNITTEST",
            font=("Segoe UI", 12, "bold"), fg="#000000", bg=self.BG_CARD
        )
        lbl.pack(pady=(15, 8))

        txt_output = scrolledtext.ScrolledText(
            modal, font=("Consolas", 9), bg="#060C18", fg="#A7F3D0",
            insertbackground="white", padx=10, pady=10
        )
        txt_output.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 12))

        # Tangkap stream output runner
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMusikify)
        hasil = runner.run(suite)

        log_teks = stream.getvalue()
        txt_output.insert(tk.END, log_teks)
        txt_output.configure(state="disabled")

        if hasil.wasSuccessful():
            status_txt = f"SEMUA PENGUJIAN BERHASIL ({hasil.testsRun} TEST CASES PASSED)"
            status_fg = self.TEXT_LIGHT
        else:
            status_txt = f"TERDAPAT {len(hasil.failures)} TEST GAGAL"
            status_fg = self.ACCENT_RED

        lbl_res = tk.Label(modal, text=status_txt, font=("Segoe UI", 11, "bold"), fg=status_fg, bg=self.BG_CARD)
        lbl_res.pack(pady=(0, 10))

        btn_tutup = tk.Button(
            modal, text="Tutup", font=("Segoe UI", 9),
            bg="#334155", fg="#FFFFFF", relief="flat", padx=12, pady=4,
            command=modal.destroy
        )
        btn_tutup.pack(pady=(0, 12))


# Fungsi instansiasi untuk dipanggil dari main.py
def jalankan_aplikasi_ui():
    """Fungsi pembungkus untuk memulai loop aplikasi Tkinter."""
    root = tk.Tk()
    MusikifyUI(root)
    root.mainloop()


if __name__ == '__main__':
    jalankan_aplikasi_ui()
