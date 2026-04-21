from django import forms
from . import mongo


def course_choices():
    return [(str(c['_id']), f"{c['code']} - {c['name']}")
            for c in mongo.courses().find().sort('code', 1)]


class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    courses = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].choices = course_choices()

    def clean_email(self):
        email = self.cleaned_data['email']
        if mongo.students().find_one({'email': email}):
            raise forms.ValidationError('A student with this email already exists.')
        return email


class CourseForm(forms.Form):
    code = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_code(self):
        code = self.cleaned_data['code']
        if mongo.courses().find_one({'code': code}):
            raise forms.ValidationError('A course with this code already exists.')
        return code
