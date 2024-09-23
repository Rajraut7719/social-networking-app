from rest_framework import serializers
from users_app.models import User

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, row_email):
        get_email = User.objects.filter(email__iexact=row_email).exists()
        if get_email:
            raise serializers.ValidationError("Email already exist")
        return row_email

    def create(self, validated_data):
        try:
            User.objects.create_user(**validated_data)
        except Exception as e:
            print(f"{e = }")
        return User(**validated_data)

class GetUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('user_id','username','email')
