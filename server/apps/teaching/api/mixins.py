from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter = {}
        for url_field in self.lookup_fields:
            if self.kwargs[url_field]:  # Ignore empty fields.
                filter_field = self.lookup_fields[url_field]
                filter[filter_field] = self.kwargs[url_field] # Translate field
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
