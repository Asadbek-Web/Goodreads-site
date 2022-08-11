from django.urls import path
from author.views import BookAuthorView

app_name = "author"

urlpatterns = [
    
    path('<int:id>/', BookAuthorView.as_view(), name="author")
]
