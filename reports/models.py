from django.db import models


class IAACR(models.Model):


    drug_name = models.CharField(max_length=255)
    drug_code = models.CharField(max_length=255)

    def __str__(self):
        return self.drug_name

class FacilityDropdown(models.Model):


    facility_name = models.CharField(max_length=255)
    facility_code = models.CharField(max_length=255)

    def __str__(self):
        return self.facility_name
