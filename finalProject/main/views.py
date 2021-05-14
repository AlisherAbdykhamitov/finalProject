import logging
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import BookCategory, BookProduct, Card, Liked, Order
from main.serializers import BookCategorySerializer, BookProductSerializer, CardSerializer, LikedSerializer, \
    OrderSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = BookCategory.objects.all()
        serializer = BookCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = BookCategory.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookCategorySerializer(user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser, ))
    def create(self, request):
        if request.method == 'POST':
            category_data = request.data

            new_category = BookCategory.objects.create(category_name=category_data['category_name'])
            new_category.save()
            serializer = BookCategorySerializer(new_category)
            logger.debug(f'Category object created, ID: {serializer.instance}')
            logger.info(f'Category object created, ID: {serializer.instance}')
            return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = BookCategory.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Category object deleted, ID: {instance}')
            logger.info(f'Category object deleted, ID: {instance}')
        except Http404:
            logger.error(f'Category object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)



    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser, ))
    def update(self, request, pk):
        category = BookCategory.objects.get(id=pk)
        category.category_name = request.data['category_name']
        category.save()
        serializer = BookCategorySerializer(category)
        logger.debug(f'Category object updated, ID: {serializer.instance}')
        logger.info(f'Category object updated, ID: {serializer.instance}')
        return Response(serializer.data)


class BookViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = BookProduct.objects.all()
        serializer = BookProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = BookProduct.objects.filter(category=pk)
        user = get_list_or_404(queryset)
        serializer = BookProductSerializer(user, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser,))
    def create(self, request):
        book_data = request.data
        category = BookCategory.objects.get(id=book_data['category'])
        new_book = BookProduct.objects.create(product_name=book_data['product_name'],description=book_data['description'],
                                              price=book_data['price'], category=category)
        new_book.save()
        serializer = BookProductSerializer(new_book)
        logger.debug(f'BookProduct object created, ID: {serializer.instance}')
        logger.info(f'BookProduct object created, ID: {serializer.instance}')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = BookProduct.objects.get(id=pk)
            instance.delete()
            logger.debug(f'BookProduct object deleted, ID: {instance}')
            logger.info(f'BookProduct object deleted, ID: {instance}')
        except Http404:
            logger.error(f'BookProduct object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def select(self, request, pk=None):
        queryset = BookProduct.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookProductSerializer(user)
        return Response(serializer.data)

    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser, ))
    def update(self, request, pk):
        book_product = BookProduct.objects.get(id=pk)
        book_product.book_product = request.data['product_name']
        book_product.description = request.data['description']
        book_product.price = request.data['price']
        category = BookCategory.objects.get(category_name=request.data['category'])
        book_product.category = category
        book_product.save()
        serializer = BookProductSerializer(book_product)
        logger.debug(f'book_product object updated, ID: {serializer.instance}')
        logger.info(f'Bbook_product object updated, ID: {serializer.instance}')
        return Response(serializer.data)


@csrf_exempt
def credit_card(request):
    if request.method == 'GET':
        credit_cards = Card.objects.all()
        serializer = CardSerializer(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = CardSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Card object created, ID: {serializer.instance}')
            logger.info(f'Card object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'Card object is not created, ID: {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)



class CardAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Card object updated, ID: {serializer.instance}')
            logger.info(f'Card object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Card object cannot be updated, {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        card = self.get_object(pk)
        card.delete()
        logger.debug(f'Card object deleted')
        logger.info(f'Card object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)



class LikedAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Liked.objects.get(customer_id=pk)
        except Liked.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        liked = self.get_object(pk)
        serializer = LikedSerializer(liked)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        liked = self.get_object(pk)
        serializer = LikedSerializer(liked, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Liked object updated, ID: {serializer.instance}')
            logger.info(f'Liked object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Liked object cannot be updated')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        liked = self.get_object(pk)
        liked.delete()
        logger.debug(f'Liked object deleted')
        logger.info(f'Liked object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def liked(request):
    if request.method == 'GET':
        liked_a = Liked.objects.all()
        serializer = CardSerializer(liked_a, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = LikedSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Liked object created, ID: {serializer.instance}')
            logger.info(f'Liked object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'ShoppingCart object cannot be created, {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)

class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order= self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object updated, ID: {serializer.instance}')
            logger.info(f'Order object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Order object cannot be updated, {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        logger.debug(f'Order object deleted')
        logger.info(f'Order object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def orders(request):
    if request.method == 'GET':
        all_orders = Order.objects.all()
        serializer = OrderSerializer(all_orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = OrderSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object created, ID: {serializer.instance}')
            logger.info(f'Order object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'Order object cannot be created, {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)