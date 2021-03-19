from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .serializers import PageSerializer
from ..models import Page


class PageView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PageSerializer

    def get_object(self):
        page_slug = self.kwargs["page_slug"]
        return Page.objects.get(url=page_slug)
