from django.urls import path
from .views import GetLeaderboard, GetPassByVehicle, VehicleList

urlpatterns = [
    path('leaderboard/',GetLeaderboard.as_view()),
    path('vehicles/',VehicleList.as_view()),
    path('vehicle/<str:vpk>/booth/<int:bpk>/',GetPassByVehicle.as_view())
]