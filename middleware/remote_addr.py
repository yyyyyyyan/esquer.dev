class RemoteAddrMiddleware(object):
    def process_request(self, request):
        request.META["REMOTE_ADDR"] = request.META.get("HTTP_X_REAL_IP", "127.0.0.1")