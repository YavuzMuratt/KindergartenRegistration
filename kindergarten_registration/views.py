# views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Ogrenci, Kres


@staff_member_required
def atama(request):
    students = Ogrenci.objects.filter(tuvalet_egitimi=True, elendi=False)
    reserve_list = []

    students_with_points = []
    for student in students:
        points = student.calculate_points()
        if points != "Elendi":
            students_with_points.append((student, points))

    students_with_points.sort(key=lambda x: x[1], reverse=True)
    kindergartens = Kres.objects.all()

    if request.method == 'POST':
        for student, _ in students_with_points:
            yas = student.yas()
            ilk_yari = student.dogum_tarihi.month <= 6
            assigned = False

            if student.tercih_edilen_okul:
                sinif = student.tercih_edilen_okul.kres_siniflar.filter(yas_grubu=yas, ilk_yari=ilk_yari).first()
                if sinif and sinif.bosluk_varmi():
                    student.kres = student.tercih_edilen_okul
                    student.sinif = sinif
                    student.save()
                    assigned = True

            if not assigned:
                for kindergarten in kindergartens:
                    sinif = kindergarten.kres_siniflar.filter(yas_grubu=yas, ilk_yari=ilk_yari).first()
                    if sinif and sinif.bosluk_varmi():
                        student.kres = kindergarten
                        student.sinif = sinif
                        student.save()
                        assigned = True
                        break

            if not assigned:
                reserve_list.append(student)

        # Save reserve list
        for student in reserve_list:
            student.yedekte = True
            student.save()

        return redirect('atama')

    context = {
        'students_with_points': students_with_points,
        'kindergartens': kindergartens,
        'reserve_list': reserve_list,
    }
    return render(request, 'assignment.html', context)


def ogrenci_kayit(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            points = student.calculate_points()
            if points != "Elendi":
                student.points = points
                student.save()
            messages.success(request, 'Student successfully saved.')
            return redirect('success')
        else:
            messages.error(request, 'Form is not valid. Please check your inputs.')
    else:
        form = StudentForm()

    return render(request, 'register_student.html', {'form': form})


def success(request):
    return render(request, 'success.html')
