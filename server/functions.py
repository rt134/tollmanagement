from django.utils import timezone
from datetime import timedelta
from .models import *

def verify_pass(booth_id, reg_no):
    booth = Booth.objects.get(id=booth_id)
    vehicle = Vehicle.objects.get(reg_no=reg_no)
    vehicle_passes = Pass.objects.filter(vehicle_id=vehicle.id).filter(toll_id=booth.parent_id)
    for vehicle_pass in vehicle_passes:
        if vehicle_pass.valid_till > timezone.now():
            return vehicle_pass
    return None

def buy_pass(booth_id, reg_no, pass_num):
    try:
        toll_id = Booth.objects.get(id=booth_id).parent_id
        vehicle_id = Vehicle.objects.get(reg_no=reg_no).id
        pass_obj = Pass.objects.create(pass_type=pass_num,toll_id=toll_id,vehicle_id=vehicle_id)
        update_leaderboard(booth_id,pass_obj.price)
        return pass_obj
    except Exception as exception:
        print(str(exception))
        return None


def process_vehicle(booth_id, reg_no, vehicle_pass):

    if vehicle_pass.created_at > timezone.now() + timedelta(minutes=-1):
        print("Vehicle Passed and Leaderboard handled in buy Pass")
        return True
    else:
        if vehicle_pass.pass_type == 2:
            vehicle_pass.valid_till = timezone.now()
        update_leaderboard(booth_id,0)
        return True
    return False
    


def update_leaderboard(booth_id, price):
    try:
        leaderboard_obj, created = Leaderboard.objects.get_or_create(booth_id=booth_id)
        if created:
            leaderboard_obj.vehicles_passed = 1
            leaderboard_obj.toll_charges_collected = price
        else:
            leaderboard_obj.vehicles_passed += 1
            leaderboard_obj.toll_charges_collected += price
        leaderboard_obj.save()
        return True
    except Exception as exception:
        print(str(exception))
        return False
