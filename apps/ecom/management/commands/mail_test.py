from django.core.management.base import BaseCommand

from apps.mailersend_utils import send_mailersend_email


class Command(BaseCommand):
    help = 'Send test emails via MailerSend: plain text or template'

    def add_arguments(self, parser):
        parser.add_argument(
            'email_type',
            choices=['text_email', 'template_email'],
            help='Choose email type: text_email or template_email'
        )

    def handle(self, *args, **options):
        email_type = options['email_type']

        if email_type == 'text_email':
            # Plain text email settings
            to_list = ["devblc1@daffodilvarsity.edu.bd"]
            subject = "Test Text Email"
            body = "Hello! This is a plain text test email sent via MailerSend."

            result = send_mailersend_email(to_list, subject, body)
        elif email_type == 'template_email':
            # Template email settings
            to_list = ["devblc1@daffodilvarsity.edu.bd"]
            subject = "OTP Email Test"
            template_name = "otp.html"
            context = {
                "name": "User Name",
                "otp": "123456",
                "text_fallback": "Your OTP is 123456"
            }

            result = send_mailersend_email(to_list, subject, template_name, context=context, is_template=True)
        else:
            self.stdout.write(self.style.ERROR("Invalid email type"))
            return

        if result['status'] == 'success':
            self.stdout.write(self.style.SUCCESS("Email sent successfully!"))
        else:
            self.stdout.write(self.style.ERROR(f"Error sending email: {result.get('error')}"))
