from django.forms import ModelForm


from auctions.models import Listing, Comment, Bid


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['creator', 'watched_item', 'category']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)
