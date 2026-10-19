from rest_framework import serializers
from .models import EvaluationResult, HRActivityLog

class EvaluationResultSerializer(serializers.ModelSerializer):
    candidate_identifier = serializers.CharField(source='submission.candidate_identifier', read_only=True)
    candidate_name = serializers.CharField(source='submission.candidate_name', read_only=True)
    candidate_email = serializers.CharField(source='submission.candidate_email', read_only=True)
    candidate_phone = serializers.CharField(source='submission.candidate_phone', read_only=True)
    raw_file_name = serializers.CharField(source='submission.raw_file_name', read_only=True)
    job_id = serializers.UUIDField(source='submission.job_id', read_only=True)
    previous_rank = serializers.SerializerMethodField()
    rank_delta = serializers.SerializerMethodField()

    def get_previous_rank(self, obj):
        return (obj.shap_attributions or {}).get('previous_rank')

    def get_rank_delta(self, obj):
        return (obj.shap_attributions or {}).get('rank_delta', 0)

    class Meta:
        model = EvaluationResult
        fields = [
            'id',
            'job_id',
            'candidate_identifier',
            'candidate_name',
            'candidate_email',
            'candidate_phone',
            'raw_file_name',
            'rank_position',
            'previous_rank',
            'rank_delta',
            'is_shortlisted',
            'shortlist_status',
            'funnel_stage',
            'hard_skill_score',
            'soft_skill_score',
            'title_proximity_score',
            'duration_score',
            'stability_score',
            'experience_composite_score',
            'education_score',
            'final_weighted_score',
            'shap_attributions',
            'plain_english_summary',
            'skill_gaps',
            'evaluated_at',
        ]
        read_only_fields = ['id', 'evaluated_at']


class HRActivityLogSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = HRActivityLog
        fields = [
            'id',
            'hr_name',
            'hr_email',
            'hr_organization',
            'action_type',
            'description',
            'job_title',
            'stage',
            'candidate_count',
            'metadata',
            'created_at',
            'created_at_formatted',
        ]
        read_only_fields = ['id', 'created_at']

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%b %d, %Y • %H:%M:%S')
