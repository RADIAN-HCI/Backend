from rest_framework import viewsets
from .models import BrainStorm
from idea.models import Idea
from .serializers import BrainStormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from assignment.models import Assignment
from course.models import Course
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
import re
from langchain_cohere import ChatCohere


class BrainstormViewSet(viewsets.ModelViewSet):
    queryset = BrainStorm.objects.all()
    serializer_class = BrainStormSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        assignment_param = self.request.query_params.get("assignment_id") or self.request.query_params.get("assignment")

        if assignment_param:
            try:
                assignment_id = int(assignment_param)
            except (TypeError, ValueError):
                return queryset.none()

            queryset = queryset.filter(assignment_id=assignment_id)

        return queryset

    def parse_response(self, response):
        questions = []
        pattern = r"Question\d+\|([^|]+)\|([^|]+)\|<?(\d+)>?\|<?(\d+)>?"
        matches = re.findall(pattern, response)

        for match in matches:
            # print(match)
            title = match[0].strip()
            question_text = match[1].strip()
            innovation_score = int(match[2])
            difficulty_score = int(match[3])
            questions.append(
                {
                    "title": title,
                    "text": question_text,
                    "innovation_score": innovation_score,
                    "difficulty_score": difficulty_score,
                }
            )
        return questions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["owner"] = request.user
        brainstorm_obj = serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)

        assignment = Assignment.objects.get(id=request.data["assignment"])
        prompt_user = request.data["prompt"]
        course = Course.objects.get(id=request.data["course"])
        lang = request.data["lang"]

        prompt_english = """
            I am going to design an assignment for the course {course} on the topic of {topic}, provide 4 question ideas specifically. For each question idea, give two scores out of 5 in integer value:
            1. Innovation score: How innovative or thought-provoking is the question idea?
            2. Difficulty score: How difficult or challenging is the question idea?

            Your question should be on the following theme: {theme}

            The response you give should exatlye be like the following format, nothing less, nothing more:

            Question1|<title>|<question text>|<innovation score>|<difficulty score>
            Question2|<title>|<question text>|<innovation score>|<difficulty score>
            Question3|<title>|<question text>|<innovation score>|<difficulty score>
            Question4|<title>|<question text>|<innovation score>|<difficulty score>
        """

        prompt_persian = """
            برای یک تکلیف درباره موضوع {topic} در درس {course}، 4 ایده سوال ارائه دهید. برای هر ایده سوال، دو امتیاز به مقدار عددی که با رقم باشد، از 5 بدهید:
            1. امتیاز نوآوری: این ایده سوال تا چه حد نوآورانه یا برانگیزاننده تفکر است؟
            2. امتیاز دشواری: این ایده سوال تا چه حد دشوار یا چالش برانگیز است؟
            
            سوالاتی که طرح می کنید، باید درباره موضوع زیر باشند: {theme}

            (به ترتیبی که امتیاز نوآوری و امتیاز دوشواری دو عدد آخر در هر خط باشند) پاسخی که میدهی دقیقا باید با فرمت زیر باشد، نه بیشتر و نه کمتر

            Question1|<عنوان>|<متن سوال>|<امتیاز نوآوری>|<امتیاز دشواری>
            Question2|<عنوان>|<متن سوال>|<امتیاز نوآوری>|<امتیاز دشواری>
            Question3|<عنوان>|<متن سوال>|<امتیاز نوآوری>|<امتیاز دشواری>
            Question4|<عنوان>|<متن سوال>|<امتیاز نوآوری>|<امتیاز دشواری>
        """

        if lang == "fa":
            prompt = prompt_persian.format(
                topic=assignment.title, course=course.name, theme=prompt_user
            )
        else:
            prompt = prompt_english.format(
                topic=assignment.title, course=course.name, theme=prompt_user
            )
        llm = ChatCohere()

        llm_response = llm.invoke(prompt).content

        parsed_questions = self.parse_response(llm_response)

        for question in parsed_questions:
            title = question["title"]
            details = question["text"]
            difficulty = question["difficulty_score"]
            innovation = question["innovation_score"]
            data = {
                "title": title,
                "details": details,
                "difficulty": difficulty,
                "innovation": innovation,
                "brainstorm": brainstorm_obj,
                "owner": request.user,
            }
            Idea(**data).save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # def list(self, request, *args, **kwargs):
    #     author_id = request.query_params.get('author_id')
    #     assignment_id = request.query_params.get('assignment_id')

    #     if not author_id or not assignment_id:
    #         return Response({"error": "Both author_id and assignment_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         author_id = int(author_id)
    #         assignment_id = int(assignment_id)
    #     except ValueError:
    #         return Response({"error": "author_id and assignment_id must be integers"}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         author_brainstorms = BrainStorm.objects.filter(owner_id=author_id, assignment_id=assignment_id)
    #         serializer = self.get_serializer(author_brainstorms, many=True)
    #         return Response(serializer.data)
    #     except Assignment.DoesNotExist:
    #         return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
