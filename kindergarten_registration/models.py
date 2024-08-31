# models.py
from django.db import models
from django.utils import timezone

class Kindergarten(models.Model):
    name = models.CharField(max_length=255)
    student_limit = models.PositiveIntegerField()
    num_classes = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Class(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, related_name='classes')
    limit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kindergarten.name} - Sınıf {self.id}"

class Student(models.Model):
    # Student Info
    preferred_kindergarten_1 = models.ForeignKey(Kindergarten, on_delete=models.SET_NULL, null=True, related_name='preferred_1')
    preferred_kindergarten_2 = models.ForeignKey(Kindergarten, on_delete=models.SET_NULL, null=True, related_name='preferred_2', blank=True)
    preferred_kindergarten_3 = models.ForeignKey(Kindergarten, on_delete=models.SET_NULL, null=True, related_name='preferred_3', blank=True)
    name = models.CharField(max_length=64)
    tc_number = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
    address = models.CharField(max_length=500)
    toilet_trained = models.BooleanField(default=False)
    school_experience = models.BooleanField(default=False)
    school_type = models.CharField(max_length=20, choices=[('Devlet', 'Devlet'), ('Özel', 'Özel')], blank=True, null=True)
    sibling_count = models.PositiveIntegerField(default=0)

    # Parent Info
    mother_alive = models.BooleanField(default=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_phone = models.CharField(max_length=10, blank=True, null=True)
    mother_education = models.CharField(max_length=100, blank=True, null=True)
    mother_job = models.CharField(max_length=100, blank=True, null=True)
    mother_employer = models.CharField(max_length=255, blank=True, null=True)
    mother_salary = models.PositiveIntegerField(default=0, blank=True, null=True)

    father_alive = models.BooleanField(default=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_phone = models.CharField(max_length=10, blank=True, null=True)
    father_education = models.CharField(max_length=100, blank=True, null=True)
    father_job = models.CharField(max_length=100, blank=True, null=True)
    father_employer = models.CharField(max_length=255, blank=True, null=True)
    father_salary = models.PositiveIntegerField(default=0, blank=True, null=True)

    # Shared Parent Info
    owns_house = models.BooleanField(default=True)
    marital_status = models.CharField(max_length=10, choices=[('Birlikte', 'Birlikte'), ('Ayrı', 'Ayrı')])

    # Registration Info
    registration_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    disqualified = models.BooleanField(default=False)
    assigned_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_points(self):
        points = 0
        current_year = timezone.now().year
        age = current_year - self.birth_date.year

        print(f"Calculating points for student: {self.name}")
        print(f"Student age: {age}")

        if age > 6 or age < 3:
            self.disqualified = True
            self.save()
            print("Disqualified: Age issue")
            return 'Elendi'

        if 'Atakum' in self.address:
            points += 5
            print("Points for address: +5")

        if not self.toilet_trained:
            self.disqualified = True
            self.save()
            print("Disqualified: Toilet training issue")
            return 'Elendi'

        points += self.sibling_count
        print(f"Points for sibling count: +{self.sibling_count}")

        if self.school_experience and self.school_type == 'Devlet':
            points += 5
            print("Points for school experience: +5")

        if 'Atakum Bel' in (self.mother_employer or '') or 'Atakum Bel' in (self.father_employer or ''):
            points += 5
            print("Points for employer: +5")

        if not self.mother_alive:
            points += 5
            print("Points for mother not alive: +5")

        if not self.father_alive:
            points += 5
            print("Points for father not alive: +5")

        if not self.owns_house:
            points += 5
            print("Points for not owning house: +5")

        if self.marital_status == 'Ayrı':
            points += 5
            print("Points for marital status: +5")

        mother_salary = self.mother_salary if self.mother_salary is not None else 0
        father_salary = self.father_salary if self.father_salary is not None else 0
        total_salary = mother_salary + father_salary
        print(f"Total salary: {total_salary}")

        if total_salary < 17000:
            points += 20
            print("Points for salary < 17000: +20")
        elif total_salary < 35000:
            points += 15
            print("Points for salary < 35000: +15")
        elif total_salary < 53000:
            points += 10
            print("Points for salary < 53000: +10")
        elif total_salary < 67000:
            points += 5
            print("Points for salary < 67000: +5")

        print(f"Total calculated points: {points}")
        self.points = points
        self.save()
        print(f"Points saved: {self.points}")

        return self.points

    def __str__(self):
        return self.name
