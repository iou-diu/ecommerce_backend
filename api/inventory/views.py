# views.py
from decimal import Decimal, InvalidOperation
from django.db import transaction
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import status as ApiStatus
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView
from apps.ecom.models import ProductVariant, Tax
from apps.inventory.models import PO, AdditionalCost, POAdditionalCost, POItem, PurchaseOrder, PurchaseOrderItem, \
    Requisition, Supplier
from api.inventory.serializers import POSerializer, ProductVariantSerializer, PublicProductVariantSerializer, \
    PurchaseOrderSerializer, RequisitionItemSerializer, RequisitionSerializer, SupplierSerializer
from apps.user.permission import IsAdminOrStaff


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  #

    # Add search functionality for SKU, UPC, and product name
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku', 'upc', 'product__name']


class PublicProductVariantViewSet(viewsets.ReadOnlyModelViewSet):  # Public access, read-only
    queryset = ProductVariant.objects.all()
    serializer_class = PublicProductVariantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku', 'upc', 'product__name']

# Admin or Staff Only


class RequisitionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrStaff]
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']  # Allows search by Requisition ID
    filterset_fields = ['id']  # Also allows filtering by Requisition ID

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        requisition = self.get_object()
        serializer = self.get_serializer(requisition)
        return Response(serializer.data)


# Admin or Staff Only
class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrStaff]
    queryset = Supplier.objects.all().order_by('-id')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'phone_number', ]
    search_fields = ['name', 'phone_number']

    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TestPayloadView(APIView):
    permission_classes = [IsAuthenticated]  # Optional: use if you want authentication

    def post(self, request, *args, **kwargs):
        # Log the received data for debugging
        print("Received payload:", request.data)

        # Return the received payload back to the client
        return Response(request.data, status=status.HTTP_200_OK)


def calculate_tax(amount: Decimal, tax_value: Decimal, tax_type: str) -> Decimal:
    """
    Calculate the tax amount based on the tax type (flat or percentage).
    """
    try:
        if tax_type == 'percentage':
            return (amount * tax_value) / Decimal("100")
        elif tax_type == 'flat':
            return tax_value
    except (InvalidOperation, TypeError, ValueError) as e:
        print(f"Error calculating tax: {e}")
    return Decimal("0.00")  # Fallback to 0.00 if calculation fails


def calculate_discount(amount: Decimal, discount_value: Decimal, discount_type: str) -> Decimal:
    """
    Calculate the discount amount based on the discount type (flat or percentage).
    """
    try:
        if discount_type == 'percentage':
            return (amount * discount_value) / Decimal("100")
        elif discount_type == 'flat':
            return discount_value
    except (InvalidOperation, TypeError, ValueError) as e:
        print(f"Error calculating discount: {e}")
    return Decimal("0.00")


class POCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  #

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                # Retrieve main data and related objects
                requisition = data.get("requisition")
                supplier = data.get("supplier")
                requisition_obj = Requisition.objects.get(id=requisition)
                supplier_obj = Supplier.objects.get(id=supplier)
                order_date = data.get("order_date")
                expected_delivery_date = data.get("expected_delivery_date")
                status = data.get("status", "draft")
                notes = data.get("notes", "")
                global_discount_type = data.get("global_discount_type")
                global_discount_value = Decimal(data.get("global_discount_value", "0"))
                shipping_info = data.get("shipping_info", "")
                shipping_cost = Decimal(data.get("shipping_cost", "0"))

                purchase_tax_id = data.get("purchase_tax_id")

                purchase_tax_name = purchase_tax_type = None
                purchase_tax_value = Decimal("0")

                paymentDays = data.get("paymentDays")
                paymentMonths = data.get("paymentMonths")

                if purchase_tax_id:
                    tax = Tax.objects.filter(id=purchase_tax_id).first()
                    if tax:
                        purchase_tax_name = tax.name
                        purchase_tax_type = tax.tax_type
                        purchase_tax_value = Decimal(tax.value)

                # Create PurchaseOrder entry
                purchase_order = PO.objects.create(
                    requisition=requisition_obj,
                    supplier=supplier_obj,

                    expected_delivery_date=order_date,
                    status=status,
                    notes=notes,
                    global_discount_type=global_discount_type,
                    global_discount_value=global_discount_value,
                    shipping_info=shipping_info,
                    shipping_cost=shipping_cost,
                    purchase_tax_name=purchase_tax_name,
                    purchase_tax_type=purchase_tax_type,
                    purchase_tax_value=purchase_tax_value,
                    payload=data,
                    paymentMonths=paymentMonths,
                    paymentDays=paymentDays
                )

                # Process items and calculate total
                items_data = data.get("items", [])
                total_cost = Decimal("0")

                for item_data in items_data:
                    sku = item_data.get("variant")
                    quantity_ordered = int(item_data.get("quantity_ordered", 1))
                    price_per_unit = Decimal(item_data.get("price_per_unit", "0"))
                    discount = Decimal(item_data.get("discount", "0"))

                    variant = ProductVariant.objects.filter(sku=sku).first()
                    if not variant:
                        raise ValueError(f"Variant with SKU '{sku}' does not exist.")

                    # Calculate line total
                    sub_total = quantity_ordered * price_per_unit
                    discount_amount = (sub_total * discount) / Decimal("100")
                    net_cost = sub_total - discount_amount

                    # Default tax amount to 0.00
                    tax_amount = Decimal("0.00")
                    line_total = Decimal("0.00")

                    # Calculate tax if tax_id is provided
                    tax_id = item_data.get("tax")

                    item_tax = None
                    if tax_id:
                        item_tax = Tax.objects.filter(id=tax_id).first()
                        if item_tax:
                            try:
                                tax_amount = calculate_tax(net_cost, item_tax.value, item_tax.tax_type)

                            except (InvalidOperation, TypeError, ValueError) as e:
                                print(f"Invalid tax value for {variant}: {e}")
                                tax_amount = Decimal("0.00")  # Fallback to 0.00 if tax is invalid

                    # Calculate final line total
                    line_total = net_cost + tax_amount
                    new_line_total = Decimal(line_total)
                    new_tax_amount = Decimal(tax_amount)

                    total_cost += line_total

                    print("=========", variant, Decimal(tax_amount), line_total)

                    # Create PurchaseOrderItem entry
                    POItem.objects.create(
                        purchase_order=purchase_order,
                        variant=variant,
                        quantity_ordered=quantity_ordered,
                        price_per_unit=price_per_unit,
                        discount=discount,
                        tax=new_tax_amount if tax_id else Decimal("0.00"),  # Pass tax_amount even if it's 0.00
                        line_total=new_line_total,
                        tax_model=item_tax if item_tax else None,

                    )

                # calculate purchase tax on  cost

                print("Total Line Cost:", total_cost)

                purchase_tax_on_line_total = calculate_tax(total_cost, purchase_tax_value, purchase_tax_type)

                print("Purchase Tax Cost:", purchase_tax_on_line_total)

                sub_total_after_purchase_tax = total_cost + purchase_tax_on_line_total

                # Calculate additional costs
                additional_cost_data = data.get("additional_costs", [])
                additional_cost_total = sum(Decimal(cost["value"]) for cost in additional_cost_data)

                # Create AdditionalCost entries
                for cost in additional_cost_data:
                    POAdditionalCost.objects.create(
                        purchase_order=purchase_order,
                        description=cost.get("key"),
                        amount=Decimal(cost.get("value", "0"))
                    )

                # add additional_cost + shipping_cost with sub_total_after_purchase_tax
                sub_total_with_additional_cost = sub_total_after_purchase_tax + additional_cost_total + shipping_cost

                # apply global discount calculate_discount

                final_total_after_global_discount = sub_total_with_additional_cost - calculate_discount(
                    sub_total_with_additional_cost, global_discount_value, global_discount_type)

                purchase_order.final_total_cost = final_total_after_global_discount
                purchase_order.save()

            return Response({
                "message": "Purchase order created successfully",
                "purchase_order_id": purchase_order.id,
                "final_total_cost": purchase_order.final_total_cost
            }, status=ApiStatus.HTTP_201_CREATED)

        except Exception as e:
            transaction.rollback()
            return Response({
                "message": "Failed to create purchase order",
                "error": str(e)
            }, status=ApiStatus.HTTP_400_BAD_REQUEST)


class PurchaseOrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  #

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                # Retrieve main data and related objects
                requisition = data.get("requisition")
                supplier = data.get("supplier")
                requisition_obj = Requisition.objects.get(id=requisition)
                purchase_order_obj = PO.objects.get(id=data.get('selectedPO'))
                supplier_obj = Supplier.objects.get(id=supplier)
                order_date = data.get("order_date")
                expected_delivery_date = data.get("expected_delivery_date")
                status = data.get("status", "draft")
                notes = data.get("notes", "")
                global_discount_type = data.get("global_discount_type")
                global_discount_value = Decimal(data.get("global_discount_value", "0"))
                shipping_info = data.get("shipping_info", "")
                shipping_cost = Decimal(data.get("shipping_cost", "0"))

                purchase_tax_id = data.get("purchase_tax_id")

                purchase_tax_name = purchase_tax_type = None
                purchase_tax_value = Decimal("0")

                paymentDays = data.get("paymentDays")
                paymentMonths = data.get("paymentMonths")

                if purchase_tax_id:
                    tax = Tax.objects.filter(id=purchase_tax_id).first()
                    if tax:
                        purchase_tax_name = tax.name
                        purchase_tax_type = tax.tax_type
                        purchase_tax_value = Decimal(tax.value)

                # Create PurchaseOrder entry
                purchase_order = PurchaseOrder.objects.create(
                    requisition=requisition_obj,
                    supplier=supplier_obj,
                    purchase_order=purchase_order_obj,

                    expected_delivery_date=order_date,
                    status=status,
                    notes=notes,
                    global_discount_type=global_discount_type,
                    global_discount_value=global_discount_value,
                    shipping_info=shipping_info,
                    shipping_cost=shipping_cost,
                    purchase_tax_name=purchase_tax_name,
                    purchase_tax_type=purchase_tax_type,
                    purchase_tax_value=purchase_tax_value,
                    payload=data,
                    paymentMonths=paymentMonths,
                    paymentDays=paymentDays
                )

                # Process items and calculate total
                items_data = data.get("items", [])
                total_cost = Decimal("0")

                for item_data in items_data:
                    sku = item_data.get("variant")
                    quantity_ordered = int(item_data.get("quantity_ordered", 1))
                    price_per_unit = Decimal(item_data.get("price_per_unit", "0"))
                    discount = Decimal(item_data.get("discount", "0"))

                    variant = ProductVariant.objects.filter(sku=sku).first()
                    if not variant:
                        raise ValueError(f"Variant with SKU '{sku}' does not exist.")

                    # Calculate line total
                    sub_total = quantity_ordered * price_per_unit
                    discount_amount = (sub_total * discount) / Decimal("100")
                    net_cost = sub_total - discount_amount

                    # Default tax amount to 0.00
                    tax_amount = Decimal("0.00")
                    line_total = Decimal("0.00")

                    # Calculate tax if tax_id is provided
                    tax_id = item_data.get("tax")

                    item_tax = None
                    if tax_id:
                        item_tax = Tax.objects.filter(id=tax_id).first()
                        if item_tax:
                            try:
                                tax_amount = calculate_tax(net_cost, item_tax.value, item_tax.tax_type)

                            except (InvalidOperation, TypeError, ValueError) as e:
                                print(f"Invalid tax value for {variant}: {e}")
                                tax_amount = Decimal("0.00")  # Fallback to 0.00 if tax is invalid

                    # Calculate final line total
                    line_total = net_cost + tax_amount
                    new_line_total = Decimal(line_total)
                    new_tax_amount = Decimal(tax_amount)

                    total_cost += line_total

                    print("=========", variant, Decimal(tax_amount), line_total)

                    profit_margin_percentage = Decimal(item_data.get("profit_margin_percentage", "0"))
                    expected_selling_price = Decimal(item_data.get("expected_selling_price", "0"))
                    selling_tax = item_data.get("selling_tax", None)
                    if selling_tax:
                        selling_tax_model = Tax.objects.filter(id=selling_tax).first()

                    # Create PurchaseOrderItem entry
                    PurchaseOrderItem.objects.create(
                        purchase_order=purchase_order,
                        variant=variant,
                        quantity_ordered=quantity_ordered,
                        price_per_unit=price_per_unit,
                        discount=discount,
                        tax=new_tax_amount if tax_id else Decimal("0.00"),  # Pass tax_amount even if it's 0.00
                        line_total=new_line_total,
                        tax_model=item_tax if item_tax else None,

                        profit_margin_percentage=profit_margin_percentage,
                        expected_selling_price=expected_selling_price,
                        selling_tax_model=selling_tax_model if selling_tax else None
                    )

                # calculate purchase tax on  cost

                print("Total Line Cost:", total_cost)

                purchase_tax_on_line_total = calculate_tax(total_cost, purchase_tax_value, purchase_tax_type)

                print("Purchase Tax Cost:", purchase_tax_on_line_total)

                sub_total_after_purchase_tax = total_cost + purchase_tax_on_line_total

                # Calculate additional costs
                additional_cost_data = data.get("additional_costs", [])
                additional_cost_total = sum(Decimal(cost["value"]) for cost in additional_cost_data)

                # Create AdditionalCost entries
                for cost in additional_cost_data:
                    AdditionalCost.objects.create(
                        purchase_order=purchase_order,
                        description=cost.get("key"),
                        amount=Decimal(cost.get("value", "0"))
                    )

                # add additional_cost + shipping_cost with sub_total_after_purchase_tax
                sub_total_with_additional_cost = sub_total_after_purchase_tax + additional_cost_total + shipping_cost

                # apply global discount calculate_discount

                final_total_after_global_discount = sub_total_with_additional_cost - calculate_discount(
                    sub_total_with_additional_cost, global_discount_value, global_discount_type)

                purchase_order.final_total_cost = final_total_after_global_discount
                purchase_order.save()

            return Response({
                "message": "Purchase order created successfully",
                "purchase_order_id": purchase_order.id,
                "final_total_cost": purchase_order.final_total_cost
            }, status=ApiStatus.HTTP_201_CREATED)

        except Exception as e:
            transaction.rollback()
            return Response({
                "message": "Failed to create purchase order",
                "error": str(e)
            }, status=ApiStatus.HTTP_400_BAD_REQUEST)


class PurchaseOrderUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def put(self, request, pk, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                # Retrieve the existing purchase order
                purchase_order = PurchaseOrder.objects.get(pk=pk)

                # Update main fields
                requisition_id = data.get("requisition", purchase_order.requisition.id)
                supplier_id = data.get("supplier", purchase_order.supplier.id)
                requisition_obj = Requisition.objects.get(id=requisition_id)
                supplier_obj = Supplier.objects.get(id=supplier_id)
                order_date = data.get("order_date", purchase_order.order_date)
                expected_delivery_date = data.get("expected_delivery_date", purchase_order.expected_delivery_date)
                status = data.get("status", purchase_order.status)
                notes = data.get("notes", purchase_order.notes)
                global_discount_type = data.get("global_discount_type", purchase_order.global_discount_type)
                global_discount_value = Decimal(data.get("global_discount_value", purchase_order.global_discount_value))
                shipping_info = data.get("shipping_info", purchase_order.shipping_info)
                shipping_cost = Decimal(data.get("shipping_cost", purchase_order.shipping_cost))

                purchase_tax_id = data.get("purchase_tax_id")

                purchase_tax_name = purchase_tax_type = None
                purchase_tax_value = Decimal("0")

                payment_days = data.get("paymentDays", purchase_order.paymentDays)
                payment_months = data.get("paymentMonths", purchase_order.paymentMonths)

                if purchase_tax_id:
                    tax = Tax.objects.filter(id=purchase_tax_id).first()
                    if tax:
                        purchase_tax_name = tax.name
                        purchase_tax_type = tax.tax_type
                        purchase_tax_value = Decimal(tax.value)

                # Update PurchaseOrder fields
                purchase_order.requisition = requisition_obj
                purchase_order.supplier = supplier_obj

                purchase_order.expected_delivery_date = expected_delivery_date
                purchase_order.status = status
                purchase_order.notes = notes
                purchase_order.global_discount_type = global_discount_type
                purchase_order.global_discount_value = global_discount_value
                purchase_order.shipping_info = shipping_info
                purchase_order.shipping_cost = shipping_cost
                purchase_order.purchase_tax_name = purchase_tax_name
                purchase_order.purchase_tax_type = purchase_tax_type
                purchase_order.purchase_tax_value = purchase_tax_value
                purchase_order.paymentDays = payment_days
                purchase_order.paymentMonths = payment_months
                purchase_order.payload = data  # Optional: Store payload for auditing

                purchase_order.save()

                # Remove existing items and additional costs
                purchase_order.items.all().delete()
                purchase_order.additional_costs.all().delete()

                # Process items and calculate total
                items_data = data.get("items", [])
                total_cost = Decimal("0")

                for item_data in items_data:
                    variant_id = item_data.get("variant")  # Now expecting variant ID
                    quantity_ordered = int(item_data.get("quantity_ordered", 1))
                    price_per_unit = Decimal(item_data.get("price_per_unit", "0"))
                    discount = Decimal(item_data.get("discount", "0"))

                    variant = ProductVariant.objects.filter(sku=variant_id).first()
                    if not variant:
                        raise ValueError(f"Variant with ID '{variant_id}' does not exist.")

                    # Calculate line total
                    sub_total = quantity_ordered * price_per_unit
                    discount_amount = (sub_total * discount) / Decimal("100")
                    net_cost = sub_total - discount_amount

                    # Default tax amount to 0.00
                    tax_amount = Decimal("0.00")
                    line_total = Decimal("0.00")

                    # Calculate tax if tax_id is provided
                    tax_id = item_data.get("tax")
                    item_tax = None
                    if tax_id:
                        item_tax = Tax.objects.filter(id=tax_id).first()
                        if item_tax:
                            try:
                                tax_amount = calculate_tax(net_cost, item_tax.value, item_tax.tax_type)
                            except (InvalidOperation, TypeError, ValueError) as e:
                                print(f"Invalid tax value for {variant}: {e}")
                                tax_amount = Decimal("0.00")  # Fallback to 0.00 if tax is invalid

                    # Calculate final line total
                    line_total = net_cost + tax_amount
                    new_line_total = Decimal(line_total)
                    new_tax_amount = Decimal(tax_amount)

                    total_cost += line_total

                    profit_margin_percentage = Decimal(item_data.get("profit_margin_percentage", "0"))
                    expected_selling_price = Decimal(item_data.get("expected_selling_price", "0"))
                    selling_tax = item_data.get("selling_tax", None)
                    if selling_tax:
                        selling_tax_model = Tax.objects.filter(id=selling_tax).first()

                    # Create PurchaseOrderItem entry
                    PurchaseOrderItem.objects.create(
                        purchase_order=purchase_order,
                        variant=variant,
                        quantity_ordered=quantity_ordered,
                        price_per_unit=price_per_unit,
                        discount=discount,
                        tax=new_tax_amount if tax_id else Decimal("0.00"),
                        line_total=new_line_total,
                        tax_model=item_tax if item_tax else None,

                        profit_margin_percentage=profit_margin_percentage,
                        expected_selling_price=expected_selling_price,
                        selling_tax_model=selling_tax_model if selling_tax else None
                    )

                # Calculate purchase tax on total cost
                purchase_tax_on_line_total = calculate_tax(total_cost, purchase_tax_value, purchase_tax_type)
                sub_total_after_purchase_tax = total_cost + purchase_tax_on_line_total

                # Calculate additional costs
                additional_cost_data = data.get("additional_costs", [])
                additional_cost_total = Decimal("0")
                for cost in additional_cost_data:
                    amount = Decimal(cost.get("amount", "0"))
                    description = cost.get("description", "")
                    AdditionalCost.objects.create(
                        purchase_order=purchase_order,
                        description=description,
                        amount=amount
                    )
                    additional_cost_total += amount

                # Add additional_costs and shipping_cost to subtotal
                sub_total_with_additional_cost = sub_total_after_purchase_tax + additional_cost_total + shipping_cost

                # Apply global discount
                total_discount_amount = calculate_discount(sub_total_with_additional_cost, global_discount_value,
                                                           global_discount_type)
                final_total_after_global_discount = sub_total_with_additional_cost - total_discount_amount

                purchase_order.final_total_cost = final_total_after_global_discount
                purchase_order.save()

                return Response({
                    "message": "Purchase order updated successfully",
                    "purchase_order_id": purchase_order.id,
                    "final_total_cost": str(purchase_order.final_total_cost)
                }, status=ApiStatus.HTTP_200_OK)

        except PurchaseOrder.DoesNotExist:
            return Response({"detail": "Not found."}, status=ApiStatus.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.rollback()
            return Response({
                "message": "Failed to update purchase order",
                "error": str(e)
            }, status=ApiStatus.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
            serializer = self.get_serializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"message": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)


class POViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    queryset = PO.objects.all().order_by('-id')
    serializer_class = POSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['id']


class PODetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    queryset = PO.objects.all()
    serializer_class = POSerializer

    def get(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
            serializer = self.get_serializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"message": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)
