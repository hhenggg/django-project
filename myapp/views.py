from django.shortcuts import render, redirect
from bson import ObjectId
from .forms import StudentForm, CourseForm
from . import mongo


def home(request):
    return render(request, 'myapp/home.html')


def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            mongo.students().insert_one({
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'course_ids': [ObjectId(cid) for cid in data['courses']],
            })
            return redirect('report')
    else:
        form = StudentForm()
    return render(request, 'myapp/student_form.html', {'form': form})


def course_register(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            mongo.courses().insert_one(form.cleaned_data)
            return redirect('report')
    else:
        form = CourseForm()
    return render(request, 'myapp/course_form.html', {'form': form})


def report(request):
    course_list = list(mongo.courses().find().sort('code', 1))
    for c in course_list:
        c['students'] = list(
            mongo.students().find({'course_ids': c['_id']}).sort('last_name', 1)
        )
    return render(request, 'myapp/report.html', {'courses': course_list})
