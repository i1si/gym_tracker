from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Func, Q
from django.db.models.functions import ExtractYear
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers import UserSerializer, TrainingSerializer, FinishedTrainingSerializer
from main.models import CustomUser, Training, FinishedTraining


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


class TrainingViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = TrainingSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Training.objects.filter(owner=self.request.user).order_by('id')
        return queryset


class FinishedTrainingSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FinishedTrainingSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.query_params.get('last', None):
            queryset = FinishedTraining.objects.filter(
                training__owner=self.request.user
            ).order_by('training', '-started_at').distinct('training')
        else:
            queryset = FinishedTraining.objects.filter(training__owner=self.request.user)
        return queryset
