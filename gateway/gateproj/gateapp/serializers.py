from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    year = serializers.DecimalField(max_digits=4, decimal_places=0)

    def create(self, validated_data):
        return validated_data
