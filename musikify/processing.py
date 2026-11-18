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