from rest_framework import exceptions
from apps.businesses.models import Business, BusinessMember

class TenantMixin:
    def get_business(self):
        # In a real app, this might come from a header or session
        # For simplicity, we'll take the first business the user is a member of
        # or a business specified in the query params/URL
        business_id = self.request.query_params.get('business_id')
        if not business_id:
            membership = BusinessMember.objects.filter(user=self.request.user).first()
            if membership:
                return membership.business
            raise exceptions.PermissionDenied("No business selected or membership found.")
        
        try:
            membership = BusinessMember.objects.get(
                user=self.request.user,
                business_id=business_id
            )
            return membership.business
        except BusinessMember.DoesNotExist:
            raise exceptions.PermissionDenied("You are not a member of this business.")

    def get_queryset(self):
        queryset = super().get_queryset()
        business = self.get_business()
        return queryset.filter(business=business)

    def perform_create(self, serializer):
        business = self.get_business()
        serializer.save(business=business)
