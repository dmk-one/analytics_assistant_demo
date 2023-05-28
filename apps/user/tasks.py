from celery import shared_task


from apps.user.models import UserVerificationCode, User
from apps.user.utils import verification_code_generator, MailSender


@shared_task
def create_verif_code_and_send_mail(
    user_obj_id: int
):
    user = User.objects.filter(id=user_obj_id).first()

    user_verification_object = UserVerificationCode.objects.create(
        user=user,
        code=verification_code_generator()
    )

    MailSender().send_activation_mail(
        verification_code=user_verification_object.code,
        recipient=user_verification_object.user.email
    )

@shared_task
def send_password_to_employee_mail(
    new_password: str,
    recipient_email: str
):
    MailSender().send_password_to_employee_mail(
        new_password=new_password,
        recipient=recipient_email
    )
