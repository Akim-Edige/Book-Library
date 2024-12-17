from http import HTTPStatus
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Book
from rest_framework.test import APITestCase


class BookListTestCase(TestCase):

    def test_view(self):
        path = reverse('show_books')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'books_with_images.html')


class BookViewSetTests(APITestCase):
    fixtures = ['data.json']
    def setUp(self):
        # Sample books for testing
        self.sample_book = Book.objects.first()

        # URL for the book endpoints
        self.book_list_url = 'http://127.0.0.1:8000/api/books/'
        self.book_detail_url = self.book_list_url+str(self.sample_book.id)+'/'


    def test_list_books(self):
        """Test listing all books"""
        response = self.client.get(self.book_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)


    def test_create_book(self):
        """Test creating a new book"""
        cover_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "title": "New Book",
            "author": "New Author",
            "year": 2023,
            "status": "В наличии",
            "description": "A new test book",
            "cover_image": cover_image
        }
        response = self.client.post(self.book_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 11)
        last_added_book = Book.objects.all()[10]
        self.assertEqual(last_added_book.title, "New Book")


    def test_get_book_detail(self):
        """Test retrieving a single book detail"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.sample_book.title)

    def test_update_book(self):
        """Test updating a book"""
        data = {
            "title": "Updated Book Title",
            "author": "Updated Author",
            "year": 2021,
            "status": "Выдана",
            "description": "Updated description"
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sample_book.refresh_from_db()
        self.assertEqual(self.sample_book.title, "Updated Book Title")
        self.assertEqual(self.sample_book.year, 2021)


    def test_delete_book(self):
        """Test deleting a book"""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Book.objects.count(), 9)

    def test_missing_fields_on_create(self):
        """Test creating a book with missing fields"""
        data = {
            "title": "Incomplete Book",
            "author": "",
            "year": "",
            "status": "",
            "description": ""
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("All fields are required", response.data['error'])