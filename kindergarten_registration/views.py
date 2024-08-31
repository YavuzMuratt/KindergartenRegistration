# views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Student, Kindergarten, Class
from .forms import StudentForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class StudentRegistrationView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'student_registration.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.calculate_points()
            student.save()
            return redirect('success')
        return render(request, 'student_registration.html', {'form': form})


class StudentListView(View):
    def get(self, request):
        students = Student.objects.order_by('-points', 'registration_date')
        return render(request, 'student_list.html', {'students': students})


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # Ensure the user is an admin


class AssignmentView(LoginRequiredMixin, AdminRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        return render(request, 'assignment.html')

    def post(self, request):
        students = Student.objects.filter(disqualified=False, assigned_class__isnull=True).order_by('-points',
                                                                                                    'registration_date')

        for student in students:
            assigned = False
            for preferred in ['preferred_kindergarten_1', 'preferred_kindergarten_2', 'preferred_kindergarten_3']:
                kindergarten = getattr(student, preferred)
                if kindergarten and self.assign_to_kindergarten(student, kindergarten):
                    assigned = True
                    break

            if not assigned:
                messages.warning(request, f"Student {student.name} could not be assigned to any kindergarten.")

        self.assign_students_to_classes()
        messages.success(request, "All students have been successfully assigned.")
        return redirect('assignment')

    def assign_to_kindergarten(self, student, kindergarten):
        total_assigned = Student.objects.filter(assigned_class__kindergarten=kindergarten).count()
        if total_assigned < kindergarten.student_limit:
            self.assign_student_to_kindergarten(student, kindergarten)
            return True
        return False

    def assign_student_to_kindergarten(self, student, kindergarten):
        classes = Class.objects.filter(kindergarten=kindergarten)
        if classes.exists():
            student.assigned_class = classes.first()
            student.save()

    def assign_students_to_classes(self):
        kindergartens = Kindergarten.objects.all()
        for kindergarten in kindergartens:
            students = Student.objects.filter(assigned_class__kindergarten=kindergarten).order_by('birth_date')
            classes = kindergarten.classes.all()

            class_index = 0
            for student in students:
                assigned_class = classes[class_index]
                student.assigned_class = assigned_class
                student.save()

                if Student.objects.filter(assigned_class=assigned_class).count() >= assigned_class.limit:
                    class_index += 1
                    if class_index >= len(classes):
                        break


class SuccessView(View):
    def get(self, request):
        return render(request, 'registration_success.html')