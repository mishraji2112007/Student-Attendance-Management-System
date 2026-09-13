from datetime import date
from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404,redirect,render
from .forms import AttendanceMarkForm,LoginForm,StudentForm,SubjectForm,TeacherForm
from .models import Attendance,Student,Subject,Teacher

def role_required(*roles):
    def deco(view):
        @wraps(view)
        @login_required
        def wrap(request,*args,**kwargs):
            if request.user.is_superuser: return view(request,*args,**kwargs)
            p=getattr(request.user,'profile',None)
            if not p or p.role not in roles: messages.error(request,'You are not authorized to access this page.'); return redirect('dashboard')
            return view(request,*args,**kwargs)
        return wrap
    return deco

def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    form=LoginForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user: login(request,user); return redirect('dashboard')
        messages.error(request,'Invalid username or password.')
    return render(request,'attendance/login.html',{'form':form})
@login_required
def logout_view(request): logout(request); return redirect('login')
@login_required
def dashboard(request):
    if request.user.is_superuser: return render(request,'attendance/admin_dashboard.html',{'students_count':Student.objects.count(),'teachers_count':Teacher.objects.count(),'subjects_count':Subject.objects.count(),'attendance_count':Attendance.objects.count()})
    p=getattr(request.user,'profile',None)
    if p and p.role=='TEACHER':
        t=request.user.teacher; return render(request,'attendance/teacher_dashboard.html',{'teacher':t,'subjects':Subject.objects.filter(teacher=t),'students_count':Student.objects.count()})
    s=request.user.student; records=Attendance.objects.filter(student=s); present=records.filter(status='P').count(); total=records.count(); pct=round(present/total*100,1) if total else 0
    return render(request,'attendance/student_dashboard.html',{'student':s,'present':present,'total':total,'percentage':pct})
@role_required('TEACHER')
def student_list(request): return render(request,'attendance/students.html',{'students':Student.objects.select_related('user')})
@role_required('TEACHER')
def student_add(request):
    form=StudentForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        s=form.save(); from .models import UserProfile; UserProfile.objects.update_or_create(user=s.user,defaults={'role':'STUDENT'}); messages.success(request,'Student added successfully.'); return redirect('student_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Add Student','back':'student_list'})
@role_required('TEACHER')
def student_edit(request,pk):
    s=get_object_or_404(Student,pk=pk); initial={'username':s.user.username,'first_name':s.user.first_name,'last_name':s.user.last_name,'email':s.user.email}; form=StudentForm(request.POST or None,instance=s,initial=initial)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Student updated successfully.'); return redirect('student_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Edit Student','back':'student_list'})
@role_required('TEACHER')
def student_delete(request,pk):
    s=get_object_or_404(Student,pk=pk)
    if request.method=='POST': u=s.user; s.delete(); u.delete(); messages.success(request,'Student deleted successfully.')
    return redirect('student_list')
@role_required('ADMIN')
def teacher_list(request): return render(request,'attendance/teachers.html',{'teachers':Teacher.objects.select_related('user')})
@role_required('ADMIN')
def teacher_add(request):
    form=TeacherForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        t=form.save(); from .models import UserProfile; UserProfile.objects.update_or_create(user=t.user,defaults={'role':'TEACHER'}); messages.success(request,'Teacher added successfully.'); return redirect('teacher_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Add Teacher','back':'teacher_list'})
@role_required('ADMIN')
def teacher_edit(request,pk):
    t=get_object_or_404(Teacher,pk=pk); initial={'username':t.user.username,'first_name':t.user.first_name,'last_name':t.user.last_name,'email':t.user.email}; form=TeacherForm(request.POST or None,instance=t,initial=initial)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Teacher updated successfully.'); return redirect('teacher_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Edit Teacher','back':'teacher_list'})
@role_required('ADMIN')
def teacher_delete(request,pk):
    t=get_object_or_404(Teacher,pk=pk)
    if request.method=='POST': u=t.user; t.delete(); u.delete(); messages.success(request,'Teacher deleted successfully.')
    return redirect('teacher_list')
@role_required('ADMIN')
def subject_list(request): return render(request,'attendance/subjects.html',{'subjects':Subject.objects.select_related('teacher__user')})
@role_required('ADMIN')
def subject_add(request):
    form=SubjectForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Subject added successfully.'); return redirect('subject_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Add Subject','back':'subject_list'})
@role_required('ADMIN')
def subject_edit(request,pk):
    form=SubjectForm(request.POST or None,instance=get_object_or_404(Subject,pk=pk))
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Subject updated successfully.'); return redirect('subject_list')
    return render(request,'attendance/form.html',{'form':form,'title':'Edit Subject','back':'subject_list'})
@role_required('ADMIN')
def subject_delete(request,pk):
    if request.method=='POST': get_object_or_404(Subject,pk=pk).delete(); messages.success(request,'Subject deleted successfully.')
    return redirect('subject_list')
@role_required('TEACHER')
def mark_attendance(request):
    teacher=request.user.teacher; form=AttendanceMarkForm(request.POST or None,teacher=teacher); selected_date=date.today()
    if request.method=='POST' and form.is_valid():
        subject=form.cleaned_data['subject']; selected_date=form.cleaned_data['date']; students=Student.objects.filter(course=subject.course,semester=subject.semester)
        with transaction.atomic():
            for s in students: Attendance.objects.update_or_create(student=s,subject=subject,date=selected_date,defaults={'status':request.POST.get(f'status_{s.pk}','A'),'marked_by':teacher})
        messages.success(request,f'Attendance saved for {subject.subject_name}.'); return redirect('attendance_report')
    return render(request,'attendance/mark_attendance.html',{'form':form,'students':Student.objects.all(),'selected_date':selected_date})
@login_required
def attendance_report(request):
    r=Attendance.objects.select_related('student__user','subject','marked_by__user')
    if request.user.is_superuser: pass
    elif hasattr(request.user,'teacher'): r=r.filter(marked_by=request.user.teacher)
    elif hasattr(request.user,'student'): r=r.filter(student=request.user.student)
    else: r=r.none()
    return render(request,'attendance/report.html',{'records':r[:500]})
@login_required
def my_attendance(request):
    if not hasattr(request.user,'student'): return redirect('dashboard')
    s=request.user.student; records=Attendance.objects.filter(student=s).select_related('subject'); summary=[]
    for sub in Subject.objects.filter(course=s.course,semester=s.semester):
        q=records.filter(subject=sub); total=q.count(); present=q.filter(status='P').count(); summary.append({'subject':sub,'total':total,'present':present,'percentage':round(present/total*100,1) if total else 0})
    return render(request,'attendance/my_attendance.html',{'student':s,'summary':summary,'records':records[:100]})
