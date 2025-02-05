from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from shop_api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "is_active", "date_joined"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # fixme: add permissions and authentication
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username", "email"]
