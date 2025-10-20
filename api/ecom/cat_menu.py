from rest_framework import serializers
from apps.ecom.models import Category, Product
from apps.solutions.models import Solution


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'is_active']


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['title', 'slug']


class ChildCategorySerializer(serializers.ModelSerializer):
    # products = ProductListSerializer(many=True, read_only=True)
    solutions = SolutionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'solutions']


class ParentCategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'children']


from rest_framework.views import APIView
from rest_framework.response import Response
from apps.ecom.models import Category
from rest_framework.permissions import AllowAny


class MenuCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        parents = Category.objects.filter(parent__isnull=True, is_active=True, for_solution=True)
        serializer = ParentCategorySerializer(parents, many=True)
        return Response(serializer.data)
