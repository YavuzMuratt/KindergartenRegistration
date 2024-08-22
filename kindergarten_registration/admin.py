from django.contrib import admin
from .models import Ogrenci, Kres, Sınıf


class StudentInline(admin.StackedInline):
    model = Ogrenci
    extra = 0  # Number of empty forms to display
    fields = ('isim', 'tc_no', 'kres', 'points_display')  # List fields in desired order
    readonly_fields = ('points_display',)  # Make points_display read-only
    fk_name = 'kres'

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
    list_filter = ('kres',)  # Allow filtering by kindergarten
    search_fields = ('isim', 'tc_no', 'adres')  # Add search functionality

    def points_display(self, obj):
        return obj.calculate_points()
    points_display.short_description = 'Points'


class SınıfAdmin(admin.ModelAdmin):
    list_display = ('isim', 'kres', 'yas_grubu', 'ilk_yari', 'student_count')
    filter_horizontal = ('students',)

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = 'Student Count'


admin.site.register(Kres, KindergartenAdmin)
admin.site.register(Ogrenci, StudentAdmin)
admin.site.register(Sınıf)