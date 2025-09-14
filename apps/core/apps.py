from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self):
        try:
            import apps.core.signals  # This line is CRITICAL
            print("✅ Signals imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import signals: {e}")
