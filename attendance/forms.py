from django import forms
from django.contrib.auth.models import User
from .models import Attendance,Student,Subject,Teacher
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
class StudentForm(forms.ModelForm):
    first_name=forms.CharField(); last_name=forms.CharField(required=False); email=forms.EmailField(required=False); username=forms.CharField(); password=forms.CharField(required=False,widget=forms.PasswordInput)
    class Meta: model=Student; fields=['student_id','roll_number','course','semester','section','phone']
    def save(self,commit=True):
        obj=super().save(commit=False); user=obj.user if obj.pk else User(); user.username=self.cleaned_data['username']; user.first_name=self.cleaned_data['first_name']; user.last_name=self.cleaned_data['last_name']; user.email=self.cleaned_data['email'];
        if self.cleaned_data['password']: user.set_password(self.cleaned_data['password'])
        if commit: user.save(); obj.user=user; obj.save()
        return obj
class TeacherForm(forms.ModelForm):
    first_name=forms.CharField(); last_name=forms.CharField(required=False); email=forms.EmailField(required=False); username=forms.CharField(); password=forms.CharField(required=False,widget=forms.PasswordInput)
    class Meta: model=Teacher; fields=['teacher_id','department','phone']
    def save(self,commit=True):
        obj=super().save(commit=False); user=obj.user if obj.pk else User(); user.username=self.cleaned_data['username']; user.first_name=self.cleaned_data['first_name']; user.last_name=self.cleaned_data['last_name']; user.email=self.cleaned_data['email'];
        if self.cleaned_data['password']: user.set_password(self.cleaned_data['password'])
        if commit: user.save(); obj.user=user; obj.save()
        return obj
class SubjectForm(forms.ModelForm):
    class Meta: model=Subject; fields=['subject_code','subject_name','teacher','course','semester']
class AttendanceMarkForm(forms.Form):
    date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    subject=forms.ModelChoiceField(queryset=Subject.objects.none())
    def __init__(self,*args,teacher=None,**kwargs):
        super().__init__(*args,**kwargs); self.fields['subject'].queryset=Subject.objects.filter(teacher=teacher) if teacher else Subject.objects.none()
