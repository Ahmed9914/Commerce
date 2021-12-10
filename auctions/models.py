from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256, blank=False)
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=256, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='products', blank=True,
                                 null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='created_listing')
    watched_item = models.ManyToManyField(User, related_name='watcher',
                                          blank=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    amount = models.IntegerField()
    item_on_bid = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                    related_name='listing_bid')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_bid')

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return f'Bid on {self.item_on_bid} by {self.bidder}'


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=128)
    commented_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                          related_name='listing_comment')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='user_comment')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.commenter}'
