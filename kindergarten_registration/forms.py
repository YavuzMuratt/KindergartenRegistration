# forms.py
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'preferred_kindergarten_1', 'preferred_kindergarten_2', 'preferred_kindergarten_3',
            'name', 'tc_number', 'birth_date', 'address', 'toilet_trained', 'school_experience',
            'school_type', 'sibling_count', 'mother_alive', 'mother_name', 'mother_phone',
            'mother_education', 'mother_job', 'mother_employer', 'mother_salary',
            'father_alive', 'father_name', 'father_phone', 'father_education', 'father_job',
            'father_employer', 'father_salary', 'owns_house', 'marital_status'
        ]

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        school_experience = cleaned_data.get("school_experience")
        school_type = cleaned_data.get("school_type")
        if not school_experience:
            cleaned_data["school_type"] = None
        mother_alive = cleaned_data.get("mother_alive")
        if not mother_alive:
            cleaned_data["mother_name"] = None
            cleaned_data["mother_phone"] = None
            cleaned_data["mother_education"] = None
            cleaned_data["mother_job"] = None
            cleaned_data["mother_employer"] = None
            cleaned_data["mother_salary"] = 0
        father_alive = cleaned_data.get("father_alive")
        if not father_alive:
            cleaned_data["father_name"] = None
            cleaned_data["father_phone"] = None
            cleaned_data["father_education"] = None
            cleaned_data["father_job"] = None
            cleaned_data["father_employer"] = None
            cleaned_data["father_salary"] = 0
        return cleaned_data
