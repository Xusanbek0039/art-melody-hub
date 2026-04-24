from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import (
    TheoryLevel, TheoryTopic, TheoryTest, Question, Choice,
    TestAttempt, Answer, TheoryResource, UserProgress, StudySession
)
from .serializers import (
    TheoryLevelSerializer, TheoryTopicSerializer, TheoryTopicDetailSerializer,
    TheoryTestSerializer, QuestionSerializer, TestAttemptSerializer,
    TheoryResourceSerializer, UserProgressSerializer, StudySessionSerializer,
    SubmitTestSerializer, SimpleTheoryTestSerializer
)


class TheoryLevelListCreateView(generics.ListCreateAPIView):
    """List and create theory levels"""
    queryset = TheoryLevel.objects.all()
    serializer_class = TheoryLevelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TheoryLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a theory level"""
    queryset = TheoryLevel.objects.all()
    serializer_class = TheoryLevelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TheoryTopicListCreateView(generics.ListCreateAPIView):
    """List and create theory topics"""
    serializer_class = TheoryTopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = TheoryTopic.objects.select_related('level').prefetch_related('resources', 'tests')
        
        # Filter by level
        level_id = self.request.query_params.get('level')
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('level', 'order')


class TheoryTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a theory topic"""
    queryset = TheoryTopic.objects.select_related('level').prefetch_related('resources', 'tests')
    serializer_class = TheoryTopicDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TheoryTestListCreateView(generics.ListCreateAPIView):
    """List and create theory tests"""
    serializer_class = TheoryTestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SimpleTheoryTestSerializer
        return TheoryTestSerializer

    def get_queryset(self):
        queryset = TheoryTest.objects.select_related('level', 'topic').prefetch_related('questions')
        
        # Filter by level
        level_id = self.request.query_params.get('level')
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        
        # Filter by topic
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('level', 'created_at')


class TheoryTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a theory test"""
    queryset = TheoryTest.objects.select_related('level', 'topic').prefetch_related('questions__choices')
    serializer_class = TheoryTestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_test_questions(request, pk):
    """Get questions for a test (without correct answers)"""
    try:
        test = TheoryTest.objects.get(pk=pk, is_active=True)
        
        # Check if user can attempt this test
        attempts_count = TestAttempt.objects.filter(user=request.user, test=test).count()
        if attempts_count >= test.max_attempts:
            return Response({'error': 'Maximum attempts reached'}, status=status.HTTP_400_BAD_REQUEST)
        
        questions = test.questions.prefetch_related('choices').order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        
        # Remove correct answers from choices
        data = serializer.data
        for question in data:
            for choice in question['choices']:
                choice.pop('is_correct', None)
        
        return Response(data)
    
    except TheoryTest.DoesNotExist:
        return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_test(request, pk):
    """Submit test answers"""
    try:
        test = TheoryTest.objects.get(pk=pk, is_active=True)
        
        # Check if user can attempt this test
        attempts_count = TestAttempt.objects.filter(user=request.user, test=test).count()
        if attempts_count >= test.max_attempts:
            return Response({'error': 'Maximum attempts reached'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SubmitTestSerializer(data=request.data)
        if serializer.is_valid():
            answers_data = serializer.validated_data['answers']
            
            # Create test attempt
            attempt_number = attempts_count + 1
            attempt = TestAttempt.objects.create(
                user=request.user,
                test=test,
                score=0,
                total_points=0,
                earned_points=0,
                started_at=timezone.now(),
                attempt_number=attempt_number
            )
            
            # Process answers
            total_points = 0
            earned_points = 0
            
            for answer_data in answers_data:
                question = Question.objects.get(id=answer_data['question_id'], test=test)
                total_points += question.points
                
                # Check answer
                is_correct = False
                points_earned = 0
                
                if question.question_type in ['multiple_choice', 'true_false']:
                    selected_choice_id = answer_data.get('selected_choice_id')
                    if selected_choice_id:
                        try:
                            selected_choice = Choice.objects.get(id=selected_choice_id, question=question)
                            is_correct = selected_choice.is_correct
                            if is_correct:
                                points_earned = question.points
                        except Choice.DoesNotExist:
                            pass
                
                elif question.question_type == 'fill_blank':
                    text_answer = answer_data.get('text_answer', '').strip().lower()
                    # This is a simplified check - in production, you'd want more sophisticated matching
                    correct_choice = question.choices.filter(is_correct=True).first()
                    if correct_choice and text_answer == correct_choice.choice_text.strip().lower():
                        is_correct = True
                        points_earned = question.points
                
                # Save answer
                answer = Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice_id=answer_data.get('selected_choice_id'),
                    text_answer=answer_data.get('text_answer', ''),
                    is_correct=is_correct,
                    points_earned=points_earned
                )
                
                earned_points += points_earned
            
            # Calculate final score
            score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
            is_passed = score_percentage >= test.passing_score
            
            # Update attempt
            attempt.total_points = total_points
            attempt.earned_points = earned_points
            attempt.score = int(score_percentage)
            attempt.is_passed = is_passed
            attempt.completed_at = timezone.now()
            attempt.save()
            
            # Update user progress
            if test.topic:
                progress, created = UserProgress.objects.get_or_create(
                    user=request.user,
                    topic=test.topic,
                    defaults={
                        'completion_percentage': score_percentage if is_passed else 0,
                        'is_completed': is_passed
                    }
                )
                
                if not created and is_passed:
                    progress.completion_percentage = max(progress.completion_percentage, score_percentage)
                    progress.is_completed = True
                    progress.save()
            
            return Response(TestAttemptSerializer(attempt).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except TheoryTest.DoesNotExist:
        return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)


class TestAttemptListCreateView(generics.ListCreateAPIView):
    """List and create test attempts"""
    serializer_class = TestAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user).select_related(
            'test', 'test__level'
        ).prefetch_related('answers__question')


class TestAttemptDetailView(generics.RetrieveAPIView):
    """Retrieve test attempt details"""
    serializer_class = TestAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user).select_related(
            'test', 'test__level'
        ).prefetch_related('answers__question')


class TheoryResourceListCreateView(generics.ListCreateAPIView):
    """List and create theory resources"""
    serializer_class = TheoryResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = TheoryResource.objects.select_related('topic').all()
        
        # Filter by topic
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        
        # Filter by resource type
        resource_type = self.request.query_params.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        # Filter by free status
        is_free = self.request.query_params.get('free')
        if is_free == 'true':
            queryset = queryset.filter(is_free=True)
        
        return queryset.order_by('-created_at')


class TheoryResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a theory resource"""
    queryset = TheoryResource.objects.select_related('topic')
    serializer_class = TheoryResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserProgressListCreateView(generics.ListCreateAPIView):
    """List and create user progress"""
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related('topic', 'topic__level')

    def perform_create(self, serializer):
        topic_id = serializer.validated_data.get('topic_id')
        try:
            topic = TheoryTopic.objects.get(id=topic_id)
            progress, created = UserProgress.objects.get_or_create(
                user=self.request.user,
                topic=topic,
                defaults=serializer.validated_data
            )
            
            if not created:
                # Update existing progress
                for key, value in serializer.validated_data.items():
                    if key != 'topic_id':
                        setattr(progress, key, value)
                progress.save()
            
            return progress
        except TheoryTopic.DoesNotExist:
            raise serializers.ValidationError({'topic_id': 'Topic not found'})


class UserProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete user progress"""
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related('topic', 'topic__level')


class StudySessionListCreateView(generics.ListCreateAPIView):
    """List and create study sessions"""
    serializer_class = StudySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user).select_related('topic')

    def perform_create(self, serializer):
        # Update user's total study time
        duration = serializer.validated_data.get('duration_minutes', 0)
        if duration > 0:
            topic_id = serializer.validated_data.get('topic_id')
            if topic_id:
                try:
                    topic = TheoryTopic.objects.get(id=topic_id)
                    progress, created = UserProgress.objects.get_or_create(
                        user=self.request.user,
                        topic=topic,
                        defaults={
                            'time_spent_minutes': duration,
                            'completion_percentage': min(100, duration * 2)  # Simple logic
                        }
                    )
                    
                    if not created:
                        progress.time_spent_minutes += duration
                        progress.completion_percentage = min(100, progress.time_spent_minutes * 2)
                        progress.save()
                except TheoryTopic.DoesNotExist:
                    pass
        
        serializer.save(user=self.request.user)


class StudySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a study session"""
    serializer_class = StudySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user).select_related('topic')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def theory_stats(request):
    """Get user's theory learning statistics"""
    total_topics = TheoryTopic.objects.filter(is_active=True).count()
    completed_topics = UserProgress.objects.filter(user=request.user, is_completed=True).count()
    total_study_time = StudySession.objects.filter(user=request.user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0
    
    # Test statistics
    total_attempts = TestAttempt.objects.filter(user=request.user).count()
    passed_tests = TestAttempt.objects.filter(user=request.user, is_passed=True).count()
    best_score = TestAttempt.objects.filter(user=request.user).order_by('-score').first()
    avg_score = TestAttempt.objects.filter(user=request.user).aggregate(
        avg_score=Avg('score')
    )['avg_score'] or 0
    
    # Progress by level
    progress_by_level = UserProgress.objects.filter(
        user=request.user
    ).values('topic__level__name').annotate(
        completed=Count('id', filter=Q(is_completed=True)),
        total=Count('id'),
        avg_completion=Avg('completion_percentage')
    ).order_by('topic__level__order')
    
    return Response({
        'total_topics': total_topics,
        'completed_topics': completed_topics,
        'completion_rate': (completed_topics / total_topics * 100) if total_topics > 0 else 0,
        'total_study_time_minutes': total_study_time,
        'total_study_time_hours': total_study_time // 60,
        'total_attempts': total_attempts,
        'passed_tests': passed_tests,
        'best_score': best_score.score if best_score else 0,
        'average_score': round(avg_score, 2),
        'progress_by_level': list(progress_by_level)
    })
