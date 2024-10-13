from django.http import JsonResponse
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.models import User  # Importing User model
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
import logging
import json
from .populate import initiate
from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review
)

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


@csrf_exempt
def login_user(request):
    # Get username and password from request body
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response_data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        response_data = {
            "userName": username,
            "status": "Unauthorized"
        }

    return JsonResponse(response_data)


def logout_request(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        return JsonResponse({"userName": username})
    else:
        return JsonResponse(
            {"error": "User is not logged in."},
            status=400
        )


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        })

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({
        "userName": username,
        "status": "Authenticated"
    })


def get_dealerships(request, state="All"):
    endpoint = (
        "/fetchDealers" if state == "All"
        else f"/fetchDealers/{state}"
    )
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment_response = (
                analyze_review_sentiments(
                    review_detail['review']
                )
            )
            review_detail['sentiment'] = sentiment_response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error in posting review: {e}")
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })

    return JsonResponse({
        "status": 403,
        "message": "Unauthorized"
    })


def get_cars(request):
    # Count the number of car makes in the database
    count = CarMake.objects.count()

    # If there are no car makes, call the initiate function to populate
    if count == 0:
        initiate()

    # Fetch car models with their associated car make using select_related
    car_models = CarModel.objects.select_related('make')

    # Create a list of dictionaries to hold car model and make data
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.make.name
        }
        for car_model in car_models
    ]

    # Return the list of car models as a JSON response
    return JsonResponse({"CarModels": cars})

# Make sure to add a newline at the end of the file
