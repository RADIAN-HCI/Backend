# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from assignment.serializers import AssignmentSerializer
# from core.models import Course, User
# from course.serializers import CourseSerializer, UserProfileSerializer


# # class CourseViewSet(viewsets.ModelViewSet):
# #     queryset = Course.objects.all()

# #     def retrieve(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         assignments = instance.assignment_set.all()
# #         assignment_serializer = AssignmentSerializer(assignments, many=True)

# #         return Response(
# #             {
# #                 "course": {
# #                     "id": instance.id,
# #                     "name": instance.name,
# #                     # Add other course fields as needed
# #                 },
# #                 "assignments": assignment_serializer.data,
# #             }
# #         )


# class IsAuthenticatedUser(permissions.BasePermission):
#     """
#     Allows access only to authenticated users.
#     """

#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated


# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticatedUser]

#     def perform_create(self, serializer):
#         course = serializer.save()
#         user = self.request.user
#         user.courses.add(course)

#     def perform_update(self, serializer):
#         course = serializer.save()
#         user = self.request.user
#         user.courses.add(course)


# # class UserCourseViewSet(viewsets.ViewSet):
# #     permission_classes = [IsAuthenticated]

# #     def create(self, request):
# #         try:
# #             course_id = request.data["course_id"]
# #             course = Course.objects.get(pk=course_id)
# #             user_profile = request.user.userprofile
# #             user_profile.courses.add(course)
# #             user_profile.save()
# #             serializer = CourseSerializer(course)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         except KeyError:
# #             return Response(
# #                 {"error": "Please provide a course_id in the request data."},
# #                 status=status.HTTP_400_BAD_REQUEST,
# #             )
# #         except Course.DoesNotExist:
# #             return Response(
# #                 {"error": "Course with the provided ID does not exist."},
# #                 status=status.HTTP_404_NOT_FOUND,
# #             )


# # class UserViewSet(viewsets.ViewSet):
# #     @action(detail=False, methods=["post"])
# #     def signup(self, request):
# #         serializer = UserProfileSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save()
# #             user.set_password(request.data["password"])
# #             user.save()
# #             token, created = Token.objects.get_or_create(user=user)
# #             return Response(
# #                 {"token": token.key, "user": serializer.data},
# #                 status=status.HTTP_201_CREATED,
# #             )
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     @action(detail=False, methods=["post"])
# #     def login(self, request):
# #         user = get_object_or_404(UserProfile, username=request.data["username"])
# #         if not user.check_password(request.data["password"]):
# #             return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
# #         token, created = Token.objects.get_or_create(user=user)
# #         serializer = UserProfileSerializer(user)
# #         return Response(
# #             {"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK
# #         )


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer

#     @action(detail=False, methods=["post"])
#     def signup(self, request):
#         serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.set_password(request.data["password"])
#             user.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(
#                 {"token": token.key, "user": serializer.data},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=False, methods=["post"])
#     def login(self, request):
#         user = get_object_or_404(User, username=request.data["username"])
#         if not user.check_password(request.data["password"]):
#             return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
#         token, created = Token.objects.get_or_create(user=user)
#         serializer = UserProfileSerializer(user)
#         return Response(
#             {"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK
#         )

#     @action(detail=True, methods=["post"])
#     def add_course(self, request, pk=None):
#         user = self.get_object()
#         course_id = request.data.get("course_id")
#         if course_id:
#             try:
#                 course = Course.objects.get(pk=course_id)
#                 user.courses.add(course)
#                 user.save()
#                 return Response(
#                     {"detail": "Course added successfully"}, status=status.HTTP_200_OK
#                 )
#             except Course.DoesNotExist:
#                 return Response(
#                     {"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND
#                 )
#         else:
#             return Response(
#                 {"detail": "Please provide a course_id"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
