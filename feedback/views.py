from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Feedback
from .forms import FeedbackForm

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'url', 'body', 'email', 'rating', 'user_agent', 'created_at']


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        serializer = FeedbackSerializer(data=request.data)

        user_agent = request.data.get('user_agent')
        if not user_agent:
            user_agent = request.META.get('HTTP_USER_AGENT', None)

        if serializer.is_valid():
            serializer.save(user_agent=user_agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


@method_decorator(xframe_options_exempt, name='dispatch')
class FeedbackCreate(CreateView):
    form_class = FeedbackForm
    model = Feedback
    success_url = reverse_lazy('feedback-thankyou')
