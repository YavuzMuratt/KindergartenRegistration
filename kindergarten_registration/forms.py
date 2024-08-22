from django import forms
from .models import Ogrenci, Kres, Sınıf


class StudentForm(forms.ModelForm):
    OKUL_TIPLERI = [
        ('None', 'Yok'),
        ('Devlet', 'Devlet'),
        ('Özel', 'Özel'),
    ]

    okul_tecrubesi = forms.ChoiceField(choices=OKUL_TIPLERI, required=False, widget=forms.Select())

    preferred_kindergarten = forms.ModelChoiceField(
        queryset=Kres.objects.all(),
        required=False,
        label="Tercih Edilen Anaokulu"
    )

    class Meta:
        model = Ogrenci
        fields = [
            'isim', 'tc_no', 'adres', 'tuvalet_egitimi', 'okul_tecrubesi', 'devlet_ozel',
            'kardes_sayisi', 'dogum_tarihi',
            'anne_ismi', 'anne_telefon', 'anne_egitim', 'anne_meslek', 'anne_yasiyor',
            'anne_ev_varmi', 'anne_evlimi', 'anne_maas', 'baba_isim', 'baba_telefon',
            'baba_egitim', 'baba_meslek', 'baba_yasiyor', 'baba_ev_varmi', 'baba_evlimi',
            'baba_maas'
        ]
        widgets = {
            'dogum_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'devlet_ozel': forms.Select(choices=[('Devlet', 'Devlet'), ('Özel', 'Özel')]),
            'tuvalet_egitimi': forms.CheckboxInput(),
            'okul_tecrubesi': forms.Select(),
            'anne_yasiyor': forms.CheckboxInput(),
            'anne_ev_varmi': forms.CheckboxInput(),
            'anne_evlimi': forms.CheckboxInput(),
            'baba_yasiyor': forms.CheckboxInput(),
            'baba_ev_varmi': forms.CheckboxInput(),
            'baba_evlimi': forms.CheckboxInput(),
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
            'anne_yasiyor': 'Anne Yaşıyor',
            'anne_ev_varmi': 'Anne Evi Var mı',
            'anne_evlimi': 'Anne Evli mi',
            'anne_maas': 'Anne Maaşı',
            'baba_isim': 'Baba Adı',
            'baba_telefon': 'Baba Telefonu',
            'baba_egitim': 'Baba Eğitimi',
            'baba_meslek': 'Baba Mesleği',
            'baba_yasiyor': 'Baba Yaşıyor',
            'baba_ev_varmi': 'Baba Evi Var mı',
            'baba_evlimi': 'Baba Evli mi',
            'baba_maas': 'Baba Maaşı',
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