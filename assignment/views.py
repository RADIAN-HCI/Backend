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
import posixpath


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

            # Build a direct URL to the generated file
            filename = os.path.basename(pdf_path)
            pdf_url = request.build_absolute_uri(reverse("serve_generated_pdf", kwargs={"filename": filename}))

            return JsonResponse({"message": "PDF generated successfully", "pdf_url": pdf_url, "file_name": filename}, status=200)
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


def serve_generated_pdf(request, filename: str):
    # Only allow simple filenames (defend against path traversal)
    if "/" in filename or ".." in filename or filename.startswith("."):
        raise Http404("Invalid filename")
    if not filename.lower().endswith(".pdf"):
        raise Http404("Unsupported file type")

    latex_dir = os.path.join(settings.BASE_DIR, "latex")
    pdf_path = os.path.normpath(os.path.join(latex_dir, filename))
    # Ensure the file is inside the latex directory
    if not pdf_path.startswith(os.path.abspath(latex_dir) + os.sep):
        raise Http404("Invalid path")
    if not os.path.exists(pdf_path):
        raise Http404("PDF not found")

    response = FileResponse(open(pdf_path, "rb"), as_attachment=False, filename=filename, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
