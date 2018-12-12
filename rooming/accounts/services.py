from django.urls import reverse

from . import models


class TrackingURLService:
    def generate_link(self, account, user, url, request):
        tracking_url, created = models.TrackingURL.objects.get_or_create(
            account=account,
            user=user,
            url=url
        )
        return self.get_link(tracking_url, request)

    def get_link(self, tracking_url, request):
        path = reverse('chatbot:redirect', kwargs=dict(
            tracking_url_id=tracking_url.tracking_url_id
        ))
        url = request.build_absolute_uri(path).replace('http', 'https')
        return url

    def reverse_link(self, tracking_url_id):
        try:
            t_url = models.TrackingURL.objects.get(tracking_url_id=tracking_url_id)
        except models.TrackingURL.DoesNotExist:
            return None
        t_url.click_count += 1
        t_url.save()
        return t_url.url
