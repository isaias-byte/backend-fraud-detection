import random
from rest_framework import viewsets
from .models import Transactions, TransactionsTest, UserInfo
from .serializer import TransactionSerializer, TransactionTestSerializer, UserInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def transactions(request):
    """
    List all transactions or filter by user.
    """
    queryset = Transactions.objects.all().order_by('id')[:1000]
    serializer = TransactionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_transaction_test_populate(request):
    serializer = TransactionTestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_transaction(request, id):
    # Verify if the ID is provided
    try:
        transaction = Transactions.objects.get(id=id)
    except Transactions.DoesNotExist:
        return Response(
            {"detail": "Object not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Data validation
    serializer = TransactionSerializer(transaction, data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "detail": "Invalid data.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Guarda los cambios
    serializer.save()
    
    return Response(
        {
            "detail": "Successfully updated.",
            "id": id,
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_transaction(request, id):
    try:
        item = Transactions.objects.get(id=id)
    except Transactions.DoesNotExist:
        return Response(
            {"detail": "Object not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    item.delete()
    return Response(
        {"detail": "Transaction successfully deleted.", id: id},
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(['GET'])
def all_fraudulent_transactions(request):
    try:        
        search_term = request.query_params.get('search', None)

        fraudulent_txs_query = TransactionsTest.objects.filter(fraud=True).select_related('user')

        if search_term:            
            fraudulent_txs_query = fraudulent_txs_query.filter(
                Q(user__name__icontains=search_term) |
                Q(user__card_last_four__icontains=search_term)
            )
        
        fraudulent_txs_query = fraudulent_txs_query.order_by('-id')
        
        paginator = PageNumberPagination()
        paginated_txs = paginator.paginate_queryset(fraudulent_txs_query, request)
        
        response_data = []
        for tx in paginated_txs:            
            if not tx.user:
                continue
                           
            user_data = UserInfoSerializer(tx.user).data
               
            user_data['used_chip'] = tx.used_chip
            
            user_data['transaction_id'] = tx.id

            response_data.append(user_data)
      
        return paginator.get_paginated_response(response_data)
    
    except Exception as e:        
        return Response(
            {"error": f"Ocurrió un error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def create_transaction_test(request):
    serializer = UserInfoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data

    try:
        user_object, created = UserInfo.objects.get_or_create(            
            name=validated_data['name'],
            card_bin=validated_data['card_bin'],
            card_last_four=validated_data['card_last_four'],
                       
            defaults={
                'card_expiry_month': validated_data.get('card_expiry_month'),
                'card_expiry_year': validated_data.get('card_expiry_year')
            }
        )
    except Exception as e:        
        return Response(
            {"error": f"Error en la base de datos al buscar/crear usuario: {e}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    dist_home = random.uniform(0.5, 60.0) if random.random() > 0.05 else random.uniform(60.0, 800.0)
    dist_last = random.uniform(0.1, 10.0) if random.random() > 0.05 else random.uniform(10.0, 60.0)
    ratio = random.uniform(0.1, 3.0) if random.random() > 0.05 else random.uniform(3.0, 7.0)
    
    repeat_retailer = True if random.random() > 0.1 else False
    used_chip = random.choice([True, False])
    used_pin_number = True if random.random() < 0.1 else False
    online_order = random.choice([True, False])
    fraud = True if random.random() < 0.07 else False

    try:
        new_transaction = TransactionsTest(
            distance_from_home=dist_home,
            distance_from_last_transaction=dist_last,
            ratio_to_median_purchase_price=ratio,
            repeat_retailer=repeat_retailer,
            used_chip=used_chip,
            used_pin_number=used_pin_number,
            online_order=online_order,
            fraud=fraud,
            user=user_object
        )
        new_transaction.save()
                
        response_data = UserInfoSerializer(user_object).data
       
        if created:
            print(f"The user was created {user_object.id} and the transaction was added {new_transaction.id}")
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print(f"The user was found {user_object.id} and the transaction was added {new_transaction.id}")            
            return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"The transaction could not be created for the user: {user_object.id, user_object.name}: {e}")
        return Response(
            {"error": f"No se pudo crear la transacción: {e}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )     