class RemoteAddrMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        request.META["REMOTE_ADDR"] = request.META.get("HTTP_X_REAL_IP", "127.0.0.1")
        return request