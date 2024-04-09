from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from langchain_cohere import ChatCohere


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data["author"] = request.user
        lang = request.data["lang"]
        question = request.data["details_original"]

        llm = ChatCohere()

        prompt_english = """
        You are an AI assistant tasked with helping students anonymize and format their assignment questions. Your job is to take the raw text of an assignment question provided by the user and perform the following tasks:

        1. Remove any personally identifiable information (PII) such as names, email addresses, phone numbers, etc. Replace these with generic placeholders like [NAME], [EMAIL], etc.

        2. Format the question in a clear and readable manner. This may involve:
            - Adding line breaks and whitespace for better readability
            - Numbering question parts if there are multiple parts
            - Formatting code snippets or mathematical equations using markdown syntax
            - Any other formatting needed to improve clarity and structure

        3. Provide the anonymized and formatted version of the question back to the user.
        
        4. You should only and exactly return the formatted question text without any personal information and no additional explanations before or after it. Just return the formatted and anonymized question text.

        Here is the raw text of the question:
        {question}
        """

        prompt_persian = """
        شما یک دستیار هوش مصنوعی هستید که وظیفه کمک به دانشجویان برای حذف مشخصات شخصی و آماده سازی سوالات تکالیف را بر عهده دارید. کار شما این است که متن خام یک سوال تکلیف را که توسط کاربر ارائه می شود دریافت کنید و کارهای زیر را انجام دهید:

        1. حذف هر گونه اطلاعات شناسایی شخصی (PII) مانند نام، آدرس ایمیل، شماره تلفن و غیره. این موارد را با جایگزین های عمومی مانند [NAME]، [EMAIL] و غیره جایگزین کنید.

        2. قالب بندی سوال به شکل خوانا و واضح. این کار ممکن است شامل موارد زیر باشد:
            - اضافه کردن سطرهای جدید و فاصله برای بهبود خوانایی 
            - شماره گذاری بخش های مختلف سوال در صورت وجود چندین بخش
            - قالب بندی قطعات کد یا معادلات ریاضی با استفاده از سینتکس مارک داون
            - هر گونه قالب بندی دیگری که برای افزایش وضوح و ساختار لازم باشد

        3. ارائه نسخه حذف مشخصات شخصی شده و قالب بندی شده سوال به کاربر.
        
        4. فقط و فقط باید در جواب متن سوال را به صورت فرمت شده و بدون اطلاعات شخصی برگردانی و هیچ توضیحات اضافی ای قبل و یا بعد آن نیاوری. فقط متن سوال را جواب بده.

        متن خام سوال در ادامه آمده است:
        {question}
        """

        if lang == "fa":
            prompt = prompt_persian.format(question=question)
        else:
            prompt = prompt_english.format(question=question)

        llm_response = llm.invoke(prompt).content
        print(llm_response)
        serializer.validated_data["details_modified"] = llm_response

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
