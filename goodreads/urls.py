
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import landing_page, review_page


urlpatterns =[
    path('', landing_page, name='landing_page'),
    path('review/', review_page, name='review_page'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api/', include('api.urls')),
    path('author/', include('author.urls')),

    path('api-auth/', include('rest_framework.urls')),
    
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)