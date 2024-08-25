from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if not self.context['request'].user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
