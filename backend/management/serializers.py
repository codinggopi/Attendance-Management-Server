from rest_framework import serializers
from .models import Student, Teacher, Course, AttendanceRecord

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacherId = serializers.PrimaryKeyRelatedField(source='teacher', queryset=Teacher.objects.all())
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacherId', 'students']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
