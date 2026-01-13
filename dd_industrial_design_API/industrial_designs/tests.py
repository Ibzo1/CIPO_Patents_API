from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import skipIfDBFeature

@skipIfDBFeature('supports_transactions')
class IDSmokeTests(APITestCase):
    schema = "id_csv_2024_03_07"

    # 1 pagination
    def test_application_main_pagination(self):
        url = reverse("id_main-list")
        resp = self.client.get(url, {"page": 1, "page_size": 5})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(resp.data["results"]), 5)

    # 2 filtering – exact
    def test_application_classification_exact(self):
        sample_app_no = "99989"
        url = reverse("id_classification-list")
        resp = self.client.get(url, {"application_number": sample_app_no})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for row in resp.data["results"]:
            self.assertEqual(row["application_number"], sample_app_no)

    # 3 filtering – range
    def test_application_main_range(self):
        url = reverse("id_main-list")
        resp = self.client.get(
            url, {"filing_date_after": "2015-01-01", "filing_date_before": "2015-12-31"}
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for row in resp.data["results"]:
            self.assertTrue("2015-01-01" <= row["filing_date"] <= "2015-12-31")

    # 4 search
    def test_assignment_ip_search(self):
        kw = "Assignee"
        url = reverse("id_assignment_interested_party-list")
        resp = self.client.get(url, {"search": kw})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # 5 detail view
    def test_assignment_main_detail(self):
        pk = "5000"
        url = reverse("id_assignment_main-detail", args=[pk])
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND))
