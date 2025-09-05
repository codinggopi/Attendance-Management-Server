from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Teacher, Course, AttendanceRecord
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, AttendanceRecordSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['delete'], url_path='all')
    def delete_all(self, request):
        """
        Deletes all students.
        """
        Student.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=False, methods=['delete'], url_path='all')
    def delete_all(self, request):
        """
        Deletes all teachers.
        """
        Teacher.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('studentId')
        if not student_id:
            return Response({'error': 'Student ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            
        course.students.add(student)
        return Response(self.get_serializer(course).data)

    @action(detail=False, methods=['delete'], url_path='all')
    def delete_all(self, request):
        """
        Deletes all courses, as requested by the frontend.
        """
        Course.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# This new ViewSet is needed to handle the "deleteAllUsers" call from the frontend
class UserViewSet(viewsets.ViewSet):
    """
    A viewset for handling bulk user-related actions.
    """
    queryset = User.objects.none() 

    @action(detail=False, methods=['delete'], url_path='all')
    def delete_all_users(self, request):
        """
        Deletes all students and teachers, as requested by the frontend.
        """
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
