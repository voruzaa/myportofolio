from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "description",
            "started_at",
            "ended_at",
            "is_ongoing",
            "star_count",
            "is_starred",
        ]
        read_only_fields = ["id", "is_ongoing", "star_count", "is_starred"]

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if not request or not request.user:
            return False
        user = request.user
        return bool(user.is_authenticated and obj.starred_by.filter(pk=user.pk).exists())

    def validate_institution(self, value):
        institution = strip_tags(value).strip()
        if not institution:
            raise serializers.ValidationError("Institusi tidak boleh hanya berisi tag HTML.")
        return institution

    def validate_degree(self, value):
        degree = strip_tags(value).strip()
        if not degree:
            raise serializers.ValidationError("Gelar / program studi tidak boleh hanya berisi tag HTML.")
        return degree

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started_at = attrs.get("started_at")
        ended_at = attrs.get("ended_at")

        if self.instance is not None:
            if started_at is None:
                started_at = self.instance.started_at
            if ended_at is None and "ended_at" not in attrs:
                ended_at = self.instance.ended_at

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."}
            )
        return attrs


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
            "star_count",
            "is_starred",
        ]
        read_only_fields = ["id", "star_count", "is_starred"]

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if not request or not request.user:
            return False
        user = request.user
        return bool(user.is_authenticated and obj.starred_by.filter(pk=user.pk).exists())

    def validate_title(self, value):
        title = strip_tags(value).strip()
        if not title:
            raise serializers.ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()
