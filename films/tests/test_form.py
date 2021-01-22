from films.forms import film
import pytest
from films.models import Category
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestForms:

    @pytest.fixture(scope="function", name="category")
    def create_category(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = Category.objects.create(name="cat1")
        yield category
        with django_db_blocker.unblock():
            category.delete()

    @pytest.fixture(scope="class", name="user")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username="user1", password="pass123")
            yield user
        with django_db_blocker.unblock():
            user.delete()

    def test_film_valid_data(self, category):
        form = film.FilmForm(
            data={
                "title": "Test film",
                "description": "Test content",
                "isPublic": True,
                "category": category.id,
                "tags": "test_tag,test_tag1"
            }
        )
        assert form.is_valid()