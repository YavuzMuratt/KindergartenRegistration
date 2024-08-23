from django import forms
from .models import Ogrenci, Kres, Sınıf
from django.core.exceptions import ValidationError


class StudentForm(forms.ModelForm):
    OKUL_TIPLERI = [
        ('None', 'Yok'),
        ('Devlet', 'Devlet'),
        ('Özel', 'Özel'),
    ]
    KURUMLAR = [
        ('None', 'Seçiniz'),
        ('Atakum Belediyesi', 'Atakum Belediyesi'),
        ('Diğer', 'Diğer'),
    ]
    #anne_kurum = forms.ChoiceField(choices=KURUMLAR, required=True)
    #baba_kurum = forms.ChoiceField(choices=KURUMLAR, required=True)
    #diger_kurum = forms.CharField(required=False)
    okul_tecrubesi = forms.ChoiceField(choices=OKUL_TIPLERI, required=False, widget=forms.Select())

    preferred_kindergarten = forms.ModelChoiceField(
        queryset=Kres.objects.all(),
        required=False,
        label="Tercih Edilen Anaokulu"
    )

    preferred_kindergarten = forms.ModelChoiceField(
        queryset=Kres.objects.all(),
        required=False,
        label="Tercih Edilen Anaokulu"
    )

    kres = forms.ModelChoiceField(queryset=Kres.objects.all(), required=True, widget=forms.Select())
    def clean(self):
        cleaned_data = super().clean()
        kurum = cleaned_data.get('kurum')
        diger_kurum = cleaned_data.get('diger_kurum')


        if kurum == 'Diğer' and not diger_kurum:
            raise ValidationError("Diğer Kurum'u seçtiyseniz, lütfen alanı doldurunuz.")

        return cleaned_data

    class Meta:
        model = Ogrenci
        fields = [
            'isim', 'soyisim', 'tc_no', 'adres', 'tuvalet_egitimi', 'okul_tecrubesi', 'devlet_ozel',
            'kardes_sayisi', 'dogum_tarihi',
            'anne_isim', 'anne_soyisim', 'anne_telefon', 'anne_egitim', 'anne_meslek','anne_kurum', 'anne_yasiyor',
            'anne_oz', 'anne_maas', 'baba_isim', 'baba_soyisim', 'baba_telefon',
            'baba_egitim', 'baba_meslek', 'baba_kurum', 'baba_yasiyor', 'baba_oz',
            'baba_maas', 'evlimi', 'ev_varmi'
        ]
        widgets = {
            'dogum_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'devlet_ozel': forms.Select(choices=[('Devlet', 'Devlet'), ('Özel', 'Özel')]),
            'tuvalet_egitimi': forms.CheckboxInput(),
            'okul_tecrubesi': forms.Select(),
            'anne_yasiyor': forms.CheckboxInput(),
            'baba_yasiyor': forms.CheckboxInput(),
            'evlimi': forms.Select(),
            'ev_varmi': forms.Select(),
            'kardes_sayisi': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
        }
        labels = {
            'isim': 'Öğrenci Adı',
            'tc_no': 'Öğrenci ID',
            'adres': 'Adres',
            'tuvalet_egitimi': 'Tuvalet Eğitimi',
            'okul_tecrubesi': 'Okul Tecrübesi',
            'devlet_ozel': 'Devlet / Özel',
            'kardes_sayisi': 'Kardeş Sayısı',
            'anne_ismi': 'Anne Adı',
            'anne_telefon': 'Anne Telefonu',
            'anne_egitim': 'Anne Eğitimi',
            'anne_meslek': 'Anne Mesleği',
            'anne_kurum': 'Anne Kurum',
            'anne_yasiyor': 'Anne Yaşıyor',
            'anne_maas': 'Anne Maaşı',
            'baba_isim': 'Baba Adı',
            'baba_telefon': 'Baba Telefonu',
            'baba_egitim': 'Baba Eğitimi',
            'baba_meslek': 'Baba Mesleği',
            'baba_kurum': 'Baba Kurum',
            'baba_yasiyor': 'Baba Yaşıyor',
            'baba_oz': 'Baba Oz',
            'baba_ev_varmi': 'Baba Evi Var mı',
            'evlimi': 'Anne Baba Evli mi',
            'ev_varmi': 'Ev Sahibi misiniz?',
        }
        help_texts = {
            'tuvalet_egitimi': 'Tuvalet eğitimi almış mı?',
            'okul_tecrubesi': 'Okul tecrübesi var mı?',
            'devlet_ozel': 'Okul tipi: Devlet veya Özel',
            'kardes_sayisi': 'Kardeş sayısını belirtin',
            'anne_yasiyor': 'Anne hayatta mı?',
            'anne_ev_varmi': 'Anne kendi evi var mı?',
            'anne_evlimi': 'Anne evli mi?',
            'baba_yasiyor': 'Baba hayatta mı?',
            'baba_ev_varmi': 'Baba kendi evi var mı?',
            'baba_evlimi': 'Baba evli mi?',
        }


class SınıfAdminForm(forms.ModelForm):
    class Meta:
        model = Sınıf
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict students to those in the same Kres
        if self.instance and self.instance.kres:
            self.fields['students'].queryset = Ogrenci.objects.filter(kres=self.instance.kres)
        else:
            self.fields['students'].queryset = Ogrenci.objects.none()