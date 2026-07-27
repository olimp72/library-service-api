from datetime import date
from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer

class BorrowingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active is not None:
            queryset = queryset.filter(actual_return_date__isnull=(is_active.lower() == "true"))

        if user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        borrowing.book.inventory -= 1
        borrowing.book.save()

    @action(detail=True, methods=["post"], url_path="return")
    @transaction.atomic
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response({"error": "This borrowing has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrowing.actual_return_date = date.today()
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        return Response({"message": "Borrowing returned successfully."}, status=status.HTTP_200_OK)
