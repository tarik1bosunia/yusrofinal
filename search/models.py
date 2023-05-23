from django.db import models


class Name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} {self.name}'


# class SearchHistory(models.Model):
#     session_key = models.CharField(max_length=255, blank=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     keyword = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.keyword