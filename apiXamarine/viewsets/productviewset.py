from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apiXamarine.models import Product
from apiXamarine.serializers import ProductSerializer

# This grants all the basic REST API such as insert and update
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Action decorator is used to mark a function as routable: details is used to say if the method has to handle
    # more than 1 item of the referred class.
    @action(methods=['GET'], detail=False)
    def get_oldest(self, request):
        oldest = self.get_queryset().order_by('created_at').first()
        serializer = self.get_serializer_class()(oldest)
        return Response(serializer.data, status=status.HTTP_200_OK)
