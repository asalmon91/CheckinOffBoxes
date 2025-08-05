from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views  # importing all handlers from views.py
from .views import BoardFormView, TaskFormView

urlpatterns = [
                  path('', views.MainView.as_view(), name="home"),
                  path('boards/', views.BoardListView.as_view(), name='board-set'),
                  path('boards/<uuid:pk>/', views.BoardView.as_view(), name="board_view"),
                  path('boards/boardform/', BoardFormView.as_view()),
                  path('boards/taskform/', TaskFormView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # For collectstatic

# For development serving:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
