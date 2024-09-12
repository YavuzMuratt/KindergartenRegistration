import openpyxl
from django.contrib import admin
from django.http import HttpResponse

from .models import Ogrenci, Kres, Sınıf
from .forms import SınıfAdminForm  # Import the custom form for Sınıf


class StudentInline(admin.StackedInline):
    model = Ogrenci
    extra = 0
    fk_name = 'kres'
    fields = ('isim', 'tc_no', 'kres', 'points_display')  # Ya da tercih_edilen_okul
    readonly_fields = ('points_display',)

    def points_display(self, obj):
        return obj.calculate_points()

    points_display.short_description = 'Points'


class KindergartenAdmin(admin.ModelAdmin):
    list_display = ('kres_ismi', 'siniflar', 'sinif_basi_ogrenci', 'student_count')  # Adjust as needed
    inlines = [StudentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Prefetch students related to each kindergarten
        queryset = queryset.prefetch_related('students')
        return queryset

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = 'Number of Students'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('isim', 'tc_no', 'kres', 'adres', 'points_display')
    list_filter = ('kres',)  # Ya da tercih_edilen_okul
    search_fields = ('isim', 'tc_no', 'adres')
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        # Excel dosyasını oluştur
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Öğrenciler"

        # Başlık satırlarını yaz
        ws.append(['İsim', 'Puan', 'Kres', ])

        # Öğrenci verilerini yaz
        for ogrenci in queryset:
            kres_ismi = ogrenci.kres.kres_ismi if ogrenci.kres else 'Belirtilmemiş'
            ws.append([ogrenci.isim,ogrenci.tc_no, ogrenci.calculate_points(), kres_ismi,ogrenci.anne_isim, ogrenci.anne_meslek,ogrenci.anne_egitim,ogrenci.baba_isim,ogrenci.baba_meslek])

        # HTTPResponse ile dosyayı döndür
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="ogrenciler.xlsx"'
        wb.save(response)
        return response

    export_to_excel.short_description = 'Excel olarak dışa aktar'

    def points_display(self, obj):
        return obj.calculate_points()

    points_display.short_description = 'Points'


class OgrenciInline(admin.TabularInline):
    model = Sınıf.students.through
    extra = 0
    can_delete = True
    verbose_name = 'Student'
    verbose_name_plural = 'Students'


class SınıfAdmin(admin.ModelAdmin):
    #form = SınıfAdminForm
    list_display = ('isim', 'kres', 'student_count')
    filter_horizontal = ('students',)
    inlines = [OgrenciInline]

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = 'Student Count'


admin.site.register(Kres, KindergartenAdmin)
admin.site.register(Ogrenci, StudentAdmin)
admin.site.register(Sınıf, SınıfAdmin)
