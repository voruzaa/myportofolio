from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Education
        fields = [
            "id", "institution", "degree", "description", "started_at", "ended_at",
            "is_ongoing", "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institusi tidak boleh hanya berisi tag HTML.")
        return value

    def validate_degree(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Gelar / program studi tidak boleh hanya berisi tag HTML.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()
