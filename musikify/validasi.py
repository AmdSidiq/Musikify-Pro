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

def validasi_baris_data(baris):
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