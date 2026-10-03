from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from main.models import Education, Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
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

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Personal Portfolio Website",
            description="A personal portfolio website built with Django MVT",
            tech_stack="Python, Django, HTML, CSS",
            project_url="https://github.com/ke-Vyn/myportofolio",
        )

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_page_renders_ajax_skeleton(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="grid"')
        self.assertNotContains(response, self.project.title)

    def test_projects_json_returns_project_data(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.project.id))
        self.assertEqual(
            data[0]["fields"]["title"],
            self.project.title,
        )
        self.assertEqual(
            data[0]["fields"]["description"],
            self.project.description,
        )
        self.assertEqual(
            data[0]["fields"]["tech_stack"],
            self.project.tech_stack,
        )

    def test_projects_json_returns_empty_list_when_no_projects(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

class EducationCreationTest(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username="education-owner",
            email="owner@example.com",
            password="test-password",
        )
        self.create_url = reverse("main:create_education")
        self.valid_payload = {
            "institution": "Universitas Indonesia",
            "degree": "S1 Sistem Informasi",
            "description": "Fokus pada sistem informasi.",
            "start_year": "2025",
            "end_year": "",
        }

    def test_superuser_can_create_education(self):
        self.client.force_login(self.superuser)

        response = self.client.post(self.create_url, self.valid_payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["education"]["institution"],
            "Universitas Indonesia",
        )
        self.assertTrue(
            Education.objects.filter(
                institution="Universitas Indonesia"
            ).exists()
        )

    def test_invalid_education_returns_400(self):
        self.client.force_login(self.superuser)
        payload = {
            **self.valid_payload,
            "institution": "",
            "start_year": "not-a-year",
        }

        response = self.client.post(self.create_url, payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.json()["errors"])
        self.assertIn("start_year", response.json()["errors"])
        self.assertEqual(Education.objects.count(), 0)

    def test_anonymous_user_cannot_create_education(self):
        response = self.client.post(self.create_url, self.valid_payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 0)

    def test_regular_user_cannot_create_education(self):
        regular_user = get_user_model().objects.create_user(
            username="regular-user",
            password="test-password",
        )
        self.client.force_login(regular_user)

        response = self.client.post(self.create_url, self.valid_payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 0)

    def test_html_tags_are_removed_from_text_fields(self):
        self.client.force_login(self.superuser)
        payload = {
            **self.valid_payload,
            "institution": "<b>Universitas Indonesia</b>",
            "degree": "<i>S1 Sistem Informasi</i>",
            "description": "<script>alert(1)</script>Deskripsi",
        }

        response = self.client.post(self.create_url, payload)

        self.assertEqual(response.status_code, 201)

        education = Education.objects.get()
        self.assertEqual(education.institution, "Universitas Indonesia")
        self.assertEqual(education.degree, "S1 Sistem Informasi")
        self.assertEqual(education.description, "alert(1)Deskripsi")
        self.assertNotIn("<", education.institution)
        self.assertNotIn("<", education.degree)
        self.assertNotIn("<", education.description)