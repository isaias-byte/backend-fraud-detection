from rest_framework import viewsets
from .models import Transactions
from .serializer import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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