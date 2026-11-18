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