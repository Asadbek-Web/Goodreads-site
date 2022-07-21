from django.shortcuts import render, redirect
from django.views import View

from books.models import Author

class BookAuthorView(View):
    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)

        return render(request, "author/author.html", {"author": author,})
