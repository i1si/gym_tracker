from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Func, Q
from django.db.models.functions import ExtractYear
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.serializers import NewFinishedExerciseSerializer, NewTrainingSerializer, TrainingSerializer, UserSerializer
from main.models import CustomUser, FinishedExerciseSet, Training, FinishedTraining, Exercise


class UserInfoViewSet(CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, args, kwargs)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return response


@api_view(["POST"])
def login_view(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user:
        login(request, user)
        return Response({"success": True}, status=status.HTTP_200_OK)
    return Response({"success": False, "err": "Неверный логин или пароль"}, status=status.HTTP_401_UNAUTHORIZED)


class TrainingViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Training.objects.filter(owner=self.request.user).order_by('id')
        serializer = TrainingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = NewTrainingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        training = Training.objects.create(name=serializer.validated_data['name'], owner=self.request.user)
        for exercise in serializer.validated_data['exercises']:
            Exercise.objects.create(name=exercise['name'], training=training)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class FinishedExerciseViewSet(ViewSet):
    permission_classes (IsAuthenticated, )

    def create(self, request):
        serializer = NewFinishedExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        finished_training, created = FinishedTraining.objects.get_or_create(training_id=serializer.validated_data['training_id'])
        exercise = Exercise.objects.get(pk=serializer.validated_data['exercise_id'])
        for finished_exercise in serializer.validated_data['finished_exercises']:
            FinishedExerciseSet.objects.create(training=finished_training, exercise=exercise, **finished_exercise)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
    
    def retrieve(self, request):
        ...


# class FinishedTrainingSet(CreateModelMixin, ListModelMixin, GenericViewSet):
#     serializer_class = FinishedTrainingSerializer
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         if self.request.query_params.get('last', None):
#             queryset = FinishedTraining.objects.filter(
#                 training__owner=self.request.user
#             ).order_by('training', '-started_at').distinct('training')
#         else:
#             queryset = FinishedTraining.objects.filter(training__owner=self.request.user)
#         return queryset
