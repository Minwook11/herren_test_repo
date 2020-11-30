from django.urls import path

from .views import (
    SubscribeView,
    UnsubscribeView,
    SendView
)

urlpatterns = [
    path('/subscribe', SubscribeView.as_view()),
    path('/unsubscribe', UnsubscribeView.as_view()),
    path('/send', SendView.as_view()),
]
