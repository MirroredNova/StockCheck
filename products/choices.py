FAST = 'Fast'
MED = 'Medium'
SLOW = 'Slow'
NOTIFICATION_INTERVAL = [
        (FAST, 'Notifications every 1 min'),
        (MED, 'Notifications every 10 min'),
        (SLOW, 'Notifications every 1 hour')
]

EMAIL = 'Email'
DISCORD = 'Discord'
SMS = 'SMS'
NOTIFICATION_CHOICES = [
        (EMAIL, 'Notications by Email'),
        (DISCORD, 'Notifications by Discord DM'),
        (SMS, 'Notifications by Text Message'),
]

