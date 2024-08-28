from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver

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

    sinif = models.ForeignKey('Sınıf', related_name='sınıf_students', on_delete=models.SET_NULL, null=True, blank=True)
    elendi = models.BooleanField(default=False)

    isim = models.CharField(max_length=100)
    soyisim = models.CharField(max_length=100,blank=True)
    tc_no = models.CharField(max_length=11,primary_key=True)
    adres = models.CharField(max_length=255)
    dogum_tarihi = models.DateField(default=timezone.now)
    kayıt_tarihi = models.DateTimeField(default=timezone.now)
    tuvalet_egitimi = models.BooleanField(default=False)
    okul_tecrubesi = models.CharField(max_length=10, default='None', blank=True)
    devlet_ozel = models.CharField(max_length=10, choices=[('Devlet', 'Devlet'), ('Özel', 'Özel')], blank=True, null=True)
    kardes_sayisi = models.IntegerField(default=0, blank=True)
    tercih_edilen_okul = models.ForeignKey('Kres', on_delete=models.SET_NULL, null=True, blank=True)

    # Parent 1 Info
    anne_isim = models.CharField(max_length=100, blank=True)
    anne_soyisim = models.CharField(max_length=100, blank=True)
    anne_telefon = models.CharField(max_length=20, blank=True)
    anne_egitim = models.CharField(max_length=100, blank=True)
    anne_meslek = models.CharField(max_length=100, blank=True)
    anne_kurum = models.CharField(max_length=100, blank=True)
    anne_yasiyor = models.BooleanField(default=True)
    anne_oz = models.BooleanField(default=True)
    anne_maas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Parent 2 Info
    baba_isim = models.CharField(max_length=100, blank=True)
    baba_soyisim = models.CharField(max_length=100, blank=True)
    baba_telefon = models.CharField(max_length=20, blank=True)
    baba_egitim = models.CharField(max_length=100, blank=True)
    baba_meslek = models.CharField(max_length=100, blank=True)
    baba_kurum = models.CharField(max_length=100, blank=True)
    baba_yasiyor = models.BooleanField(default=True)
    baba_oz = models.BooleanField(default=True)
    baba_maas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    evlimi = models.BooleanField(default=True)
    ev_varmi = models.BooleanField(default=True)

    # Foreign Key to Kindergarten
    kres = models.ForeignKey('Kres', related_name='students', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.isim} - {self.tc_no}"

    def yas(self):
        from datetime import date
        return date.today().year - self.dogum_tarihi.year - (
                    (date.today().month, date.today().day) < (self.dogum_tarihi.month, self.dogum_tarihi.day))

    def calculate_points(self):
        points = 0

        yas = self.yas()
        if yas < 3 or yas > 6:
            self.elendi = True
            self.save()
            return "Elendi"
        if 'Atakum' in self.adres:
            points += 5
        if not self.tuvalet_egitimi:
            self.elendi = True
            self.save()
            return "Elendi"
        if self.okul_tecrubesi == 'Devlet':
            points += 5
        if 'Atakum Belediyesi' in self.anne_kurum or 'Atakum Belediyesi' in self.baba_kurum:
            points += 5
        if not self.anne_yasiyor:
            points += 5
        if not self.baba_yasiyor:
            points += 5
        if not self.evlimi:
            points += 5
        if not self.ev_varmi:
            points += 5
        total_salary = (self.anne_maas or 0) + (self.baba_maas or 0)
        if total_salary < 18000:
            points += 20
        elif 18000 <= total_salary < 35000:
            points += 15
        elif 35000 <= total_salary < 53000:
            points += 10
        elif 53000 <= total_salary < 67000:
            points += 5

        points += self.kardes_sayisi

        return points


class Sınıf(models.Model):
    isim = models.CharField(max_length=100)
    kres = models.ForeignKey('Kres', related_name='kres_siniflar', on_delete=models.CASCADE)
    yas_grubu = models.IntegerField()
    ilk_yari = models.BooleanField(default=True)
    students = models.ManyToManyField('Ogrenci', related_name='sinif_students', blank=True)

    def bosluk_varmi(self):
        return self.students.count() < self.kres.toplam_ogrenci_limit / 5

    @property
    def student_count(self):
        return self.students.count()

    def __str__(self):
        return f"{self.isim} - {self.kres.kres_ismi}"


@receiver(post_save, sender=Kres)
def create_siniflar_for_kres(sender, instance, created, **kwargs):
    if created:
        # Create classes based on the number of classes specified in the Kres
        total_classes = instance.siniflar

        for yas in range(3, 6):
            # Determine how many classes should be created for each age group
            classes_per_age_group = total_classes // 4  # Assuming 4 age groups

            for i in range(classes_per_age_group):
                # Create a class for the first half of the year
                Sınıf.objects.create(
                    isim=f"{instance.kres_ismi} - {yas} Yaş İlk Yarı {i + 1}",
                    kres=instance,
                    yas_grubu=yas,
                    ilk_yari=True
                )
                # Create a class for the second half of the year
                Sınıf.objects.create(
                    isim=f"{instance.kres_ismi} - {yas} Yaş İkinci Yarı {i + 1}",
                    kres=instance,
                    yas_grubu=yas,
                    ilk_yari=False
               )
