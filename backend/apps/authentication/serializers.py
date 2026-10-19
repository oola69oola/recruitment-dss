from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'RECRUITER')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(required=False)
        self.fields['email'] = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        identifier = attrs.get('username') or attrs.get('email') or ''
        password = attrs.get('password')

        if not identifier:
            raise serializers.ValidationError({"detail": "Username or email is required."})

        # Allow username like 'admin', 'recruiter', or full email
        clean_id = identifier.strip().lower()
        if '@' not in clean_id:
            target_email = f"{clean_id}@recruitiq.io"
        else:
            target_email = clean_id

        # Auto-provision canonical recruiter user if it doesn't exist yet
        user = User.objects.filter(email=target_email).first()
        if not user:
            if clean_id in ['recruiter', 'admin', 'hr', 'recruiter@recruitiq.io', 'admin@recruitiq.io']:
                user = User.objects.create_user(
                    email=target_email,
                    password='recruitiq2026',
                    first_name="Lead",
                    last_name="Recruiter",
                    role="RECRUITER"
                )

        attrs['email'] = target_email
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
