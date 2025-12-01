from django.utils import translation

class UserLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = None

        user = getattr(request, "user", None)
        if user and user.is_authenticated and hasattr(user, "profile"):
            language = user.profile.language

        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = language

        response = self.get_response(request)

        translation.deactivate()

        return response
