from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image

from portfolio import seed_data
from portfolio.models import AboutCard, Metric, Profile, Project, Skill

SEED_MEDIA_DIR = Path(__file__).resolve().parents[2] / "seed_media"
MAX_IMAGE_WIDTH = 1600


def _webp(path: Path) -> ContentFile:
    """Convert a seed image to an optimized WebP file."""
    with Image.open(path) as img:
        img = img.convert("RGB")
        if img.width > MAX_IMAGE_WIDTH:
            height = round(img.height * MAX_IMAGE_WIDTH / img.width)
            img = img.resize((MAX_IMAGE_WIDTH, height), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=82, method=6)
    return ContentFile(buffer.getvalue(), name=f"{path.stem}.webp")


class Command(BaseCommand):
    help = "Fill the database with the initial portfolio content (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace existing content (metrics, about cards, skills, projects, profile).",
        )

    @transaction.atomic
    def handle(self, *args, force: bool = False, **options):
        if Profile.objects.exists() and not force:
            self.stdout.write(self.style.WARNING("Content already exists — skipped (use --force to reset)."))
            return

        self._seed_profile()
        self._replace(Metric, seed_data.METRICS)
        self._replace(AboutCard, seed_data.ABOUT_CARDS)
        self._replace(Skill, seed_data.SKILLS)
        self._seed_projects()
        self.stdout.write(self.style.SUCCESS("Portfolio content seeded."))

    def _seed_profile(self):
        profile = Profile.load() or Profile()
        for field, value in seed_data.PROFILE.items():
            setattr(profile, field, value)

        video = SEED_MEDIA_DIR / seed_data.PROFILE_MEDIA["hero_video"]
        if video.exists():
            if profile.hero_video:
                profile.hero_video.delete(save=False)
            profile.hero_video.save(video.name, ContentFile(video.read_bytes()), save=False)

        poster = SEED_MEDIA_DIR / seed_data.PROFILE_MEDIA["hero_poster"]
        if poster.exists():
            if profile.hero_poster:
                profile.hero_poster.delete(save=False)
            webp = _webp(poster)
            profile.hero_poster.save(webp.name, webp, save=False)

        profile.save()
        self.stdout.write("  profile")

    def _replace(self, model, rows):
        model.objects.all().delete()
        model.objects.bulk_create(model(order=i, **row) for i, row in enumerate(rows, start=1))
        self.stdout.write(f"  {model._meta.verbose_name_plural}: {len(rows)}")

    def _seed_projects(self):
        for project in Project.objects.all():
            if project.image:
                project.image.delete(save=False)
        Project.objects.all().delete()

        for i, row in enumerate(seed_data.PROJECTS, start=1):
            row = dict(row)
            image_name = row.pop("image", "")
            project = Project(order=i, **row)
            image_path = SEED_MEDIA_DIR / image_name if image_name else None
            if image_path and image_path.exists():
                webp = _webp(image_path)
                project.image.save(webp.name, webp, save=False)
            project.save()
        self.stdout.write(f"  projects: {len(seed_data.PROJECTS)}")
