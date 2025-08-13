from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views  # importing all handlers from views.py
from .views import BoardFormView, TaskFormView, COBSignupView, COBLoginView, COBLogoutView, BoardDeleteView

urlpatterns = [
                  path('', views.MainView.as_view(), name="home"),
                  path('boards/', views.BoardListView.as_view(), name='board-set'),
                  path('boards/<uuid:pk>/', views.BoardView.as_view(), name="board-view"),
                  path('boards/boardform/', BoardFormView.as_view(), name='new-board'),
                  path('boards/boardform/<uuid:pk>', BoardFormView.as_view(), name='edit-board'),
                  path('boards/<uuid:pk>/delete/', BoardDeleteView.as_view(), name="delete-board"),
                  path('boards/taskform/', TaskFormView.as_view()),
                  path('signup', COBSignupView.as_view()),
                  path('login', COBLoginView.as_view()),
                  path('logout', COBLogoutView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # For collectstatic

# For development serving:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
