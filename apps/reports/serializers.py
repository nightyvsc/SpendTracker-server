from rest_framework import serializers

class DateRangeOptionalSerializer(serializers.Serializer):
    start = serializers.DateField(required=False)
    end = serializers.DateField(required=False)

    def validate(self, data):
        start = data.get("start")
        end = data.get("end")
        if start and end and start > end:
            raise serializers.ValidationError("start debe ser <= end")
        return data


class SummaryQuerySerializer(DateRangeOptionalSerializer):
    daily_limit = serializers.IntegerField(required=False, min_value=1, max_value=31, default=7)
    monthly_limit = serializers.IntegerField(required=False, min_value=1, max_value=24, default=6)


class ByCategoryQuerySerializer(DateRangeOptionalSerializer):
    include_uncategorized = serializers.BooleanField(required=False, default=True)
    top_n = serializers.IntegerField(required=False, min_value=1, max_value=100)


class TrendQuerySerializer(DateRangeOptionalSerializer):
    granularity = serializers.ChoiceField(choices=["day", "week", "month"], default="week")
