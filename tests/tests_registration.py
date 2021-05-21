from django.test import TestCase
from StartPage.views import CheckRegistrPage


class RegistrationTest(TestCase):

    def test_registration_mistakes(self):
        password_mistakes = [[None, 'user', '!qwert^123', '!qwert^123'],
                             [None, 'user', 'qwerty123', 'qwerty321'],
                             [None, 'user', '1234567890', '1234567890'],
                             [None, 'user', 'qwe', 'qwe'],
                             [None, 'user', 'qwerty1234', 'qwerty1234']]
        password_messages = ['Enter a valid password. Only letters, numbers, and @/./+/-/_ are allowed',
                             'Password fields did not match',
                             'This password is entirely numeric',
                             'This password is too short. It must contain at least 8 characters',
                             'success']
        for i, case in enumerate(password_mistakes):
            message = CheckRegistrPage(*case)
            self.assertEqual(message, password_messages[i])
        username_mistakes = [[None, '~~uSER$$', 'qwerty1234', 'qwerty1234'],
                             [None, 'UseR', 'qwerty1234', 'qwerty1234']]
        username_messages = ['Enter a valid username. Only letters, numbers, and @/./+/-/_ are allowed',
                             'success']
        for i, case in enumerate(username_mistakes):
            message = CheckRegistrPage(*case)
            self.assertEqual(message, username_messages[i])
        user_mistakes = [['user', 'UseR', 'qwerty1234', 'qwerty1234'],
                         [None, 'UseR', 'qwerty1234', 'qwerty1234']]
        user_messages = ['This user already exists',
                         'success']
        for i, case in enumerate(user_mistakes):
            message = CheckRegistrPage(*case)
            self.assertEqual(message, user_messages[i])
        if_empty_mistakes = [[None, '', 'qwerty1234', 'qwerty1234'],
                             [None, 'UseR', '', ''],
                             [None, 'UseR', 'qwerty1234', 'qwerty1234']]
        if_empty_messages = ['please, fill all the fields',
                             'please, fill all the fields',
                             'success']
        for i, case in enumerate(if_empty_mistakes):
            message = CheckRegistrPage(*case)
            self.assertEqual(message, if_empty_messages[i])