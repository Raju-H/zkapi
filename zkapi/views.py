from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from zk import ZK, const
from datetime import datetime
from rest_framework import generics


from .models import *
from .serializers import *




class AttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        user_id = request.user.id

        if not username:
            return Response({"error": "Username parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(username=username)
            zk = ZK(device.ip_address, port=device.port, timeout=5)
            conn = zk.connect()
            conn.disable_device()

            users = conn.get_users()
            user_dict = {
                user.user_id: {
                    "name": user.name,
                    "privilege": "Admin" if user.privilege == const.USER_ADMIN else "User",
                    "group_id": user.group_id,
                }
                for user in users if user.user_id == user_id
            }

            attendance = conn.get_attendance()
            today = datetime.today().date()
            todays_attendance = [
                record for record in attendance if record.timestamp.date() == today and record.user_id == user_id
            ]

            in_out_records = self.filter_in_out(todays_attendance)

            response_data = self.build_response_data(in_out_records, user_dict, device)

            return Response(response_data, status=status.HTTP_200_OK)

        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if 'conn' in locals():
                conn.enable_device()
                conn.disconnect()

    def filter_in_out(self, attendance_records):
        in_out_records = {}
        for record in attendance_records:
            if record.user_id not in in_out_records:
                in_out_records[record.user_id] = {"in": record.timestamp, "out": None}
            else:
                in_out_records[record.user_id]["out"] = record.timestamp
        return in_out_records

    def build_response_data(self, in_out_records, user_dict, device):
        response_data = []
        for user_id, times in in_out_records.items():
            user_details = user_dict.get(user_id, {
                "name": "Unknown",
                "privilege": "Unknown",
                "group_id": "Unknown",
            })
            response_data.append({
                "user_id": user_id,
                "user_name": user_details['name'],
                "privilege": user_details['privilege'],
                "group_id": user_details['group_id'],
                "in_time": times['in'],
                "out_time": times['out'],
                "device_name": device.name,
                "device_area": device.area,
                "device_username": device.username,
            })
        return response_data



class DeviceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

class DeviceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]