from livefield import LiveManager


class UserManager(LiveManager):
    pass

class ActivityManager(LiveManager):
    def create_request_log(self, request):
        user = request.user
        path = request.path
        params = request.data
        instance = self.model.objects.create(user=user, path=path, params=params)
        return instance

class AccountUserManager(LiveManager):
    pass
