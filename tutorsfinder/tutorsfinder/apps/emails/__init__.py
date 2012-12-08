import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template import Template as TemplateTemplate


logger = logging.getLogger(__name__)

def apply_context(string, dictionary):
    return TemplateTemplate(string).render(Context(dictionary))

class EmailMessage(EmailMultiAlternatives):
    """
    Extending django.code.mail.EmailMessage to inject bcc email to
    all outgoing email.
    """

    def __init__(self, *args, **kwargs):
        args_list = list(args)

        bcc = getattr(settings, 'BCC_LIST', None)

        # if bcc email is given, get it then extend instead of replacing it
        if bcc is not None:
            if len(args) > 4:
                bcc.extend(args_list[4])
                args_list[4] = bcc
            else:
                if len(args) == 4:
                    args_list.append(bcc)

        args = tuple(args_list)
        super(EmailMessage, self).__init__(*args, **kwargs)


def send_using_template(email_template, context, user_email, bcc=[]):
    reply_to = getattr(settings, 'EMAIL_REPLY_TO', False)

    subject_string = email_template.subject
    template_string = email_template.template
    template_html = email_template.template_html

    subject = apply_context(subject_string, context)
    body = apply_context(template_string, context)
    body_html = apply_context(template_html, context)
    from_email = settings.EMAIL_SENDER

    if (getattr(settings, 'EMAIL_PRODUCTION_MDOE', False)):
        to_email = [settings.EMAIL_SENDER]
    else:
        if isinstance(user_email, list):
            to_email = user_email
        else:
            to_email = [email.strip() for email in user_email.split(",")]

    headers = {
        'Reply-To': reply_to,
    }

    email = EmailMessage(subject, body, from_email, to_email, bcc=bcc, headers=headers)
    if template_html:
        email.attach_alternative(body_html, "text/html")

    email_sent = email.send(fail_silently=True)

    # log message
    log_message = "%s | email from %s to %s and bcc %s using template %s" % (
                email_sent,
                from_email,
                ",".join(to_email),
                ",".join(bcc),
                email_template.slug,
            )
    logger.info(log_message, exc_info=True)

    return email_sent
