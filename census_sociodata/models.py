# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers


# Create your models here.
class NycCensusSociodata(models.Model):
    tractid = models.CharField(primary_key=True)
    transit_total = models.IntegerField()
    transit_private = models.IntegerField()
    transit_public = models.IntegerField()
    transit_walk = models.IntegerField()
    transit_other = models.IntegerField()
    transit_none = models.IntegerField()
    transit_time_mins = models.FloatField()
    family_count = models.IntegerField()
    family_income_median = models.IntegerField()
    family_income_mean = models.IntegerField()
    family_income_aggregate = models.IntegerField()
    edu_total = models.IntegerField()
    edu_no_highschool_dipl = models.IntegerField()
    edu_highschool_dipl = models.IntegerField()
    edu_college_dipl = models.IntegerField()
    edu_graduate_dipl = models.IntegerField()

    class Meta:
        db_table = 'nyc_census_sociodata'

class NycCensusSociodataSerializer(serializers.ModelSerializer):

    class Meta:
        model = NycCensusSociodata
        fields = ('tractid', 'transit_total', 'transit_private', 'transit_public', 'transit_walk', 'transit_other', 'transit_none',
                  'transit_time_mins', 'family_count', 'family_income_median', 'family_income_mean', 'family_income_aggregate',
                  'edu_total', 'edu_no_highschool_dipl', 'edu_highschool_dipl', 'edu_college_dipl', 'edu_graduate_dipl')  # Add the additional field
