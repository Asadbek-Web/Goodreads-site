from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview


def landing_page(request):
    print(request.user.is_authenticated)
    return render(request, 'landing.html')


def review_page(request):
    book_review = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 5)
    paginator = Paginator(book_review, page_size)

    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)


    return render(request, "review.html", {"page_obj": page_object })



def time_view(request):
    time = datetime.datetime.now() + datetime.timedelta(hours=1)
    return render(request, "base.html", {'time': time })