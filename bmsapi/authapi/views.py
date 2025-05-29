from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import auth, credentials
from django.middleware import csrf
import os
import json

# Initialize Firebase Admin SDK (do this only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'firebase_credentials.json'))
    firebase_admin.initialize_app(cred)

# Create your views here.

class FirebaseLoginView(APIView):
    def post(self, request):
        id_token = request.data.get('idToken')
        if not id_token:
            return Response({'error': 'No ID token provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            # Generate a CSRF token as a simple session token (for demo)
            session_token = csrf.get_token(request)
            return Response({'session_token': session_token, 'uid': uid}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
