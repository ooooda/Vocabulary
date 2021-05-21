from django.test import TestCase
from StartPage.models import Vocabulary, Book
from django.contrib.auth.models import User

from StartPage.views import ChangeColour


class VocabularyTest(TestCase):
    def setUp(self):
        user = User.objects.create()
        book = Book.objects.create(user=user)
        Vocabulary.objects.create(word='WORD', colour_status='red', book=book)

    def test_word_change_colour(self):
        word = Vocabulary.objects.get(word='WORD')
        incorrect_word = 'word'
        correct_word = 'WORD'
        status = ChangeColour(word, correct_word)
        self.assertEqual(word.colour_status, 'orange')
        self.assertEqual(status, True)
        status = ChangeColour(word, correct_word)
        self.assertEqual(word.colour_status, 'green')
        self.assertEqual(status, True)
        status = ChangeColour(word, incorrect_word)
        self.assertEqual(status, False)
        self.assertEqual(word.colour_status, 'orange')
        status = ChangeColour(word, incorrect_word)
        self.assertEqual(word.colour_status, 'red')
        self.assertEqual(status, False)


