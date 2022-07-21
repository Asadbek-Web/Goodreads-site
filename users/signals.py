# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.core.mail import send_mail

# from users.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):   #--> signal handler
#     if created:
#         send_mail( 
#             "Welcome to our Goodreads Clone",
#             f"Hello {instance.username} You can read books and reviews in our e-book site", 
#              "asadbekabdumalikovfifth@gmail.com", 
#             [instance.email]
#         )