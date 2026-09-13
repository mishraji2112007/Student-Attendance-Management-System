from django.contrib.auth.models import User
from django.db import models
class UserProfile(models.Model):
    ROLE_CHOICES=[('TEACHER','Teacher'),('STUDENT','Student')]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    def __str__(self): return f'{self.user.username} - {self.role}'
class Teacher(models.Model):
    teacher_id=models.CharField(max_length=30,unique=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher')
    phone=models.CharField(max_length=20,blank=True)
    department=models.CharField(max_length=100,blank=True)
    def __str__(self): return f'{self.teacher_id} - {self.user.get_full_name() or self.user.username}'
class Student(models.Model):
    student_id=models.CharField(max_length=30,unique=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')
    roll_number=models.CharField(max_length=30,unique=True)
    phone=models.CharField(max_length=20,blank=True)
    course=models.CharField(max_length=100)
    semester=models.PositiveIntegerField(default=1)
    section=models.CharField(max_length=20,default='A')
    def __str__(self): return f'{self.roll_number} - {self.user.get_full_name() or self.user.username}'
class Subject(models.Model):
    subject_code=models.CharField(max_length=30,unique=True)
    subject_name=models.CharField(max_length=100)
    teacher=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,related_name='subjects')
    course=models.CharField(max_length=100)
    semester=models.PositiveIntegerField(default=1)
    def __str__(self): return f'{self.subject_code} - {self.subject_name}'
class Attendance(models.Model):
    STATUS_CHOICES=[('P','Present'),('A','Absent')]
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendance_records')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='attendance_records')
    date=models.DateField()
    status=models.CharField(max_length=1,choices=STATUS_CHOICES)
    marked_by=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,related_name='marked_attendance')
    marked_at=models.DateTimeField(auto_now=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['student','subject','date'],name='unique_student_subject_date')]
        ordering=['-date','student__roll_number']
    def __str__(self): return f'{self.student} | {self.subject} | {self.date} | {self.status}'
