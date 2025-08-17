"""
Core app URL configuration.
"""
from django.urls import path
from .views.health import (
    HealthCheckView,
    DetailedHealthCheckView,
    LivenessProbeView,
    ReadinessProbeView,
)

app_name = 'core'

urlpatterns = [
    # Health check endpoints
    path('health/', HealthCheckView.as_view(), name='health'),
    path('health/detailed/', DetailedHealthCheckView.as_view(), name='health-detailed'),
    path('health/live/', LivenessProbeView.as_view(), name='health-liveness'),
    path('health/ready/', ReadinessProbeView.as_view(), name='health-readiness'),
]