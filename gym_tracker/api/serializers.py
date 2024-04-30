from rest_framework import serializers

from main.models import CustomUser, FinishedTraining, Training


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%d.%m.%Y', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'date_joined', 'photo', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class FinishedTrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinishedTraining
        fields = ('started_at', 'finished_at', )


class TrainingSerializer(serializers.ModelSerializer):
    finished_trainings = serializers.SerializerMethodField()

    def get_finished_trainings(self, obj):
        finished_trainings = obj.finished_trainings.order_by('-started_at').first()
        if finished_trainings:
            return {'started_at': finished_trainings.started_at}

    class Meta:
        model = Training
        fields = ('id', 'name', 'finished_trainings')
