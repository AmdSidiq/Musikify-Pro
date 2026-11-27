# ============================================================
# validasi.py - Modul Validasi Input dan Integritas Data
# Berisi fungsi-fungsi untuk memastikan keamanan tipe data,
# batas nilai input (range checking), serta parsing baris file.
# Menggunakan penanganan eksepsi (try/except) dan pelemparan error (raise).
# ============================================================

# Validasi durasi lagu dalam satuan detik
def validasi_durasi(durasi_str):
    """
    Memvalidasi input durasi lagu.
    - Wajib berupa angka integer positif.
    - Batas: > 0 detik dan <= 3600 detik (1 jam).
    - Melempar ValueError jika input tidak valid.
    """
    try:
        durasi = int(durasi_str)
    except (ValueError, TypeError):
        raise ValueError(f"Durasi '{durasi_str}' bukan angka yang valid!")

    if durasi <= 0:
        raise ValueError(f"Durasi lagu harus lebih dari 0 detik (diberikan: {durasi})!")
    if durasi > 3600:
        raise ValueError(f"Durasi lagu maksimal 3600 detik/1 jam (diberikan: {durasi})!")

    return durasi

# Validasi tahun rilis lagu
def validasi_tahun(tahun_str):
    """
    Memvalidasi tahun rilis lagu.
    - Wajib berupa angka integer.
    - Rentang yang diizinkan: 1900 hingga 2030.
    - Melempar ValueError jika input di luar batas wajar.
    """
    try:
        tahun = int(tahun_str)
    except (ValueError, TypeError):
        raise ValueError(f"Tahun '{tahun_str}' bukan angka yang valid!")

    if tahun < 1900 or tahun > 2030:
        raise ValueError(f"Tahun rilis harus berada dalam rentang 1900 - 2030 (diberikan: {tahun})!")

    return tahun

# Validasi field teks agar tidak kosong
def validasi_teks(teks, nama_field="Field"):
    """
    Memeriksa string input agar tidak kosong atau hanya berupa spasi whitespace.
    - Melempar ValueError jika string kosong.
    - Mengembalikan string yang telah di-strip.
    """
    if teks is None:
        raise ValueError(f"{nama_field} wajib diisi!")

    teks_bersih = str(teks).strip()
    if not teks_bersih:
        raise ValueError(f"{nama_field} tidak boleh kosong!")

    return teks_bersih

def validasi_baris_data(baris):
    """
    Mem-parsing dan memvalidasi satu baris data dari file tabular.
    - Jika format baris rusak atau tidak lengkap, baris dilewati (skip).
    - Mencegah UI atau program utama dari crash tiba-tiba saat file korup.
    - Mengembalikan dictionary jika valid, atau None jika baris tidak valid.
    """
    try:
        baris = baris.strip()
        if not baris or baris.startswith("judul"):
            return None

        bagian = baris.split("|")
        if len(bagian) != 5:
            print(f"Baris dilewati (jumlah kolom tidak sesuai 5): {baris}")
            return None

        judul, artis, genre, durasi_str, tahun_str = bagian
        return {
            "judul": validasi_teks(judul, "Judul"),
            "artis": validasi_teks(artis, "Artis"),
            "genre": validasi_teks(genre, "Genre"),
            "durasi": validasi_durasi(durasi_str.strip()),
            "tahun": validasi_tahun(tahun_str.strip())
        }
    except (ValueError, IndexError) as err:
        print(f"Baris dilewati karena format rusak ({err}): {baris}")
        return None