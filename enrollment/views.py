from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Participant
from rest_framework.serializers import ValidationError


def validate(data):
    errors = []
    if 'contact_phone' not in data:
        errors.append('Contact phone field is required.')

    if 'ticket_type' not in data:
        errors.append('Ticket type field is required.')
    # TODO check if ticket_type is one of available choices

    if errors:
        raise ValidationError(errors)


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
