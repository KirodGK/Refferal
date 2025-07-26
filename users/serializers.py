from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone', 'invite_code', 'referred_by', 'referrals']

    def get_referrals(self, obj):
        return [u.phone for u in obj.referrals.all()]
