from rest_framework.generics import ListAPIView

from .models import Order
from .serializers import OrderSerializer


class OrderListAPIView(ListAPIView):
    """
    API endpoint that allows view orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
