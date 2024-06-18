from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Adjust the import statement if simulateur and simulation are separate apps
from simulation.urls import urlpatterns as simulation_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(simulation_urls)),
    path('', include(simulation_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
