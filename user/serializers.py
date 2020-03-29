from django.contrib.auth import authenticate

from user.models import UserInfo

from rest_framework import serializers
from JtgMoviePlanner import settings
import uuid
from JtgMoviePlanner.tasks import send_verify_email_task


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['email', 'first_name', 'last_name', 'password', 'gender','is_admin']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_admin']

        
    def create(self, validated_data):
        password = validated_data.get('password')
        email = validated_data.get('email')
        instance = super(SignUpSerializer, self).create(validated_data)
        email_subject = "JtgMoviePlanner Email Verification"

        if password is not None:
            instance.set_password(password)
            emailtoken = uuid.uuid4()
            instance.email_token = emailtoken
            token = str(emailtoken)
            send_verify_email_task.delay(email_subject, email, token)
            instance.save()
            return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                msg = ['Unable to Login with Provided Credentials.']
                raise serializers.ValidationError(msg, code='authorization')
            else:
                if(not user.is_verified):
                    msg = ['Please verify your Email Id. ']
                    raise serializers.ValidationError(
                        msg, code='authorization')
                else:
                    attrs['user'] = user
                    return attrs
