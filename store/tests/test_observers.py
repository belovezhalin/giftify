from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Customer
from store.observers import Observer, Subject, UserObserver
from unittest.mock import patch

class ObserverTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')
        self.subject = Subject()
        self.observer = UserObserver(self.customer)
        self.subject.attach(self.observer)

    def test_attach_observer(self):
        self.assertIn(self.observer, self.subject._observers)

    def test_detach_observer(self):
        self.subject.detach(self.observer)
        self.assertNotIn(self.observer, self.subject._observers)

    def test_notify_observers(self):
        with patch('store.observers.send_mail') as mock_send_mail:
            self.subject.notify('Test message')
            mock_send_mail.assert_called_once_with(
                'New Offer Notification',
                'Test message',
                'from@example.com',
                [self.customer.email],
                fail_silently=False,
            )

    def test_observer_update(self):
        with patch('store.observers.send_mail') as mock_send_mail:
            self.observer.update('Test message')
            mock_send_mail.assert_called_once_with(
                'New Offer Notification',
                'Test message',
                'from@example.com',
                [self.customer.email],
                fail_silently=False,
            )

    def test_subject_notify_no_observers(self):
        self.subject.detach(self.observer)
        with patch('store.observers.send_mail') as mock_send_mail:
            self.subject.notify('Test message')
            mock_send_mail.assert_not_called()

    def test_observer_update_logging(self):
        with patch('store.observers.logger.info') as mock_logger_info:
            self.observer.update('Test message')
            mock_logger_info.assert_called_once_with('New offer on testuser: Test message')

    def test_subject_attach_duplicate_observer(self):
        initial_count = len(self.subject._observers)
        self.subject.attach(self.observer)
        self.assertEqual(len(self.subject._observers), initial_count)

    def test_subject_detach_nonexistent_observer(self):
        non_existent_observer = UserObserver(self.customer)
        initial_count = len(self.subject._observers)
        self.subject.detach(non_existent_observer)
        self.assertEqual(len(self.subject._observers), initial_count)