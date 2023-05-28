import random
import string
from django.core.mail import send_mail


class MailSender:
    _link = 'https://www.analyticsassistant.kz/confirm'
    link = f'\nСсылка на страницу активации аккаунта: \n {_link}'
    activation_message = 'Вы получили это письмо, потому что вам нужно завершить процесс активации учетной записи. Ваш код активации: \n\n'
    reset_password_message = 'Вы получили это письмо, потому что вы отправили запрос на восстановление пароля. Обязательно установите свой новый пароль в вашем личном кабинете! Ваш новый пароль: \n\n'
    new_employee_message = 'Вы получили это письмо, потому что вас добавлили в список сотрудников. Обязательно установите свой новый пароль в вашем личном кабинете! Ваш пароль: \n\n'

    def send_activation_mail(
        self,
        verification_code: str,
        recipient: str
    ):
        send_mail(
            'Активация аккаунта',
            self.activation_message + f'{verification_code}' + self.link,
            'analyte001@mail.ru',
            [f'{recipient}'],
            fail_silently=False
        )

    def send_reset_password_mail(
        self,
        new_password: str,
        recipient: str
    ):
        send_mail(
            'Восстановление пароля',
            self.reset_password_message + f'{new_password}',
            'analyte001@mail.ru',
            [f'{recipient}'],
            fail_silently=False
        )

    def send_password_to_employee_mail(
        self,
        new_password: str,
        recipient: str
    ):
        send_mail(
            'Новый аккаунт работника',
            self.new_employee_message + f'{new_password}',
            'analyte001@mail.ru',
            [f'{recipient}'],
            fail_silently=False
        )


def verification_code_generator() -> str:
    code = ''

    while len(code) != 8:
        code += random.choice(string.ascii_letters) + str(random.randint(0, 9))

    return code


def new_password_generator() -> str:
    new_password = ''

    while len(new_password) != 16:
        new_password += random.choice(string.ascii_letters) + str(random.randint(0, 9))

    return new_password
