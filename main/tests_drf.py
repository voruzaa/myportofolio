import uuid

from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Project

VALID_PAYLOAD = {
    "institution": "Universitas Indonesia",
    "degree": "S1 Sistem Informasi",
    "description": "Pendidikan pascasarjana kebanggaan.",
    "started_at": "2025-08-01",
}


class EducationAPITestBase(APITestCase):
    def setUp(self):
        self.list_url = "/api/v1/education/"
        self.editor_group = Group.objects.get_or_create(name="Editor")[0]
        self.visitor_client = APIClient()
        self.regular_client = APIClient()
        self.editor_client = APIClient()
        self.owner_client = APIClient()
        self.regular_user = User.objects.create_user(username="regular", password="rahasia123")
        self.editor_user = User.objects.create_user(username="editor", password="rahasia123")
        self.editor_user.groups.add(self.editor_group)
        self.owner_user = User.objects.create_superuser(
            username="owner", password="rahasia123", email="owner@example.com"
        )
        self.regular_client.force_authenticate(user=self.regular_user)
        self.editor_client.force_authenticate(user=self.editor_user)
        self.owner_client.force_authenticate(user=self.owner_user)
        self.existing_education = Education.objects.create(
            institution="Institut Teknologi Bandung",
            degree="S1 Teknik Informatika",
            description="Sarjana.",
            started_at="2020-08-01",
        )
        self.detail_url = f"{self.list_url}{self.existing_education.id}/"


class EducationAPIListTest(EducationAPITestBase):
    def test_visitor_can_read_list(self):
        response = self.visitor_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["institution"], "Institut Teknologi Bandung")
        self.assertIn("star_count", response.data[0])
        self.assertIn("is_starred", response.data[0])
        self.assertNotIn("email", response.data[0])
        self.assertNotIn("password", response.data[0])

    def test_search_filters_by_institution(self):
        response = self.visitor_client.get(self.list_url, {"institution": "bandung"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["institution"], "Institut Teknologi Bandung")

    def test_visitor_cannot_create(self):
        response = self.visitor_client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_regular_user_cannot_create(self):
        response = self.regular_client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_cannot_create(self):
        response = self.editor_client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_can_create(self):
        response = self.owner_client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)
        self.assertTrue(
            Education.objects.filter(institution="Universitas Indonesia").exists()
        )

    def test_create_with_invalid_payload_returns_400(self):
        response = self.owner_client.post(self.list_url, {"institution": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 1)

    def test_create_strips_html_tags_from_text_fields(self):
        payload = dict(VALID_PAYLOAD)
        payload["institution"] = '<img src="x" onerror="alert(\'XSS!\')">Universitas Indonesia'
        payload["description"] = "<script>alert('XSS!')</script>Pendidikan."
        response = self.owner_client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education = Education.objects.get(pk=response.data["id"])
        self.assertNotIn("<", education.institution)
        self.assertNotIn("script", education.description)
        self.assertEqual(education.institution, "Universitas Indonesia")

    def test_create_with_tags_only_text_is_rejected(self):
        payload = dict(VALID_PAYLOAD)
        payload["institution"] = "<img src=\"x\" onerror=\"alert('XSS!')\">"
        response = self.owner_client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 1)

    def test_create_with_ended_at_before_started_at_returns_400(self):
        payload = dict(VALID_PAYLOAD)
        payload["ended_at"] = "2024-01-01"
        response = self.owner_client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.assertEqual(Education.objects.count(), 1)


class EducationAPIDetailTest(EducationAPITestBase):
    def test_detail_returns_404_for_missing_data(self):
        response = self.owner_client.get(f"{self.list_url}{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_cannot_update_patch(self):
        response = self.visitor_client.patch(
            self.detail_url, {"degree": "S1 Ilmu Komputer"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Teknik Informatika")

    def test_visitor_cannot_update_put(self):
        payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S1 Ilmu Komputer",
            "description": "Perubahan",
            "started_at": "2020-08-01",
        }
        response = self.visitor_client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Teknik Informatika")

    def test_regular_user_cannot_update_patch(self):
        response = self.regular_client.patch(
            self.detail_url, {"degree": "S1 Ilmu Komputer"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Teknik Informatika")

    def test_regular_user_cannot_update_put(self):
        payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S1 Ilmu Komputer",
            "description": "Perubahan",
            "started_at": "2020-08-01",
        }
        response = self.regular_client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Teknik Informatika")

    def test_editor_can_patch(self):
        response = self.editor_client.patch(
            self.detail_url, {"degree": "S1 Ilmu Komputer"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Ilmu Komputer")

    def test_editor_can_put(self):
        payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S1 Sains Data",
            "description": "Perubahan lengkap oleh editor.",
            "started_at": "2020-08-01",
            "ended_at": "2024-07-01",
        }
        response = self.editor_client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S1 Sains Data")

    def test_owner_can_put(self):
        payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S2 Sistem Informasi",
            "description": "Perubahan lengkap oleh owner.",
            "started_at": "2020-08-01",
        }
        response = self.owner_client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_education.refresh_from_db()
        self.assertEqual(self.existing_education.degree, "S2 Sistem Informasi")

    def test_visitor_cannot_delete(self):
        response = self.visitor_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_regular_user_cannot_delete(self):
        response = self.regular_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_cannot_delete(self):
        response = self.editor_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_can_delete(self):
        response = self.owner_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Education.objects.count(), 0)


class EducationAPIStarTest(EducationAPITestBase):
    def test_visitor_cannot_star(self):
        response = self.visitor_client.post(f"{self.detail_url}star/")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(self.existing_education.starred_by.count(), 0)

    def test_regular_user_can_toggle_star(self):
        response = self.regular_client.post(f"{self.detail_url}star/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])

        response = self.regular_client.post(f"{self.detail_url}star/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_star_updates_read_only_fields(self):
        self.regular_client.post(f"{self.detail_url}star/")
        self.owner_client.post(f"{self.detail_url}star/")
        response = self.visitor_client.get(self.list_url)
        self.assertEqual(response.data[0]["star_count"], 2)
        self.assertFalse(response.data[0]["is_starred"])


class EducationAPICSRFTest(APITestCase):
    def setUp(self):
        self.list_url = "/api/v1/education/"
        self.owner = User.objects.create_superuser(
            username="owner", password="rahasia123", email="owner@example.com"
        )
        self.client = APIClient(enforce_csrf_checks=True)

    def test_request_without_csrf_token_is_rejected(self):
        self.assertTrue(self.client.login(username="owner", password="rahasia123"))
        response = self.client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 0)

    def test_request_with_csrf_token_succeeds(self):
        self.assertTrue(self.client.login(username="owner", password="rahasia123"))
        # Kunjungi halaman yang merender {% csrf_token %} untuk membangkitkan cookie csrftoken
        self.client.get("/education/")
        csrf_cookie = self.client.cookies.get("csrftoken")
        self.assertIsNotNone(csrf_cookie)
        response = self.client.post(
            self.list_url,
            VALID_PAYLOAD,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_cookie.value,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 1)


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.list_url = "/api/v1/projects/"
        self.owner = User.objects.create_superuser(
            username="project_owner", password="rahasia123", email="powner@example.com"
        )
        self.regular = User.objects.create_user(username="project_user", password="rahasia123")
        self.visitor_client = APIClient()
        self.regular_client = APIClient()
        self.owner_client = APIClient()
        self.regular_client.force_authenticate(user=self.regular)
        self.owner_client.force_authenticate(user=self.owner)
        self.project = Project.objects.create(
            title="Portfolio App",
            description="A web app.",
            tech_stack="Django, DRF",
        )
        self.detail_url = f"{self.list_url}{self.project.id}/"

    def test_visitor_can_read_project_list(self):
        response = self.visitor_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_visitor_and_regular_user_cannot_create_project(self):
        payload = {
            "title": "New App",
            "description": "Desc",
            "tech_stack": "Python",
        }
        res_visitor = self.visitor_client.post(self.list_url, payload, format="json")
        self.assertEqual(res_visitor.status_code, status.HTTP_403_FORBIDDEN)
        res_regular = self.regular_client.post(self.list_url, payload, format="json")
        self.assertEqual(res_regular.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_owner_can_create_project(self):
        payload = {
            "title": "New App",
            "description": "Desc",
            "tech_stack": "Python",
        }
        response = self.owner_client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_regular_user_can_star_project(self):
        response = self.regular_client.post(f"{self.detail_url}star/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])

    def test_owner_can_delete_project(self):
        response = self.owner_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)
