from rest_framework import serializers

from .models import (email, recipient, subject)


class EmailSerializer(serializers.ModelSerializer):
    recipients = serializers.SlugRelatedField(
        many=True, slug_field='email_address',
        queryset=recipient.objects.all())
    subject = serializers.SlugRelatedField(slug_field='subject',
                                           queryset=subject.objects.all(), )
    template_inputs = serializers.SerializerMethodField('get_template_inputs')

    class Meta:
        model = email
        fields = ['recipients', 'subject', 'template_inputs']

    def get_template_inputs(self, email):
        template_inputs = email.template_type.template_inputs
        return template_inputs
