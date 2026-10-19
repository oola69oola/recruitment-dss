from rest_framework import serializers
from .models import CandidateSubmission

class CandidateSubmissionSerializer(serializers.ModelSerializer):
    evaluation = serializers.SerializerMethodField()

    class Meta:
        model = CandidateSubmission
        fields = [
            'id',
            'job',
            'candidate_identifier',
            'candidate_name',
            'candidate_email',
            'candidate_phone',
            'raw_file',
            'raw_file_name',
            'is_english',
            'rejection_reason',
            'original_text',
            'anonymized_text',
            'extracted_features',
            'processing_status',
            'uploaded_at',
            'evaluation',
        ]
        read_only_fields = ['id', 'uploaded_at', 'evaluation']

    def get_evaluation(self, obj):
        if hasattr(obj, 'evaluation'):
            from apps.evaluations.serializers import EvaluationResultSerializer
            return EvaluationResultSerializer(obj.evaluation).data
        return None
