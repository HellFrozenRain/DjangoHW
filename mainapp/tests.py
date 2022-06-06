import pickle
from unittest import mock


from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from mainapp.models import News
from authapp.models import CustomUser
from mainapp import models as mainapp_models
from authapp import models as authapp_models
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail as django_mail
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mainapp import tasks as mainapp_tasks
class StaticPagesSmokeTest(TestCase):
    def test_page_index_open(self):
        path = reverse("mainapp:index")
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        path = reverse("mainapp:contacts")
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

class NewsTestCase(TestCase):
    
    def setUp(self):
        super().setUp()
        for i in range(10):
            News.objects.create(
                title=f"news{i}",
                preamble=f"news{i}",
                body=f"Body1{i}",
            )

        CustomUser.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'geekbrains'}
        )
    
    def test_open_page(self):
        path = reverse('mainapp:news')
        result = self.client.get(path)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonym(self):
        path = reverse('mainapp:news_create')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_detail(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_create_deny_access(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):

        news_count = News.objects.all().count()
        
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.post(
            path,
            data={
            "title": "test news",
            "preamble": "test preamble",
            "body": "test body",
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

        self.assertEqual(News.objects.all().count(), news_count + 1)
        
    def test_page_open_update_deny_access(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = mainapp_models.News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data={
                "title": new_title,
                "preamble": news_obj.preamble,
                "body": news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)

class TestCoursesWithMock(TestCase):
    fixtures = (
    # "authapp/fixtures/001_user_admin.json",
    "mainapp/fixtures/002_courses.json",
    "mainapp/fixtures/003_lessons.json",
    "mainapp/fixtures/004_teachers.json",
    )

def test_page_open_detail(self):
    course_obj = mainapp_models.Courses.objects.get(pk=2)
    path = reverse("mainapp:courses_detail", args=[course_obj.pk])
    with open(
    "mainapp/fixtures/006_feedback_list_1.bin", "rb"
    ) as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
        mocked_cache.return_value = pickle.load(inpf)
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)
        self.assertTrue(mocked_cache.called)

class TestTaskMailSend(TestCase):
    fixtures = ("authapp/fixtures/001_user_admin.json",)

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = authapp_models.CustomUser.objects.first()
        mainapp_tasks.send_feedback_mail(
            {"user_id": user_obj.id, "message": message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)

class TestNewsSelenium(StaticLiveServerTestCase):

    fixtures = (
           "mainapp/fixtures/001_homework.json",
        )


    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(
        executable_path=settings.SELENIUM_DRIVER_PATH_FF
        )
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element_by_id("id_username").send_keys("django")
        self.selenium.find_element_by_id("id_password").send_keys("geekbrains")
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto"))
        )

    