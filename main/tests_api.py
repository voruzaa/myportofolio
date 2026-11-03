import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.client.force_authenticate(user=self.visitor)
        for method, url, payload in [
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "Changed"}),
            ("delete", self.detail_url, None),
        ]:
            response = getattr(self.client, method)(url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.education = Education.objects.create(
            institution="Universitas Indonesia", degree="S1 Sistem Informasi",
            description="Faculty of Computer Science", started_at="2025-08-01",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "institution": "New School", "degree": "Diploma", "description": "Education",
            "started_at": "2026-01-01", "ended_at": None,
        }

    def test_public_list_detail_search_and_order(self):
        older = Education.objects.create(
            institution="High School", degree="High School", started_at="2022-07-01",
            ended_at="2025-06-01",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [str(self.education.id), str(older.id)])
        self.assertTrue(response.data[0]["is_ongoing"])
        self.assertEqual(response.data[1]["ended_at"], "2025-06-01")
        self.assertFalse(response.data[1]["is_ongoing"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).data, response.data[0])
        response = self.client.get(self.list_url, {"institution": "  UNIVERSITAS  "})
        self.assertEqual([item["id"] for item in response.data], [str(self.education.id)])
        self.assertEqual(self.client.get(self.list_url, {"institution": "not-found"}).data, [])
        self.assertEqual(len(self.client.get(self.list_url, {"institution": "  "}).data), 2)

    def test_missing_objects_and_wrong_methods(self):
        detail_url = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(detail_url).status_code, 404)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.patch(detail_url, {"degree": "New"}, format="json").status_code, 404)
        self.assertEqual(self.client.post(reverse("api:education-star", args=[uuid.uuid4()])).status_code, 404)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url, payload in [
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"degree": "Changed"}),
                ("delete", self.detail_url, None),
            ]:
                response = getattr(self.client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi")
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"degree": "Updated"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Updated")
        self.assertEqual(self.education.description, "Faculty of Computer Science")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "New School")
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_staff_without_editor_group_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {"degree": "Changed"}, format="json").status_code, 403)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        created = Education.objects.get(pk=response.data["id"])
        self.assertEqual(created.institution, "New School")
        self.assertTrue(created.is_ongoing)
        response = self.client.patch(self.detail_url, {"degree": "Changed"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["degree"], "Changed")
        self.assertEqual(self.client.put(self.detail_url, {"degree": "Incomplete"}, format="json").status_code, 400)
        response = self.client.put(self.detail_url, {**self.payload, "ended_at": "2026-11-01"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_ongoing"])
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_validation_and_text_sanitization(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution": "   "}, "institution"),
            ({"institution": '<img src="x" onerror="alert(1)">'}, "institution"),
            ({"degree": '<img src="x" onerror="alert(1)">'}, "degree"),
            ({"started_at": "invalid-date"}, "started_at"),
            ({"ended_at": "invalid-date"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)
        response = self.client.post(self.list_url, {
            **self.payload, "institution": " <b>School</b> ", "degree": " <em>Diploma</em> ",
            "description": '<img src="x" onerror="alert(1)"><p>Safe text</p>',
        }, format="json")
        self.assertEqual(response.status_code, 201)
        created = Education.objects.get(pk=response.data["id"])
        self.assertEqual(created.institution, "School")
        self.assertEqual(created.degree, "Diploma")
        self.assertEqual(created.description, "Safe text")

    def test_editor_update_uses_serializer_validation(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"institution": "<img src=x>"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Universitas Indonesia")
        response = self.client.patch(self.detail_url, {
            "institution": "<b>Updated School</b>", "description": "<img src=x>",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Updated School")
        self.assertEqual(self.education.description, "")

    def test_star_uses_current_user_and_preserves_other_users(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.education.starred_by.add(self.editor)
        self.client.force_authenticate(user=self.visitor)
        self.assertFalse(self.client.get(self.detail_url).data["is_starred"])
        response = self.client.post(self.star_url, {"user_id": self.owner.id}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 2)
        self.assertFalse(self.education.starred_by.filter(pk=self.owner.id).exists())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.education.starred_by.filter(pk=self.editor.id).exists())
        self.client.force_authenticate(user=self.editor)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])

    def test_computed_fields_and_id_cannot_be_forged(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "star_count": 99, "is_starred": True,
            "is_ongoing": False, "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertTrue(response.data["is_ongoing"])
        self.assertNotIn("starred_by", response.data)
        self.assertNotIn("starred_by_names", response.data)
        self.assertNotIn("email", response.data)
        self.assertNotIn("password", response.data)

    def test_head_and_options_do_not_change_data(self):
        self.assertEqual(self.client.head(self.list_url).status_code, 200)
        self.assertEqual(self.client.head(self.detail_url).status_code, 200)
        self.assertEqual(self.client.options(self.detail_url).status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi")
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_session_writes_require_csrf_for_owner_and_editor(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        client.get(reverse("main:show_education"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token).status_code, 201)
        client.logout()
        client.login(username="editor", password="test-password")
        self.assertEqual(client.patch(self.detail_url, {"degree": "New"}, format="json").status_code, 403)
        client.get(reverse("main:show_education"))
        token = client.cookies["csrftoken"].value
        response = client.patch(self.detail_url, {"degree": "New"}, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)

    def test_star_receives_csrf_cookie_without_create_form(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="visitor", password="test-password")
        self.assertEqual(client.post(self.star_url).status_code, 403)
        page = client.get(reverse("main:show_education"))
        self.assertNotContains(page, 'id="education-form"')
        token = client.cookies["csrftoken"].value
        response = client.post(self.star_url, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])


class APIIntegrationTest(APITestCase):
    def test_projects_page_uses_drf_and_sets_csrf_cookie_for_visitor(self):
        visitor = User.objects.create_user(username="visitor", password="test-password")
        project = Project.objects.create(title="Portfolio", description="Website", tech_stack="Django")
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="visitor", password="test-password")
        response = client.get(reverse("main:show_projects"))
        self.assertContains(response, reverse("api:project-list"))
        self.assertNotContains(response, reverse("main:get_projects_json"))
        self.assertNotContains(response, 'id="project-form"')
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("api:project-star", args=[project.id]), HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])

    def test_education_page_uses_drf_and_editor_has_edit_modal_only(self):
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.client.force_login(editor)
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, reverse("api:education-list"))
        self.assertContains(response, 'id="education-form"')
        self.assertNotContains(response, 'data-action="create"')
        self.assertNotContains(response, 'id="delete-education-form"')

    def test_legacy_routes_and_pages_remain_available(self):
        for name in ["show_main", "show_experience", "show_projects", "show_education", "login", "register"]:
            self.assertEqual(self.client.get(reverse(f"main:{name}")).status_code, 200)
        self.assertEqual(self.client.get(reverse("main:get_projects_json")).json(), [])
        self.assertEqual(self.client.get(reverse("main:get_education_json")).json(), [])

    def test_malformed_json_is_rejected(self):
        owner = User.objects.create_superuser(username="owner", password="test-password")
        self.client.force_authenticate(user=owner)
        for name in ("project-list", "education-list"):
            response = self.client.post(reverse(f"api:{name}"), '{"invalid":', content_type="application/json")
            self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(Education.objects.count(), 0)
