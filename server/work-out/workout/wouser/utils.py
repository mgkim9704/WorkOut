import pyfcm
from django.conf import settings
from .models import Profile


def push_message(user, title, message, **kwargs):
    try:
        push_service = pyfcm.FCMNotification(
            settings.FCM_API_KEY
        )
        profile = Profile.objects.get(user=user)

        if profile.fcm_registration_id:
            data_message = {
                 "message_title": title,
                 "message_body": message
            }
            result = push_service.notify_single_device(
                registration_id=profile.fcm_registration_id,
                message_title=title,
                message_body=message,
                **kwargs
            )
            print("push_success!", result, data_message)
        else:
            print("push_message fail ", user, title, message)
    except BaseException as e:
        print(e)
