from django.urls import path
from working_spaces.views import (
    TypeWorkingSpaceDetailView,
    TypeWorkingSpaceListView,
    WorkingSpaceDetailView,
    WorkingSpaceListView,
)

urlpatterns = [
    path("working-space/", WorkingSpaceListView.as_view(), name="list_working_space"),
    path(
        "working-space/<int:pk>/",
        WorkingSpaceDetailView.as_view(),
        name="detail_working_space",
    ),
    path(
        "working-space-type/",
        TypeWorkingSpaceListView.as_view(),
        name="list_type_working_space",
    ),
    path(
        "working-space-type/<int:pk>/",
        TypeWorkingSpaceDetailView.as_view(),
        name="detail_type_working_space",
    ),
]
