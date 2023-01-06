import rsa
from rest_framework import serializers
from .models import User, RequestsCounter, Profile
from .models import Collection
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .password_vulnrability_tasks import WebhookTriggers


class LoginUserSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginUserSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'password2')
        extra_kwargs = {
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        import bcrypt
        password = validated_data['password']
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user.set_password(validated_data['password'])
        user.save()
        WebhookTriggers().trigger_password_vulnerability_test_(validated_data['username'],
                                                               validated_data['email'], )
        user_profile = Profile.objects.create(
            user=user,
            hash_key=hashed_password
        )
        user_profile.save()
        return user


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('title', 'description', 'genres', 'uuid', 'collection_name', 'collection_description', 'user',
                  'collection_uuid')


class RequestCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestsCounter
        fields = '__all__'


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
