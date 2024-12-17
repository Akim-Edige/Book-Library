from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Book
from .serializers import BookFilter, BookSerializer
import os
import boto3
from botocore.exceptions import NoCredentialsError


# Create your views here.

def create_book(request):
    return render(request, 'create.html')


class BookPagination(PageNumberPagination):
    page_size = 4  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)  # Enable Django filter
    filterset_class = BookFilter  # Apply the ProductFilter
    search_fields = ['id','title', 'author']
    ordering_fields = ['year_min', 'year_max', 'status']
    pagination_class = BookPagination  # Add pagination

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)

        if book.cover_image and os.path.isfile(book.cover_image.path):
            os.remove(book.cover_image.path)

        book.delete()

        return Response({"success": "Product was deleted succesfully"}, status=status.HTTP_202_ACCEPTED)

    def update(self, request, pk=None):
        instance = get_object_or_404(Book, pk=pk)
        # Update the instance fields with the new data
        instance.author = request.data.get('author', instance.author)
        instance.title = request.data.get('title', instance.author)
        instance.year = request.data.get('year', instance.author)
        instance.description = request.data.get('description', instance.author)
        instance.status = request.data.get('status', instance.author)
        if request.data.get('cover_image', instance.cover_image):
            instance.cover_image = request.data.get('cover_image', instance.cover_image)
        instance.save()

        # Serialize the updated product
        serializer = BookSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Retrieve data from the request
        title = request.data.get('title')
        author = request.data.get('author')
        year = request.data.get('year')
        stat = request.data.get('status')
        description = request.data.get('description')
        cover_image = request.FILES.get('cover_image')

        if not cover_image:
            cover_image = 'book_covers/default_cover.png'

        # Validation: Ensure required fields are provided
        if not title or not author or not year or not stat or not description:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new Book object
        book = Book(
            title=title,
            author=author,
            year=year,
            status=stat,
            description=description,
            cover_image=cover_image  # Only set if provided
        )

        # Save the new Book object
        try:
            book.save()
        except Exception as e:
            return Response({"error": f"Failed to create book: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize and return the newly created book
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def book_list(request):
    return render(request, 'books_with_images.html')


@csrf_exempt
def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        return render(request, 'book_details.html', {'book': book})
    except:
        return render(request, '404.html')  # You can create a 404 page or handle it in another way

def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'edit.html', {'book': book})


# def s3_api(request):
#     s3_client = boto3.client('s3')
#
#     try:
#         # Generate the pre-signed URL
#         url = s3_client.generate_presigned_url('put_object',
#                                                Params={'Bucket': 'book-library-s3-bucket', 'Key': 'first_image'},
#                                                ExpiresIn=60)
#         return HttpResponse(url, content_type='text/plain', status=200)
#
#     except NoCredentialsError:
#         print("Credentials not available.")
#         return HttpResponse("Credentials not available", status=400)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return HttpResponse(f"An error occurred: {e}", status=500)

