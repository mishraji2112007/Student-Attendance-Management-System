from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import UserProfile,Teacher,Student,Subject
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        a,_=User.objects.get_or_create(username='admin'); a.is_staff=True; a.is_superuser=True; a.set_password('Admin@123'); a.save()
        tu,_=User.objects.get_or_create(username='teacher1'); tu.first_name='Rahul'; tu.last_name='Sharma'; tu.email='teacher@example.com'; tu.set_password('Teacher@123'); tu.save(); UserProfile.objects.update_or_create(user=tu,defaults={'role':'TEACHER'})
        t,_=Teacher.objects.get_or_create(teacher_id='T001',defaults={'user':tu}); t.user=tu; t.department='Computer Science'; t.phone='9876543210'; t.save()
        su,_=User.objects.get_or_create(username='student1'); su.first_name='Aayush'; su.last_name='Mishra'; su.email='student@example.com'; su.set_password('Student@123'); su.save(); UserProfile.objects.update_or_create(user=su,defaults={'role':'STUDENT'})
        s,_=Student.objects.get_or_create(student_id='S001',defaults={'user':su,'roll_number':'101','course':'BCA','semester':1,'section':'A'}); s.user=su; s.roll_number='101'; s.course='BCA'; s.semester=1; s.section='A'; s.save()
        sub,_=Subject.objects.get_or_create(subject_code='BCA101',defaults={'subject_name':'Python Programming','teacher':t,'course':'BCA','semester':1}); sub.teacher=t; sub.save()
        self.stdout.write(self.style.SUCCESS('Demo data created.')); self.stdout.write('Admin: admin / Admin@123'); self.stdout.write('Teacher: teacher1 / Teacher@123'); self.stdout.write('Student: student1 / Student@123')
