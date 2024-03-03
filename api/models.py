from django.db import models


class Organization(models.Model):
    property_code = models.CharField(max_length=20, unique=True)  # Ensure unique property code
    property_name = models.CharField(max_length=255)
    arrival_time = models.TimeField(null=True, blank=True)  # Optional arrival time
    departure_time = models.TimeField(null=True, blank=True)  # Optional departure time

    # **Do not store sensitive information directly in the model:**
    # third_party_api_token = models.CharField(max_length=255)
    # third_party_api_url = models.URLField()

    def __str__(self):
        return self.property_code +' - '+ self.property_name