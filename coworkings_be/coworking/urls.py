from coworking.views import CoworkingListView, CoworkingView
from django.urls import path

urlpatterns = [
    path("coworkings/<int:pk>/", CoworkingView.as_view(), name="coworking-item"),
    path("coworkings/", CoworkingListView.as_view(), name="coworking-list"),
]
