# views.py
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentForm, AssignmentForm
from .models import Ogrenci, Kres


@staff_member_required
def atama(request):
    students = Ogrenci.objects.filter(tuvalet_egitimi=True, elendi=False, kres__isnull=True)
    reserve_list = []

    students_with_points = []
    for student in students:
        points = student.calculate_points()
        if points != "Elendi":
            students_with_points.append((student, points))

    students_with_points.sort(key=lambda x: x[1], reverse=True)
    kindergartens = Kres.objects.all()

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Atama işlemini yap
            for student, _ in students_with_points:
                yas = student.yas()
                ilk_yari = student.dogum_tarihi.month <= 6
                assigned = False

                # Try assigning to the student's preferred kindergarten (tercih_edilen_okul)
                if student.tercih_edilen_okul:
                    sinif = student.tercih_edilen_okul.kres_siniflar.filter(yas_grubu=yas, ilk_yari=ilk_yari).first()
                    if sinif and sinif.bosluk_varmi():
                        student.kres = student.tercih_edilen_okul
                        student.sinif = sinif
                        student.save()
                        assigned = True

                # If not assigned, try other available kindergartens
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

            for student in reserve_list:
                student.yedekte = True
                student.save()

            messages.success(request, 'Öğrenciler başarıyla atanmıştır.')
            return redirect('atama')
    else:
        form = AssignmentForm()

    context = {
        'students_with_points': students_with_points,
        'kindergartens': kindergartens,
        'reserve_list': reserve_list,
        'form': form,
    }
    return render(request, 'assignment.html', context)

def show_kres(request):
    kresler = Kres.objects.all()  # Kres modelindeki tüm kayıtları al
    return render(request, 'index.html', {'kresler': kresler})

from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentForm

@csrf_exempt
def ogrenci_kayit(request):
    if request.method == 'POST':
        dogum_tarihi_str = request.POST.get('dogum_tarihi')  # 'YYYY-MM-DD' format from the date input
        if dogum_tarihi_str:
            try:
                dogum_tarihi = datetime.strptime(dogum_tarihi_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please check your input.')
                return redirect('index')
        else:
            messages.error(request, 'Please provide a valid date.')
            return redirect('index')

        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.dogum_tarihi = dogum_tarihi
            student.save()
            points = student.calculate_points()
            if points != "Elendi":
                student.points = points
                student.save()
            messages.success(request, 'Student successfully saved.')
            return redirect('success')
        else:
            # Log detailed form errors
            for field, errors in form.errors.items():
                print(f"Error in {field}: {errors}")
                messages.error(request, f"Error in {field}: {errors}")
            messages.error(request, 'Form is not valid. Please check your inputs.')

    else:
        form = StudentForm()

    return render(request, 'index.html', {'form': form})


def success(request):
    return render(request, 'success.html')
