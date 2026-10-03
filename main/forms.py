from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from main.models import Project, Education
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/username/repo",
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "description",
            "start_year",
            "end_year",
        ]

        labels = {
            "institution": "Institusi",
            "degree": "Gelar / Program Studi",
            "description": "Deskripsi",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "e.g. Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "e.g. S1 Sistem Informasi",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan fokus studi / pencapaian",
                    "rows": 3,
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "e.g. 2025",
                    "min": 1900,
                    "max": 2100,
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "e.g. 2029 (biarkan kosong jika masih berlangsung)",
                    "min": 1900,
                    "max": 2100,
                }
            ),
        }
    def _clean_text_field(self, field_name):
        value = self.cleaned_data.get(field_name, "")
        cleaned_value = strip_tags(value).strip()

        if self.fields[field_name].required and not cleaned_value:
            raise ValidationError("Field ini wajib diisi.")

        return cleaned_value

    def clean_institution(self):
        return self._clean_text_field("institution")

    def clean_degree(self):
        return self._clean_text_field("degree")

    def clean_description(self):
        return self._clean_text_field("description")