from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import TeacherProfile, StudentProfile

@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    is_teacher = request.POST.get('is_teacher') == 'true'
    if is_teacher:
        TeacherProfile.objects.create(user=user)
    else:
        StudentProfile.objects.create(user=user)