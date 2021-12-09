from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Category, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(is_active=True)
    })


def get_categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.filter()
    })


def get_watchlist(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(watched_item=request.user),
        'watchlist': 'My Watchlist'
    })


def get_category(request, category_id):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(category=category_id,
                                           is_active=True),
        'category': Category.objects.filter(id=category_id),
    })


def get_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    comments = Comment.objects.filter(commented_listing=listing)\
        .order_by('-created')
    # Handle the following if the user is authenticated
    if request.user.is_authenticated:
        # Get the current winner of the bid
        try:
            current_bid = Bid.objects\
                .filter(item_on_bid=listing)\
                .first()
        except ObjectDoesNotExist:
            current_bid = None

        # Handle the following while the listing is active
        if listing.is_active:
            # if the current user is the listing creator
            if listing.creator == request.user:
                # Done: Add close bidding form
                if request.method == 'POST' and 'close_bid' in request.POST:
                    listing.is_active = False
                    listing.save()
                    messages.success(request,
                                     'Listing closed successfully')
                    return HttpResponseRedirect(reverse('listing',
                                                args=(listing.id,)))
            # Done: Add new bid form
            if request.method == 'POST' and 'add_bid' in request.POST:
                bid_form = BidForm(request.POST)
                if bid_form.is_valid():
                    valid_bid = False
                    new_bid = bid_form.save(commit=False)
                    if current_bid is not None:
                        if new_bid.amount > current_bid.amount:
                            valid_bid = True
                    else:
                        if new_bid.amount > listing.bid_amount:
                            valid_bid = True

                    if valid_bid:
                        new_bid.item_on_bid = listing
                        new_bid.bidder = request.user
                        listing.bid_amount = new_bid.amount
                        new_bid.save()
                        listing.save()
                        messages.success(request,
                                         'Bid added successfully')
                        return HttpResponseRedirect(reverse('listing',
                                                    args=(listing.id,)))
                    else:
                        messages.error(request,
                                       'New bids must exceed current bid!')
                        return HttpResponseRedirect(reverse('listing',
                                                    args=(listing.id,)))
                else:
                    messages.error(request, bid_form.errors)

            # Done: Add comments form
            if request.method == 'POST' and 'add_comment' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.commented_listing = listing
                    new_comment.commenter = request.user
                    new_comment.save()
                    messages.success(request,
                                     'Comment added successfully!')
                    return render(request, "auctions/listing.html", {
                            'listing': listing,
                            'comments': comments
                    })
                else:
                    messages.error(request, comment_form.errors)

            # Done: Add watchlist functionality
            if request.user in listing.watched_item.all():
                watching = True
            else:
                watching = False
            if request.method == 'POST' and\
                    'toggle_watchlist' in request.POST:
                if watching:
                    listing.watched_item.remove(request.user)
                    listing.save()
                    messages.success(request,
                                     'Listing Removed from your watchlist')
                    return HttpResponseRedirect(reverse('listing',
                                                args=(listing.id,)))
                else:
                    listing.watched_item.add(request.user)
                    listing.save()
                    messages.success(request,
                                     'Listing Added to your watchlist')
                    return HttpResponseRedirect(reverse('listing',
                                                args=(listing.id,)))

        else:
            '''
            Done: if the current user won the bid on the current listing,
                Show success message: Congrats you won the bid
                otherwise show warning message:
                    This listing is no more available
            '''
            bid_winner = current_bid.bidder
            if request.user == bid_winner:
                return render(request, "auctions/listing.html", {
                    'listing': listing,
                    'winner': bid_winner
                    })
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'comments': comments
        })


@login_required
def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_name = request.POST['category']
        if category_name != '':
            category = categories.filter(name=category_name)
            if not category:
                category = Category(name=category_name)
        else:
            category = None
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            if category:
                category.save()
                listing.category = category
            listing.save()
            messages.success(request, 'Listing added successfully')
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            messages.error(request, form.errors)
            return render(request, "auctions/create_listing.html", {
                'form': ListingForm(),
                'categories': categories,
                 })

    return render(request, "auctions/create_listing.html", {
        'form': ListingForm(),
        'categories': categories,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
