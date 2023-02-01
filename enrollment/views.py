from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Participant
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['contact_phone', 'ticket_type']

class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email']


@api_view(['POST'])
def enroll(request):
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    participants = request.data.get('participants', [])  # TODO validate data!

    if not isinstance(participants, list):
        raise ValidationError('Expects participants field be a list')

    for fields in participants:
        serializer = ParticipantSerializer(data=fields)
        serializer.is_valid(raise_exception=True)  # выкинет ValidationError

