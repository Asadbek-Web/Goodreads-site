from rest_framework.test import APITestCase

from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    # DRY --> Don't repeat yourself
    def setUp(self):
        self.user = CustomUser.objects.create(username="asadbek", first_name="Asadbek")
        self.user.set_password("somepassword")
        self.user.save()
        self.client.login(username="asadbek", password="somepassword")
    
    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.get(reverse("api:review-detail", kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], "Book1")
        self.assertEqual(response.data['book']['description'], "Description1")
        self.assertEqual(response.data['book']['isbn'], "12131231")
        self.assertEqual(response.data['user']['id'], br.user.id)
        self.assertEqual(response.data['user']['first_name'], 'Asadbek')
        self.assertEqual(response.data['user']['username'], 'asadbek')



    def test_book_review_delete(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.delete(reverse("api:review-detail", kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())


    def test_patch_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.patch(reverse("api:review-detail", kwargs={"id": br.id}), data={'stars_given' : 4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)

    
    def test_put_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.put(reverse("api:review-detail", kwargs={"id": br.id}), 
            data={'stars_given':4, 'comment':'good book', 'user_id':self.user.id, 'book_id':book.id}
        )
        br.refresh_from_db()


        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'good book')


    def test_create_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=3, comment="Not bad")

        # data={
        #     'stars_given':3,
        #     'comment':'not bad',
        #     'user':self.user.id,
        #     'book':book.id
        # }

        response = self.client.post(reverse('api:review-list'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, 'not bad')


    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username="somebody", first_name="Somebody")
        book = Book.objects.create(title="Book1", description="Description1", isbn='12131231')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=3, comment="Not good")


        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)

