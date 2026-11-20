
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student


# HOME PAGE
def home(request):
    students = Student.objects.all()

    course = request.GET.get('course')
    semester = request.GET.get('semester')

    if course:
        students = students.filter(course=course)

    if semester:
        students = students.filter(semester=semester)

    all_students = Student.objects.all()

    total_students = all_students.count()
    total_courses = all_students.values('course').distinct().count()
    total_semesters = all_students.values('semester').distinct().count()

    courses = Student.objects.values_list(
        'course', flat=True
    ).distinct()

    semesters = Student.objects.values_list(
        'semester', flat=True
    ).distinct().order_by('semester')

    return render(request, 'students/home.html', {
        'students': students,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_semesters': total_semesters,
        'courses': courses,
        'semesters': semesters,
    })


# ADD STUDENT
def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            usn=request.POST['usn'],
            email=request.POST['email'],
            course=request.POST['course'],
            semester=request.POST['semester']
        )
        return redirect('home')

    return render(request, 'students/add.html')


# EDIT STUDENT
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.usn = request.POST['usn']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.semester = request.POST['semester']
        student.save()

        return redirect('home')

    return render(request, 'students/add.html', {'student': student})


# DELETE STUDENT
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()

    return redirect('home')


# STUDENT PROFILE
def student_profile(request, id):
    student = get_object_or_404(Student, id=id)

    return render(request, 'students/profile.html', {
        'student': student
    })
# ATTENDANCE MANAGEMENT
from .models import Attendance
from django.utils import timezone


def attendance(request):
    students = Student.objects.all()
    today = timezone.localdate()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')

        student = get_object_or_404(Student, id=student_id)

        if status in ['Present', 'Absent', 'Late']:
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={'status': status}
            )

        return redirect('attendance')

    records = Attendance.objects.filter(date=today).select_related('student')

    present_count = records.filter(status='Present').count()
    absent_count = records.filter(status='Absent').count()
    late_count = records.filter(status='Late').count()

    return render(request, 'students/attendance.html', {
        'students': students,
        'records': records,
        'today': today,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
    })