from rest_framework.authtoken.models import Token
from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework import status
from django.contrib import auth

import pytz


class TokenMod:
    VALIDATE = 3

    def __init__(self):
        pass

    def tokenAuth(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return {'message': 'None token'}, status.HTTP_401_UNAUTHORIZED
        try:
            token = Token.objects.get(key=token)
            token.created = timezone.now()
            token.save()
        except Exception as ex:
            return {'message': str(ex)}, status.HTTP_401_UNAUTHORIZED

        return token.user

    def createToken(self, request):
        try:
            user = auth.authenticate(request, username=request.data["username"], password=request.data["password"])
        except KeyError:
            return {'error_code': '0', 'error_msg': 'Missing parameters'}, status.HTTP_400_BAD_REQUEST

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            d = timedelta(days=self.VALIDATE)

            start = token.created.replace(tzinfo=pytz.UTC)
            dest = (datetime.now()).replace(tzinfo=pytz.UTC)
            end = (token.created + d).replace(tzinfo=pytz.UTC)

            if start > dest or dest > end:
                token.delete()

            token.created = timezone.now()
            token.save()

            return {"token": token.key, "created": token.created}, status.HTTP_200_OK
        else:
            return {'error_code': '2', 'error_msg': 'Auth fail'}, status.HTTP_401_UNAUTHORIZED
