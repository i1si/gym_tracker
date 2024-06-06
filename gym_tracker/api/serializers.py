from rest_framework import serializers

import main.models as main_m


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%d.%m.%Y', read_only=True)

    class Meta:
        model = main_m.CustomUser
        fields = ('username', 'first_name', 'date_joined', 'photo', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = main_m.CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class TrainingSerializer(serializers.ModelSerializer):
    finished_trainings = serializers.SerializerMethodField()

    def get_finished_trainings(self, obj):
        finished_trainings = obj.finished_trainings.order_by('-started_at').first()
        if finished_trainings:
            return {'started_at': finished_trainings.started_at}

    class Meta:
        model = main_m.Training
        fields = ('id', 'name', 'finished_trainings')


class NewExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = main_m.Exercise
        fields = ('name', )


class NewTrainingSerializer(serializers.ModelSerializer):
    exercises = NewExerciseSerializer(many=True)

    class Meta:
        model = main_m.Training
        fields = ('name', 'exercises', )


class FinishedExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = main_m.FinishedExerciseSet
        fields = ('set', 'weight', 'repetitions', )


class NewFinishedExerciseSerializer(serializers.Serializer):
    training_id = serializers.IntegerField()
    exercise_id = serializers.IntegerField()
    finished_sets = FinishedExerciseSerializer(many=True)


class ExerciseQueryParamsParser(serializers.Serializer):
    tID = serializers.IntegerField()
    eID = serializers.IntegerField(required=False)


class FinishedTrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = main_m.FinishedTraining
        fields = ('training', 'started_at', 'finished_at', )


class FinishedRunningSerialiser(serializers.ModelSerializer):

    class Meta:
        model = main_m.FinishedRunning
        fields = ('distance', 'duration', )
