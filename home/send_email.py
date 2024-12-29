from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_email(template_name, context, recipient_email, subject):
    """
    A function to send an email using a template.

    :param template_name: The path to the email template (e.g., 'email_template.html').
    :param context: The context to render the template with (e.g., {'name': 'John Doe'}).
    :param recipient_email: The recipient's email address.
    :param subject: The subject of the email.
    """
    # Render the email content from the template with the context
    message = render_to_string(template_name, context)

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Sender email (set in settings.py)
        [recipient_email],
        html_message=message,  # Send HTML formatted message
    )
