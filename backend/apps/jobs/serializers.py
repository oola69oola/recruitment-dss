from rest_framework import serializers
from .models import JobPosting

class JobPostingSerializer(serializers.ModelSerializer):
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = [
            'id',
            'title',
            'description',
            'required_hard_skills',
            'required_soft_skills',
            'target_tenure_years',
            'target_tenure_range',
            'required_education_level',
            'weight_vector',
            'anonymization_rules',
            'is_archived',
            'created_at',
            'updated_at',
            'submission_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'submission_count']

    def get_submission_count(self, obj):
        return obj.submissions.count()

    def validate_weight_vector(self, value):
        required_keys = {'w_h', 'w_s', 'w_t', 'w_e', 'w_d'}
        if not required_keys.issubset(value.keys()):
            raise serializers.ValidationError(f"Weights must include: {required_keys}")
        
        # Verify non-negative
        for k, v in value.items():
            if not isinstance(v, (int, float)) or v < 0:
                raise serializers.ValidationError(f"Weight '{k}' must be non-negative.")
        
        total = sum(float(value[k]) for k in required_keys)
        if total <= 0:
            raise serializers.ValidationError("Sum of weights must be greater than 0.")
        
        # Normalize to simplex (sum to 1.0)
        normalized = {k: round(float(value[k]) / total, 4) for k in required_keys}
        return normalized

