from rest_framework import serializers
from .models import Toll, Booth, Vehicle, Pass, Leaderboard


class TollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toll
        fields = ['id', 'name', 'location']


class BoothSerializer(serializers.ModelSerializer):
    parent = TollSerializer()
    
    class Meta:
        model = Booth
        fields = ['id', 'parent', 'is_active']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'reg_no', 'vehicle_type']


class PassSerializer(serializers.ModelSerializer):
    toll = TollSerializer()
    vehicle = VehicleSerializer()
    
    class Meta:
        model = Pass
        fields = ['id', 'pass_type', 'toll', 'vehicle', 'price', 'valid_till']


class LeaderboardSerializer(serializers.ModelSerializer):
    booth = BoothSerializer()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'booth', 'vehicles_passed', 'toll_charges_collected']
