from rest_framework import serializers


def validate_mobile_number(value):
    if not value.isdigit():
        raise serializers.ValidationError(
            "Mobile number must contain only digits"
        )

    if len(value) != 10:
        raise serializers.ValidationError(
            "Enter a valid 10-digit mobile number"
        )

    return value
