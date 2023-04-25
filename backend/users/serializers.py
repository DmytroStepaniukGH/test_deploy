from rest_framework import serializers
from .models import Appointment, Doctor, DoctorUnavailableTime, Specialization, Media
from reviews.models import Review # noqa


class AppointmentSerializer(serializers.ModelSerializer):
    # user_id = serializers.SerializerMethodField()
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
            #'user_id',
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

    # def get_user_id(self, obj):
    #     user_id = self.context['request'].user.id
    #     return user_id


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
    email = serializers.CharField(source='user.email')
    specialization = serializers.CharField(source='specialization.name')
    rating = serializers.SerializerMethodField('get_average_rating')

    def get_average_rating(self, obj):
        reviews_rating = Review.objects.filter(doctor_id=obj.id).values_list('review_rating', flat=True)
        rating_avg = 0
        if reviews_rating:
            rating_avg = round(sum(reviews_rating) / len(reviews_rating), 2)
        return rating_avg

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


class SpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('name', 'image')


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