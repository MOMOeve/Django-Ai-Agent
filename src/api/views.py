from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document

from .agent_service import invoke_agent
from .serializers import ChatSerializer, DocumentSerializer, LoginSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "CSRF cookie set"})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response({"detail": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response({
            "id": user.id,
            "username": user.username,
        })


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "已退出登录"})


class MeView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
        })


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result = invoke_agent(
                agent_type=data["agent_type"],
                message=data["message"],
                user_id=request.user.id,
                thread_id=data.get("thread_id") or None,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response(
                {"detail": f"Agent 调用失败: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(result)


class DocumentListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "未登录"}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Document.objects.filter(
            owner_id=request.user.pk,
            active=True,
        ).order_by("-updated_at")[:20]
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)
