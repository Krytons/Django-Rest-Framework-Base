from apiXamarine.viewsets.productviewset import ProductViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')

