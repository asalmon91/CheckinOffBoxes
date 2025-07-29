from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views  # importing all handlers from views.py

urlpatterns = [
                  path('boards/', views.BoardListView.as_view(), name='board-set'),
                  path('boards/<uuid:pk>/', views.BoardView.as_view(), name="board_view"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # For collectstatic

# For development serving:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
