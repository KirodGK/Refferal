from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .utils import generate_auth_code, generate_invite_code
from .serializers import ProfileSerializer
from django.core.cache import cache
from time import sleep

class RequestCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = generate_auth_code()
        cache.set(phone, code, timeout=300)
        sleep(2)
        return Response({"message": f"Код отправлен на номер {phone} (код: {code})"})

class VerifyCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        real_code = cache.get(phone)

        if str(real_code) != str(code):
            return Response({"error": "Неверный код"}, status=400)

        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.invite_code = generate_invite_code()
            user.save()

        return Response({"token": phone})

class ProfileView(APIView):
    def get(self, request):
        phone = request.headers.get("Authorization")
        user = User.objects.filter(phone=phone).first()
        return Response(ProfileSerializer(user).data)

    def post(self, request):
        phone = request.headers.get("Authorization")
        user = User.objects.filter(phone=phone).first()
        if user.referred_by:
            return Response({"error": "Инвайт-код уже активирован"}, status=400)

        code = request.data.get("invite_code")
        if code == user.invite_code:
            return Response({"error": "Нельзя ввести свой код"}, status=400)

        try:
            inviter = User.objects.get(invite_code=code)
        except User.DoesNotExist:
            return Response({"error": "Код не найден"}, status=404)

        user.referred_by = inviter
        user.save()
        return Response({"message": "Код успешно активирован"})
