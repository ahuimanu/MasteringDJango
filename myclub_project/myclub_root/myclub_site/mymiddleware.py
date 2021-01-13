class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # executed before the next middleware or view is called
        request.META['CUSTOM_KEY'] = "Kilroy was here"

        response = self.get_response(request)

        # This code is executed after the view is call - on the way back out to the response
        return response