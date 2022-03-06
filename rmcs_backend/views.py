from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


@api_view()
@permission_classes([AllowAny])
def doc_urls():
    return include_docs_urls(title='RMCSAPI')


@api_view()
@permission_classes([AllowAny])
def schema():
    return get_schema_view(
        title="RMCS",
        description="API for RMCS",
        version="1.0.0"
    )

