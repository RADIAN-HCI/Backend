# views.py
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .assignment_generator.create_assignment import retrieve_and_generate_pdf
from django.conf import settings
import os
from django.urls import reverse

from rest_framework import viewsets
from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework.permissions import IsAuthenticated


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Role-based visibility: TAs see only their own
        user = self.request.user
        if getattr(user, 'role', None) == 'TA':
            queryset = queryset.filter(owner=user)
        return queryset


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
            pdf_path = retrieve_and_generate_pdf(assignment_id)

            # Also include a URL for clients to retrieve/view the PDF
            pdf_url = request.build_absolute_uri(reverse("assignment_pdf"))

            return JsonResponse({"message": "PDF generated successfully", "pdf_path": pdf_path, "pdf_url": pdf_url}, status=200)
        except ValueError:
            return JsonResponse(
                {"error": "Invalid assignment_id. It must be an integer."}, status=400
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def assignment_pdf_view(request):
    pdf_path = os.path.join(settings.BASE_DIR, "latex", "assignment_pdf.pdf")
    if not os.path.exists(pdf_path):
        raise Http404("PDF not found. Generate it first.")

    response = FileResponse(open(pdf_path, "rb"), as_attachment=False, filename="assignment_pdf.pdf", content_type="application/pdf")
    # Ensure inline display in browsers
    response["Content-Disposition"] = 'inline; filename="assignment_pdf.pdf"'
    return response
