from django.contrib import admin
from .models import Attendance,Student,Subject,Teacher,UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin): list_display=('user','role'); list_filter=('role',)
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin): list_display=('teacher_id','user','department','phone'); search_fields=('teacher_id','user__username','user__first_name','user__last_name')
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin): list_display=('student_id','roll_number','user','course','semester','section'); search_fields=('student_id','roll_number','user__username','user__first_name','user__last_name')
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin): list_display=('subject_code','subject_name','teacher','course','semester'); search_fields=('subject_code','subject_name','course')
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin): list_display=('student','subject','date','status','marked_by','marked_at'); list_filter=('status','subject','date'); search_fields=('student__roll_number','student__user__first_name','subject__subject_name'); date_hierarchy='date'
