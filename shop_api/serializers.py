from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from shop_api.models import Category, Product, Tag, Comment, BasketItem, Basket


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "product_count",
        )


class TagSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "product_count",
        )


class ProductSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "in_stock",
            # "image",
            "is_active",
            "category",
            "tags",
            "comments_count",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "product",
            "user",
            "text",
            "created_at",
        )
        read_only_fields = (
            "user",
            "created_at",
        )


class BasketItemSerializer(serializers.ModelSerializer):
    product = SerializerMethodField()

    # product = ProductSerializer()
    class Meta:
        model = BasketItem
        fields = ["product", "quantity", "sum"]
        # fields = ['product']
        # read_only_fields = ["product"]

    @staticmethod
    def get_product(obj: BasketItem):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "price": obj.product.price,
            "sum": obj.sum,
            "qqq": obj.product.price * obj.quantity,
        }


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, source="basketitem_set")

    class Meta:
        model = Basket
        fields = ["id", "items", "user", "created_at", "updated_at"]
        read_only_fields = ("id", "items", "user", "created_at", "updated_at")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        basket = Basket.objects.create(**validated_data)
        for item_data in items_data:
            BasketItem.objects.create(basket=basket, **item_data)
        return basket

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        instance.save()

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                BasketItem.objects.create(basket=instance, **item_data)

        return instance


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ["product", "price", "quantity", "sum"]
#         read_only_fields = ["price", "sum"]
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     products = OrderItemSerializer(many=True)
#     status = serializers.ChoiceField(
#         choices=Order.Status, default=Order.Status.CREATED, read_only=True
#     )
#
#     class Meta:
#         model = Order
#         fields = ["id", "user", "status", "products", "created_at", "updated_at"]
#         read_only_fields = ["id", "user", "created_at", "updated_at"]
#
#     def create(self, validated_data):
#         items_data = validated_data.pop("products")
#         order = Order.objects.create(**validated_data)
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)
#         return order
#
#     def update(self, instance, validated_data):
#         items_data = validated_data.pop("products", None)
#         instance.status = validated_data.get("status", instance.status)
#         instance.save()
#
#         if items_data:
#             instance.products.all().delete()
#             for item_data in items_data:
#                 OrderItem.objects.create(order=instance, **item_data)
#
#         return instance
