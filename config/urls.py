from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve
import os

admin.site.site_header = "eCEP Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("core.urls")),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path(
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("accounts/", include("accounts.urls")),
    path("programs/", include("course.urls")),
    path("result/", include("result.urls")),
    path("search/", include("search.urls")),
    path("quiz/", include("quiz.urls")),
    path("payments/", include("payments.urls")),
    path('chatbot/', include('chatbot.urls')),
    path("dictionnary/", include("dictionnary.urls")),
    path("forum/", include("forum.urls")),
    path('mychatapp/', include("mychatapp.urls")),
    path('examen/', include("examen.urls")),
    path('badges/', include("badges.urls")),
    path('api_accounts/', include('accounts.urls_api')),
    
    
    
    # flutter connexion
    path('api-auth/', include('rest_framework.urls')),
    path('api_accounts/', include('accounts.urls_api')),
    
    path('api_examen/', include('examen.urls_api')),
    path('api_forum/', include('forum.urls_api')),
    path('api_core/', include('core.urls_api')),
    path('api_course/', include('course.urls_api')),
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    urlpatterns += [
            path('firebase-messaging-sw.js', lambda request: serve(request, os.path.join('static', 'firebase-messaging-sw.js'), document_root=settings.BASE_DIR))
        ]
