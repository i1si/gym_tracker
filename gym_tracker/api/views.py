from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

import api.serializers as api_s
import main.models as main_m


class UserInfoViewSet(CreateModelMixin, GenericViewSet):
    queryset = main_m.CustomUser.objects.all()
    serializer_class = api_s.UserSerializer

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
        queryset = main_m.Training.objects.filter(owner=self.request.user).order_by('id')
        serializer = api_s.TrainingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = api_s.NewTrainingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        training = main_m.Training.objects.create(name=serializer.validated_data['name'], owner=self.request.user)
        for exercise in serializer.validated_data['exercises']:
            main_m.Exercise.objects.create(name=exercise['name'], training=training)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class FinishedExerciseViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        serializer = api_s.NewFinishedExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        finished_training, created = main_m.FinishedTraining.objects.get_or_create(
            training_id=serializer.validated_data['training_id'], finished_at=None
        )
        if created:
            finished_training.started_at = timezone.now()
            finished_training.save()
        exercise = main_m.Exercise.objects.get(pk=serializer.validated_data['exercise_id'])
        last_exercise = main_m.Exercise.objects.filter(training_id=serializer.validated_data['training_id']).last()
        if exercise.id == last_exercise.id:
            finished_training.finished_at = timezone.now()
            finished_training.save()
        for finished_set in serializer.validated_data['finished_sets']:
            main_m.FinishedExerciseSet.objects.create(training=finished_training, exercise=exercise, **finished_set)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
    
    def list(self, request):
        """
        If eID is provided, return the exercise next in order after the eID.
        Return the first exercise for training by tID otherwise.
        """
        serializer = api_s.ExerciseQueryParamsParser(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        if 'eID' in serializer.validated_data:
            exercise = main_m.Exercise.objects.filter(
                id__gt=serializer.validated_data['eID'], training_id=serializer.validated_data['tID']
            ).first()
        else:
            exercise = main_m.Exercise.objects.filter(training_id=serializer.validated_data['tID']).first()
        if not exercise:
            return Response({'next': False})
        last_finished_training = main_m.FinishedTraining.objects.filter(training_id=serializer.validated_data['tID']).first()
        last_finished_exercise_sets = main_m.FinishedExerciseSet.objects.filter(training=last_finished_training, exercise=exercise).all()
        return Response({
            'next': True,
            'id': exercise.id, 
            'name': exercise.name,
            'sets': [
                {'set': x.set, 'weight': x.weight, 'repetitions': x.repetitions} for x in last_finished_exercise_sets
            ]
        })


class FinishedTrainingViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        """
        Return all user finished trainings.
        """
        queryset = main_m.FinishedTraining.objects.filter(training__owner=request.user)
        serializer = api_s.FinishedTrainingSerializer(queryset, many=True)
        return Response(serializer.data)
