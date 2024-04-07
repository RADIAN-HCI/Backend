# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .assignment_generator.create_assignment import retrieve_and_generate_pdf

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework.permissions import IsAuthenticated


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]


@csrf_exempt
def generate_pdf_api(request):
    if request.method == "POST":
        try:
            # Retrieve the assignment_id from the POST request data
            assignment_id_str = request.POST.get("assignment_id")
            # Check if assignment_id_str is None or empty
            if assignment_id_str is None or assignment_id_str == "":
                return JsonResponse(
                    {"error": "assignment_id is missing or empty"}, status=400
                )

            # Convert the assignment_id to an integer
            assignment_id = int(assignment_id_str)

            # Call the function to retrieve the PDF for the specified assignment_id
            retrieve_and_generate_pdf(assignment_id)

            return JsonResponse({"message": "PDF generated successfully"}, status=200)
        except ValueError:
            return JsonResponse(
                {"error": "Invalid assignment_id. It must be an integer."}, status=400
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
