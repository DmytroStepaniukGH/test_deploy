from rest_framework import serializers
from users.models import Appointment, Doctor, DoctorUnavailableTime, Specialization, Media


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.user.get_full_name')
    patient_id = serializers.IntegerField(source='patient.id')
    doctor = serializers.CharField(source='doctor.user.get_full_name')
    price = serializers.CharField(source='doctor.price')
    phone_num = serializers.CharField(source='patient.user.phone_num')
    specialization = serializers.CharField(source='doctor.specialization.name')
    card_id = serializers.CharField(source='patient.card.card_id')

    class Meta:
        model = Appointment
        fields = (
            'id',
            'date',
            'time',
            'price',
            'patient',
            'patient_id',
            'phone_num',
            'card_id',
            'doctor',
            'specialization',
            'status',
            'medical_history',
            'objective_status',
            'diagnosis',
            'examination',
            'recommendations'
        )


class CloseAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'id',
            'medical_history',
            'objective_status',
            'diagnosis',
            'examination',
            'recommendations'
        )


class DoctorListSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source='user.last_name')
    first_name = serializers.CharField(source='user.first_name')
    patronim_name = serializers.CharField(source='user.patronim_name')
    profile_image = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email')
    specialization = serializers.CharField(source='specialization.name')
    education = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    procedures_performed = serializers.SerializerMethodField()
    rating = serializers.FloatField()

    class Meta:
        model = Doctor
        fields = (
            'id',
            'email',
            'profile_image',
            'last_name',
            'first_name',
            'patronim_name',
            'specialization',
            'price',
            'category',
            'experience',
            'info',
            'education',
            'courses',
            'procedures_performed',
            'rating',
        )

    def get_profile_image(self, doctor_info):
        request = self.context.get('request')
        profile_image_url = doctor_info.profile_image.url
        return request.build_absolute_uri(profile_image_url)

    def get_education(self, obj):
        return obj.education.split('\\n')

    def get_courses(self, obj):
        return obj.courses.split('\\n')

    def get_procedures_performed(self, obj):
        return obj.procedures_performed.split('\\n')


class SpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = (
            'id',
            'name',
            'image',
        )


class SearchSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source='user.last_name')
    specialization = serializers.CharField(source='doctor.specialization.name')

    class Meta:
        model = Doctor
        fields = (
            'id',
            'last_name',
            'specialization'
        )


class SetUnavailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorUnavailableTime
        fields = (
            'id',
            'doctor',
            'date',
            'time',
        )


class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'id',
            'doctor',
            'date',
            'time',
        )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'id',
            'file',
        )
        read_only_fields = ('id',)