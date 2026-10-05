from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import Group, User
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education
from main.forms import EducationForm, ProjectForm


class ProjectFormTest(SimpleTestCase):
    def test_html_tags_are_removed_and_text_is_trimmed(self):
        form = ProjectForm(data={
            "title": '  <img src=x onerror="alert(1)"><b>Portfolio</b>  ',
            "tech_stack": "  <em>Django</em> & Python  ",
            "description": "  <p>Proyek <strong>pribadi</strong>.</p>  ",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Portfolio")
        self.assertEqual(form.cleaned_data["tech_stack"], "Django & Python")
        self.assertEqual(form.cleaned_data["description"], "Proyek pribadi.")

    def test_title_containing_only_html_tags_is_rejected(self):
        form = ProjectForm(data={
            "title": ' <img src=x onerror="alert(1)"> ',
            "tech_stack": "Django",
            "description": "Proyek pribadi.",
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], [
            "Nama proyek tidak boleh hanya berisi tag HTML.",
        ])


class EducationFormTest(SimpleTestCase):
    def test_text_fields_are_sanitized(self):
        form = EducationForm(data={
            "institution": '  <img src="x" onerror="alert(\'XSS!\')"><b>Universitas Indonesia</b>  ',
            "degree": "  <em>S1 Sistem Informasi</em>  ",
            "description": ' <img src="x" onerror="alert(\'XSS!\')"><p>Pendidikan</p> ',
            "started_at": "2025-08-01",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["institution"], "Universitas Indonesia")
        self.assertEqual(form.cleaned_data["degree"], "S1 Sistem Informasi")
        self.assertEqual(form.cleaned_data["description"], "Pendidikan")

    def test_required_fields_containing_only_tags_are_rejected(self):
        for field in ["institution", "degree"]:
            with self.subTest(field=field):
                data = {
                    "institution": "Universitas Indonesia", "degree": "S1 Sistem Informasi",
                    "started_at": "2025-08-01",
                }
                data[field] = '<img src="x" onerror="alert(\'XSS!\')">'
                form = EducationForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_optional_description_containing_only_tags_becomes_empty(self):
        form = EducationForm(data={
            "institution": "Universitas Indonesia", "degree": "S1 Sistem Informasi",
            "description": '<img src="x" onerror="alert(\'XSS!\')">',
            "started_at": "2025-08-01",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["description"], "")


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class EducationTest(TestCase):
    def setUp(self):
        import datetime
        self.edu = Education.objects.create(
            institution="Universitas Indonesia",
            degree="Bachelor of Information Systems",
            description="Faculty of Computer Science.",
            started_at=datetime.date(2025, 8, 1),
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page_only_renders_ajax_shell(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertNotContains(response, f'<h2>{self.edu.institution}</h2>')
        self.assertNotContains(response, self.edu.degree)
        self.assertNotIn("education_list", response.context)
        self.assertContains(response, 'id="education-grid"')
        self.assertContains(response, 'id="education-loading"')
        self.assertContains(response, 'id="education-error"')
        self.assertContains(response, 'js/education.js')

        data = self.client.get(reverse("main:get_education_json")).json()
        self.assertEqual(data[0]["pk"], str(self.edu.pk))
        self.assertEqual(data[0]["fields"], {
            "institution": self.edu.institution,
            "degree": self.edu.degree,
            "description": self.edu.description,
            "started_at": "2025-08-01",
            "ended_at": None,
            "is_ongoing": True,
            "star_count": 0,
            "is_starred": False,
        })

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "No education history yet.")
        self.assertEqual(self.client.get(reverse("main:get_education_json")).json(), [])

    def test_education_json_order_and_completed_dates(self):
        import datetime
        older = Education.objects.create(
            institution="School", degree="High school",
            started_at=datetime.date(2022, 7, 1),
            ended_at=datetime.date(2025, 6, 1),
        )
        data = self.client.get(reverse("main:get_education_json")).json()
        self.assertEqual([item["pk"] for item in data], [str(self.edu.pk), str(older.pk)])
        self.assertEqual(data[1]["fields"]["ended_at"], "2025-06-01")
        self.assertFalse(data[1]["fields"]["is_ongoing"])

    def test_star_count_and_status_are_specific_to_current_user(self):
        user = User.objects.create_user(username="star-user")
        other = User.objects.create_user(username="other-user")
        self.edu.starred_by.add(user)
        for viewer, expected in [(None, False), (user, True), (other, False)]:
            with self.subTest(viewer=viewer):
                self.client.logout()
                if viewer:
                    self.client.force_login(viewer)
                fields = self.client.get(reverse("main:get_education_json")).json()[0]["fields"]
                self.assertEqual(fields["star_count"], 1)
                self.assertEqual(fields["is_starred"], expected)
                self.assertNotIn("starred_by", fields)
                self.assertNotIn("starred_by_names", fields)

    def test_education_controls_follow_roles(self):
        ordinary = User.objects.create_user(username="ordinary")
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        owner = User.objects.create_user(username="owner", is_superuser=True, is_staff=True)
        for user, can_edit, can_delete in [
            (None, False, False), (ordinary, False, False),
            (editor, True, False), (owner, True, True),
        ]:
            with self.subTest(user=user):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                response = self.client.get(reverse("main:show_education"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(b'data-action="edit"' in response.content, can_edit)
                self.assertEqual(b'data-action="delete"' in response.content, can_delete)
                self.assertEqual(b'id="delete-education-form"' in response.content, can_delete)
                self.assertEqual(b'data-action="star"' in response.content, user is not None)
                self.assertEqual(b'id="education-form"' in response.content, can_delete)
                self.assertContains(response, 'id="education-search-input"')

    def test_education_search_filters_institution_case_insensitively(self):
        url = reverse("main:get_education_json")
        response = self.client.get(url, {"institution": "  universitas indonesia  "})
        self.assertEqual([item["pk"] for item in response.json()], [str(self.edu.pk)])
        self.assertEqual(self.client.get(url, {"institution": "Bachelor"}).json(), [])
        self.assertEqual(len(self.client.get(url, {"institution": "  "}).json()), 1)

    def test_ajax_create_requires_owner_and_post(self):
        url = reverse("main:create_education_ajax")
        ordinary = User.objects.create_user(username="create-ordinary")
        editor = User.objects.create_user(username="create-editor")
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        for user in [None, ordinary, editor]:
            with self.subTest(user=user):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                response = self.client.post(url, {
                    "institution": "School", "degree": "Diploma", "started_at": "2026-01-01",
                })
                self.assertEqual(response.status_code, 403)
                self.assertIn("message", response.json())
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.client.get(url).status_code, 405)

    def test_ajax_create_validates_and_returns_json(self):
        owner = User.objects.create_user(username="create-owner", is_superuser=True, is_staff=True)
        self.client.force_login(owner)
        url = reverse("main:create_education_ajax")
        invalid = self.client.post(url, {"institution": "School", "started_at": "invalid-date"})
        self.assertEqual(invalid.status_code, 400)
        self.assertIn("degree", invalid.json()["errors"])
        self.assertIn("started_at", invalid.json()["errors"])
        self.assertEqual(Education.objects.count(), 1)

        response = self.client.post(url, {
            "institution": "New School", "degree": "Diploma", "description": "Description",
            "started_at": "2026-01-01", "ended_at": "",
        })
        self.assertEqual(response.status_code, 201)
        created = Education.objects.get(pk=response.json()["pk"])
        self.assertEqual(created.institution, "New School")
        self.assertTrue(created.is_ongoing)
        data = self.client.get(reverse("main:get_education_json")).json()
        self.assertEqual(data[0]["pk"], str(created.pk))

    def test_ajax_create_enforces_csrf(self):
        owner = User.objects.create_user(username="create-csrf-owner", is_superuser=True, is_staff=True)
        client = Client(enforce_csrf_checks=True)
        client.force_login(owner)
        url = reverse("main:create_education_ajax")
        payload = {"institution": "School", "degree": "Diploma", "started_at": "2026-01-01"}
        self.assertEqual(client.post(url, payload).status_code, 403)
        client.get(reverse("main:show_education"))
        payload["csrfmiddlewaretoken"] = client.cookies["csrftoken"].value
        self.assertEqual(client.post(url, payload).status_code, 201)

    def test_ajax_create_rejects_xss_only_required_fields_and_sanitizes_saved_text(self):
        owner = User.objects.create_user(username="xss-owner", is_superuser=True, is_staff=True)
        self.client.force_login(owner)
        url = reverse("main:create_education_ajax")
        payload = {
            "institution": '<img src="x" onerror="alert(\'XSS!\')">',
            "degree": "<b>Diploma</b>", "started_at": "2026-01-01",
            "description": '<img src="x" onerror="alert(\'XSS!\')"><p>Safe text</p>',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.json()["errors"])
        self.assertEqual(Education.objects.count(), 1)
        payload["institution"] += "<b>Safe School</b>"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        education = Education.objects.get(pk=response.json()["pk"])
        self.assertEqual(education.institution, "Safe School")
        self.assertEqual(education.degree, "Diploma")
        self.assertEqual(education.description, "Safe text")
        fields = self.client.get(reverse("main:get_education_json")).json()[0]["fields"]
        self.assertEqual(fields["institution"], "Safe School")
        self.assertEqual(fields["description"], "Safe text")

    def test_editor_update_also_sanitizes_text(self):
        editor = User.objects.create_user(username="xss-editor")
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.client.force_login(editor)
        response = self.client.post(reverse("main:update_education", args=[self.edu.pk]), {
            "institution": "<b>Updated School</b>", "degree": "<em>Updated Degree</em>",
            "description": '<img src="x" onerror="alert(\'XSS!\')">Description',
            "started_at": "2025-08-01",
        })
        self.assertRedirects(response, reverse("main:show_education"))
        self.edu.refresh_from_db()
        self.assertEqual(self.edu.institution, "Updated School")
        self.assertEqual(self.edu.degree, "Updated Degree")
        self.assertEqual(self.edu.description, "Description")

    def test_star_requires_login_post_and_toggles_once(self):
        url = reverse("main:toggle_education_star", args=[self.edu.pk])
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(self.edu.starred_by.count(), 0)
        user = User.objects.create_user(username="visitor")
        self.client.force_login(user)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url), reverse("main:show_education"))
        self.assertEqual(self.edu.starred_by.count(), 1)
        self.assertRedirects(self.client.post(url), reverse("main:show_education"))
        self.assertEqual(self.edu.starred_by.count(), 0)

    def test_star_rejects_post_without_csrf(self):
        user = User.objects.create_user(username="csrf-visitor")
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        url = reverse("main:toggle_education_star", args=[self.edu.pk])
        self.assertEqual(client.post(url).status_code, 403)
        self.assertEqual(self.edu.starred_by.count(), 0)
