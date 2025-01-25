from django.core.mail import send_mail

import logging

logger = logging.getLogger('django')

class Observer:
    def update(self, message):
        raise NotImplementedError("Subclasses must implement this method")

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class UserObserver(Observer):
    def __init__(self, customer):
        self.customer = customer

    def update(self, message):
        logger.info(f'New offer on {self.customer.user.username}: {message}')
        send_mail(
            'New Offer Notification',
            message,
            'from@example.com',
            [self.customer.email],
            fail_silently=False,
        )