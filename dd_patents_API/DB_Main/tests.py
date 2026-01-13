from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class HealthCheckTest(TestCase):
    def test_health_check(self):
        """
        Ensures the health check endpoint is working.
        """
        url = reverse('health_check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
