from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
SETTINGS = {
    "id": 1,
    "options": {
        "seo": {
            "ogImage": None,
            "ogTitle": None,
            "metaTags": None,
            "metaTitle": None,
            "canonicalUrl": None,
            "ogDescription": None,
            "twitterHandle": None,
            "metaDescription": None,
            "twitterCardType": None
        },
        "logo": {
            "id": "862",
            "original": '/logo/logo.png',
            "thumbnail": '/logo/logo.png',
        },
        "currency": "USD",
        "taxClass": 1,
        "siteTitle": "NStore",
        "deliveryTime": [
            {
                "title": "Express Delivery",
                "description": "90 min express delivery"
            },
            {
                "title": "Morning",
                "description": "8.00 AM - 11.00 AM"
            },
            {
                "title": "Noon",
                "description": "11.00 AM - 2.00 PM"
            },
            {
                "title": "Afternoon",
                "description": "2.00 PM - 5.00 PM"
            },
            {
                "title": "Evening",
                "description": "5.00 PM - 8.00 PM"
            }
        ],
        "siteSubtitle": "Your next ecommerce",
        "shippingClass": 1,
        "contactDetails": {
            "contact": "+0123456789",
            "socials": [
                {
                    "url": "https://www.facebook.com/",
                    "icon": "FacebookIcon"
                },
                {
                    "url": "https://twitter.com/home",
                    "icon": "TwitterIcon"
                },
                {
                    "url": "https://www.instagram.com/",
                    "icon": "InstagramIcon"
                }
            ],
            "website": "https://localhost",
            "location": {
                "lat": 0,
                "lng": 0,
                "state": "Ha Noi",
                "country": "Viet Nam",
                "formattedAddress": "Ha Noi, Viet Nam"
            }
        },
        "minimumOrderAmount": 0
    }
}


def settings(request):
    return JsonResponse(SETTINGS)
