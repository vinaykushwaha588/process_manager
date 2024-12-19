from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from datetime import datetime
from django.db.models import Min
from .models import System, Process
from .serializers import ProcessSerializer
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProcessDataAPIView(CreateAPIView):
    """
        API to receive process data from systems and store it in the database.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

    def create(self, request, *args, **kwargs):
        try:
            system_name = request.data.get("system_name")
            processes = request.data.get("processes", [])
            
            if any([not system_name, not processes]):
                raise ValueError("System name and processes are required.")

            system, _ = System.objects.get_or_create(name=system_name)

            # Bulk creation of processes for efficiency
            process_instances = [
                Process(
                    system=system,
                    pid=proc["pid"],
                    name=proc["name"],
                    cpu_percent=proc["cpu_percent"],
                    memory_percent=proc["memory_percent"],
                )
                for proc in processes
            ]
            with transaction.atomic():
                Process.objects.bulk_create(process_instances)

            return Response({"success":True, "message": "Data received successfully."}, status=status.HTTP_201_CREATED)
        
        except ValueError as val_err:
            logger.error(f"Validation error: {str(val_err)}")
            return Response({'success': False, 'message': val_err.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logger.exception(f"Unexpected error: {str(err)}")
            return Response({'error': err.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Process Filtering by System and Time Range
class ProcessFilterAPIView(ListAPIView):
    """
        API to fetch process data for a specific system with optional time filters.
    """
    serializer_class = ProcessSerializer

    def parse_time_string(self, time_string):
        """Convert time string to an aware datetime object, assuming the same day."""
        today = datetime.today().date()
        naive_time = datetime.strptime(f"{today} {time_string}", "%Y-%m-%d %H:%M:%S")
        aware_time = timezone.make_aware(naive_time, timezone.get_default_timezone())
        return aware_time

    def get_queryset(self):
        start_time_str = self.request.GET.get('start_time')
        end_time_str = self.request.GET.get('end_time')

        filters = Q() 

        if start_time_str:
            start_time = self.parse_time_string(start_time_str)
            filters &= Q(timestamp__gte=start_time)

        if end_time_str:
            end_time = self.parse_time_string(end_time_str)
            filters &= Q(timestamp__lte=end_time)


        # Apply optional time filters
        queryset = Process.objects.all().select_related('system').values(
            'id', 
            'system__name', 
            'name',         
            'pid', 
            'timestamp', 
            'cpu_percent', 
            'memory_percent'
        )

        if filters:
            queryset = queryset.filter(filters)
        
        return queryset


        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            data = list(queryset)
            return Response({'success': True, 'data': data, 'count': queryset.count()},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"success":False, "message":str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


# Process Duration Calculation
class ProcessDurationAPIView(APIView):
    """
        API to fetch the total duration a specific process has been running on a system.
    """
    def get(self, request):
        system_name = request.query_params.get("system_name")
        process_name = request.query_params.get("process_name")

        if not system_name or not process_name:
            return Response({
                "success": False,
                "message": "Both system name and process name are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        processes = Process.objects.filter(system__name=system_name, name=process_name)

        if processes.exists():
            # Calculate the earliest timestamp for the process
            earliest_timestamp = processes.aggregate(Min("timestamp"))["timestamp__min"]

            if earliest_timestamp is None:
                return Response({
                    "success": False,
                    "message": "No valid timestamps found for the specified process."
                }, status=status.HTTP_404_NOT_FOUND)

            duration = now() - earliest_timestamp
            return Response({
                "success": True,
                "duration_seconds": duration.total_seconds(),
                "duration_human_readable": str(duration)
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "No process found with the specified name on the system."
        }, status=status.HTTP_404_NOT_FOUND)
