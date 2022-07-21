from django.urls import reverse

from django.test import TestCase
from users.models import CustomUser
from books.models import Book, BookReview

class ReviewPageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="book1", description="Description", isbn="123232544")
        user = CustomUser.objects.create( 
                username="asadbek", first_name="Asadbek", last_name="Abdumalikov", email="asadbekabdumalikovfifth@gmail.com"
        )
            
        user.set_password("somepassword")
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given=2, comment="Very useful")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Good book")

        response = self.client.get(reverse("review_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)