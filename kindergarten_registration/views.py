# views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Ogrenci, Kres


@staff_member_required
def atama(request):
    students = Ogrenci.objects.filter(tuvalet_egitimi=True)

    students_with_points = []
    for student in students:
        points = student.calculate_points()
        if points != "Elendi":
            students_with_points.append((student, points))

    # Sort students by points in descending order
    students_with_points.sort(key=lambda x: x[1], reverse=True)

    kindergartens = Kres.objects.all()

    if request.method == 'POST':
        for student, _ in students_with_points:
            assigned = False

            # Check if the student has a preferred kindergarten
            if student.tercih_edilen_okul and student.tercih_edilen_okul.bosluk_varmi():
                student.kres = student.tercih_edilen_okul
                student.save()
                assigned = True

            # If not assigned or no preferred kindergarten, assign to any available kindergarten
            if not assigned:
                for kindergarten in kindergartens:
                    if kindergarten.bosluk_varmi():
                        student.kres = kindergarten
                        student.save()
                        break

        return redirect('atama')

    context = {
        'students_with_points': students_with_points,
        'kindergartens': kindergartens
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
