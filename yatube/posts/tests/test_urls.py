from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создадим запись в БД для проверки доступности адреса post/test-slug/
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст поста",
            group=cls.group,
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = Client()
        self.author.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_group_posts_url_exists_at_desired_location(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.guest_client.get("/group/test-slug/")
        self.assertEqual(response.status_code, 200)

    def test_profile_username_url_exists_at_desired_location(self):
        """Страница /profile/<username> доступна любому пользователю"""
        response = self.guest_client.get(
            f"/profile/{PostURLTests.post.author}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_exists_at_desired_location(self):
        """Страница /posts/<post_id>/ доступна любому пользователю"""
        response = self.guest_client.get(f"/posts/{PostURLTests.post.id}/")
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page_url_exists_at_desired_location(self):
        """Страница /unexisting_page>/ доступна любому пользователю"""
        response = self.guest_client.get("/unexisting_page/")
        self.assertEqual(response.status_code, 404)

    # Проверяем доступность страниц для автора
    def test_post_edit_url_exists_at_desired_location(self):
        """Страница /post/<post_id>/edit/ доступна автору."""
        self.author = Client()
        self.user = User.objects.create_user(username="author")
        self.author.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text="Тестовый текст поста",
        )
        response = self.author.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизовану пользователю."""
        response = self.authorized_client.get("/create/")
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы
    def test_post_create_redirect_anonymous_on_admin_login(self):
        """Страница /create/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.guest_client.get("/create/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        self.author = Client()
        self.author.force_login(self.user)
        templates_url_names = {
            "posts/index.html": "/",
            "posts/group_list.html": "/group/test-slug/",
            "posts/profile.html": "/profile/StasBasov/",
            "posts/post_detail.html": "/posts/1/",
            "posts/create_post.html": "/post/1/edit/" and "/create/",
        }
        for template, url in templates_url_names.items():
            with self.subTest(template=template, url=url):
                response = self.author.get(url)
                self.assertTemplateUsed(response, template)
