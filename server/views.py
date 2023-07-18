from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .functions import *



class VehicleList(APIView):
    def get(self, request, format=None):
        try:
            vehicle = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicle, many=True)
            return Response(serializer.data)
        except Exception as exception:
            return Response({"error": str(exception)})


class GetLeaderboard(APIView):

    def get(self, request, format=None):
        try:
            leaderboard = Leaderboard.objects.all()
            serializer = LeaderboardSerializer(leaderboard, many=True)
            return Response(serializer.data)
        except Exception as exception:
            return Response({"error": str(exception)})

class GetPassByVehicle(APIView):

    def get(self, request, vpk, bpk ,format=None):
        try:
            reg_no = str(vpk)
            booth_no = int(bpk)

            vehicle = Vehicle.objects.get(reg_no=reg_no)

            if verify_pass(booth_no, reg_no):
                return Response({"msg": "Pass Valid ! Happy Journey"})
            
            pricing = Pricing.objects.filter()
            fares = {
                "Single Pass" : pricing.filter(pass_type=1)[0].fare * vehicle.vehicle_type,
                "Return Pass" : pricing.filter(pass_type=2)[0].fare * vehicle.vehicle_type,
                "Seven Day pass" : pricing.filter(pass_type=3)[0].fare * vehicle.vehicle_type,
            }
            return Response({"msg": "NO VALID PASS ! Please Buy a new Pass", "fares" : fares})
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, vpk, bpk ,format=None):
        try:
            reg_no = str(vpk)
            booth_id = int(bpk)
            pass_num = int(request.data['buy_pass'])

            if pass_num == 0:
                vehicle_pass = verify_pass(booth_id, reg_no)
                if vehicle_pass != None:
                    processed = process_vehicle(booth_id, reg_no, vehicle_pass)
                    if processed:
                        return Response({"msg": "Used Your existing Pass !! Happy Journey !!"})
                    else:
                        return Response({"msg": "Unable to process! Please Try Again"}, status=400)
            elif pass_num > 0:
                vehicle_pass = buy_pass(booth_id, reg_no, pass_num)
                pass_data = PassSerializer(vehicle_pass)
                processed = process_vehicle(booth_id, reg_no, vehicle_pass)
                if processed:
                    return Response({"msg": "!! Happy Journey !!", "pass details" : pass_data.data})
                else:
                    return Response({"msg": "Unable to process! Please Try Again"}, status=400)

        except Exception as exception:
            return Response({"Error": str(exception)})



    
