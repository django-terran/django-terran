from .views import SignUpEntityHtmxView
from .views import SignUpCountryHtmxView
from .views import SignUpLevel1AreaHtmxView
from .views import SignUpLevel2AreaHtmxView
from .views import SignUpPreviewHtmxView
from .views import SignUpFindMeView
from .views import SignUpView
from django.urls import path

urlpatterns = [
    path(
        "signup-htmx-entity/", SignUpEntityHtmxView.as_view(), name="signup-htmx-entity"
    ),
    path(
        "signup-htmx-country/",
        SignUpCountryHtmxView.as_view(),
        name="signup-htmx-country",
    ),
    path(
        "signup-htmx-level1area/",
        SignUpLevel1AreaHtmxView.as_view(),
        name="signup-htmx-level1area",
    ),
    path(
        "signup-htmx-level2area/",
        SignUpLevel2AreaHtmxView.as_view(),
        name="signup-htmx-level2area",
    ),
    path(
        "signup-htmx-preview/",
        SignUpPreviewHtmxView.as_view(),
        name="signup-htmx-preview",
    ),
    path("signup-findme/", SignUpFindMeView.as_view(), name="signup-findme"),
    path("signup/", SignUpView.as_view()),
]
