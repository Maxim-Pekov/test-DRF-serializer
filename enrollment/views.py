from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Participant
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField


class ApplicationSerializer(Serializer):
    contact_phone = CharField()
    ticket_type = CharField()


def validate(data):
    serializer = ApplicationSerializer(data=data)
    serializer.is_valid(raise_exception=True)


@api_view(['POST'])
def enroll(request):
    validate(request.data)

    participants = request.data.get('participants', [])  # TODO validate data!

    application = Application.objects.create(
        contact_phone=str(request.data['contact_phone']),
        ticket_type=str(request.data['ticket_type']),
    )

    participants = [Participant(application=application, **fields) for fields in participants]
    Participant.objects.bulk_create(participants)

    return Response({
        'application_id': application.id,
    })
