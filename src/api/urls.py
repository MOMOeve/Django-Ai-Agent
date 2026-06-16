from django.urls import path

from .views import ChatView, CsrfView, DocumentListView, LoginView, LogoutView, MeView

urlpatterns = [
    path("auth/csrf/", CsrfView.as_view(), name="api-csrf"),
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("auth/logout/", LogoutView.as_view(), name="api-logout"),
    path("auth/me/", MeView.as_view(), name="api-me"),
    path("chat/", ChatView.as_view(), name="api-chat"),
    path("documents/", DocumentListView.as_view(), name="api-documents"),
]
