import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User

# ==========================
# INSCRIPTION
# ==========================
@csrf_exempt
def register(request):

    if request.method == "POST":

        data = json.loads(request.body)

        if User.objects.filter(username=data["email"]).exists():
            return JsonResponse({"error": "Email déjà utilisé"}, status=400)

        User.objects.create(
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"]),
            role=data["role"],
            ville=data["ville"],
            telephone=data["telephone"],
            approved=True
        )

        return JsonResponse({"message": "Compte créé avec succès"}, status=201)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


# ==========================
# CONNEXION
# ==========================
@csrf_exempt
def login_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user = authenticate(
            request,
            username=data["email"],
            password=data["password"]
        )

        if user:
            return JsonResponse({
                "message": "Connexion réussie",
                "role": user.role
            })

        return JsonResponse({"error": "Identifiants incorrects"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)