from datetime import timedelta
from django.utils import timezone
from .models import Card, Notification


def sendDeadlineNotifications():
    notification_24_hours = timezone.now() + timedelta(hours=24)
    notification_12_hours = timezone.now() + timedelta(hours=12)

    cards = Card.objects.all()
    for card in cards:
        if card.deadLine.date() == notification_24_hours.date():
            Notification.objects.create(notificationCard=card, message="24 hours left!",
                                        notificationUsers=card.assignUsers)
        elif card.deadLine.date() == notification_12_hours.date():
            Notification.objects.create(notificationCard=card, message="12 hours left!",
                                        notificationUsers=card.assignUsers)
        elif card.deadLine.date() < timezone.now():
            Notification.objects.create(notificationCard=card, message="failed card",
                                        notificationUsers=card.assignUsers)

# bellow command for apply cron job setting
# python manage.py crontab add
# python manage.py crontab show
# python manage.py crontab remove
