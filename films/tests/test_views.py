import pytest
from django.urls import reverse_lazy

from films.models import Category, Film
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestViews:

    @pytest.fixture(scope="class", name="user")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username="user1", password="pass123")
            yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(scope="class", name="category")
    def create_category(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = Category.objects.create(name="cat1")
        yield category
        with django_db_blocker.unblock():
            category.delete()

    def test_create_view(self, client, user, category):
        client.login(username="user1", password="pass123")
        response = client.post(
            reverse_lazy("add-film"),
            data={
                "title": "Test film",
                "description": "Test content",
                "isPublic": True,
                "category": category.id,
                "tags": "test_tag,test_tag1",
            },
        )

        assert response.status_code == 302
        assert Film.objects.last().author.username == user.username
