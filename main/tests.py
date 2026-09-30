from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education
from main.forms import ProjectForm


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

    def test_education_data_appears(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, self.edu.institution)
        self.assertContains(response, self.edu.degree)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "No education history yet.")
