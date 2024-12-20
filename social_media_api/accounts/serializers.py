from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # Include CharField for password and confirmation
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture']

    def validate(self, attrs):
        """
        Ensure passwords match and perform custom validation.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Create a user using `get_user_model().objects.create_user`.
        """
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user


from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'date_of_birth', 'profile_photo']  # Adjust fields as necessary



class LoginSerializer(serializers.Serializer):
    # CharField for login credentials
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        Validate user credentials.
        """
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        raise serializers.ValidationError("Invalid username or password.")




# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8, required=True)
#     confirm_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture']

#     def validate(self, attrs):
#         if attrs['password'] != attrs['confirm_password']:
#             raise serializers.ValidationError({"password": "Passwords do not match!"})
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop('confirm_password')  # Remove confirm_password before creating user
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             bio=validated_data.get('bio', ''),
#             profile_picture=validated_data.get('profile_picture', None)
#         )
#         # Create a token for the newly registered user
#         Token.objects.create(user=user)
#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         user = User.objects.filter(username=username).first()
#         if user and user.check_password(password):
#             return user
#         raise serializers.ValidationError("Invalid username or password!")


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'bio', 'profile_picture', 'followers']
