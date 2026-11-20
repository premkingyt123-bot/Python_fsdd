from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return self.name


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.status}"