VERSION = (0, 1, 0, "final")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
}

# replacement for django.core.mail.send_mail

def send_mail(subject, message, from_email, recipient_list, priority="medium",
              fail_silently=False, reply_to=None, auth_user=None, auth_password=None):
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    # need to do this in case subject used lazy version of ugettext
    
    if len(subject) > 100:
        subject = "%s..." % subject[:97]
    
    for to_address in recipient_list:
        Message(to_address=to_address,
                from_address=from_email,
                subject=subject,
                message_body=message,
                priority=priority,
                reply_to=reply_to).save()

def mail_admins(subject, message, fail_silently=False, priority="medium"):
    from django.conf import settings
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    if len(subject) > 100:
        subject = "%s..." % subject[:97]
    
    for name, to_address in settings.ADMINS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=subject,
                message_body=message,
                priority=priority).save()

def mail_managers(subject, message, fail_silently=False, priority="medium"):
    from django.conf import settings
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    if len(subject) > 100:
        subject = "%s..." % subject[:97]
    
    for name, to_address in settings.MANAGERS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=subject,
                message_body=message,
                priority=priority).save()
