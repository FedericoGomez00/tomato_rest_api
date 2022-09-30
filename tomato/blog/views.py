# Django
from django.shortcuts import get_object_or_404

# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

# users
from users.authentication_mixins import Authentication

# blog
from .serializers import BlogpostSerializer, BlogpostListSerializer


class BlogpostViewSet(Authentication, ModelViewSet):
    """
    A user can view, write, update and delete a blogpost
    """
    serializer_class = BlogpostSerializer
    list_serializer_class = BlogpostListSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active = True)

    def list(self, request):
        """
        List all blogpost
        """
        serializer = self.list_serializer_class(self.queryset, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        """
        Delete a blogpost with your id
        """
        try:
            model = self.serializer_class.Meta.model
            blogpost = get_object_or_404(model, pk = pk)
        except:
            return Response(
                {
                    'error' : 'Blogpost not found'
                },
                status = status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = self.list_serializer_class(blogpost)
            blogpost.is_active = False
            blogpost.save()

            return Response(
                {
                    'message' : 'Blogpost deleted',
                    'blogpost' : serializer.data
                },
                status = status.HTTP_200_OK
                )


class LikeBlogpost(Authentication, APIView):
    serializer_class = BlogpostListSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active = True)

    def get(self, request, pk=None):
        """
        Like a blogpost with your id
        (ERROR: a user can liked a blogpost more than once)
        """
        try:
            model = self.serializer_class.Meta.model
            blogpost = get_object_or_404(model, pk = pk)
        except:
            return Response(
            {
                'error' : 'Blogpost not found'
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        else:
            blogpost.likes += 1
            blogpost.save()
            serializer = self.serializer_class(blogpost)

            return Response(
                {
                    'message' : 'Liked a blogpost',
                    'blogpost' : serializer.data
                },
                status = status.HTTP_200_OK
                )