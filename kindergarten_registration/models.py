from django.db import models

class Kres(models.Model):
    kres_ismi = models.CharField(max_length=100)
    siniflar = models.IntegerField(default=5)
    sinif_basi_ogrenci = models.IntegerField(default=10)
    toplam_ogrenci_limit = models.IntegerField(default=50)

    def bosluk_varmi(self):
        return self.student_count < (self.siniflar * self.sinif_basi_ogrenci)

    def __str__(self):
        return self.kres_ismi

    @property
    def student_count(self):
        return self.students.count()


class Ogrenci(models.Model):
    OKUL_TIPLERI = [
        ('None', 'No Experience'),
        ('Devlet', 'Devlet'),
        ('Özel', 'Özel'),
    ]
    # Student Information
    isim = models.CharField(max_length=100)
    tc_no = models.CharField(max_length=20, unique=True)
    adres = models.CharField(max_length=255)
    tuvalet_egitimi = models.BooleanField(default=False)
    okul_tecrubesi = models.CharField(max_length=10, choices=OKUL_TIPLERI, default='None', blank=True)
    devlet_ozel = models.CharField(max_length=10, choices=[('Devlet', 'Devlet'), ('Özel', 'Özel')], blank=True, null=True)
    kardes_sayisi = models.IntegerField(default=0, blank=True)
    tercih_edilen_okul = models.ForeignKey(Kres, on_delete=models.SET_NULL, null=True, blank=True)

    # Parent 1 Info
    anne_ismi = models.CharField(max_length=100, blank=True)
    anne_telefon = models.CharField(max_length=20, blank=True)
    anne_egitim = models.CharField(max_length=100, blank=True)
    anne_meslek = models.CharField(max_length=100, blank=True)
    anne_yasiyor = models.BooleanField(default=True)
    anne_ev_varmi = models.BooleanField(default=False)
    anne_evlimi = models.BooleanField(default=False)
    anne_maas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Parent 2 Info
    baba_isim = models.CharField(max_length=100, blank=True)
    baba_telefon = models.CharField(max_length=20, blank=True)
    baba_egitim = models.CharField(max_length=100, blank=True)
    baba_meslek = models.CharField(max_length=100, blank=True)
    baba_yasiyor = models.BooleanField(default=True)
    baba_ev_varmi = models.BooleanField(default=False)
    baba_evlimi = models.BooleanField(default=False)
    baba_maas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Foreign Key to Kindergarten
    kres = models.ForeignKey(Kres, related_name='students', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.isim} - {self.tc_no}"

    def calculate_points(self):
        points = 0

        if 'Atakum' in self.adres:
            points += 5
        if not self.tuvalet_egitimi:
            return "Elendi"
        if self.okul_tecrubesi == 'Devlet':
            points += 5
        if 'Atakum Belediyesi' in self.anne_meslek or 'Atakum Belediyesi' in self.baba_meslek:
            points += 5
        if not self.anne_yasiyor:
            points += 5
        if not self.baba_yasiyor:
            points += 5
        if self.anne_evlimi or self.baba_evlimi:
            points += 5
        if not self.anne_ev_varmi or not self.baba_ev_varmi:
            points += 5
        total_salary = (self.anne_maas or 0) + (self.baba_maas or 0)
        if total_salary < 20000:
            points -= 20
        elif 20000 <= total_salary < 30000:
            points -= 15
        elif 30000 <= total_salary < 40000:
            points -= 10
        elif 40000 <= total_salary < 50000:
            points -= 5
        elif total_salary >= 50000:
            points += 5

        points += self.kardes_sayisi

        return points
