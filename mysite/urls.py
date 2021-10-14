from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # ------------ Index ----------------
    path('', include('organizer.urls')),
    # ------------ Admin ----------------
    path('admin/', admin.site.urls),
    # ------------ Calendar -------------
]