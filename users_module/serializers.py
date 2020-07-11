from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers


from users_module.models import User


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    employee_id = serializers.CharField(max_length=100)


    def validate_employee_id(self, employee_id):
        if employee_id in User.objects.all().values_list('employee_id', flat=True):
            raise serializers.ValidationError("A user with that employee_id already exists.")
        return employee_id

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'employee_id': self.validated_data.get('employee_id', ''),
        }

    def custom_signup(self, request, user):
        user.employee_id = self.get_cleaned_data().get("employee_id")
        user.save()
