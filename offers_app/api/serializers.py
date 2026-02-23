from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(read_only=True)  # MYA: offer wird serverseitig gesetzt

    class Meta:
        model = OfferDetail
        fields = "__all__"

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        request = self.context.get("request")

        offer = Offer.objects.create(
        user=request.user,   # 🔥 DAS IST WICHTIG
        **validated_data
    )

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            # Update Details einzeln über ID (oder komplett ersetzen)
            for detail_data in details_data:
                detail_id = detail_data.get("id", None)
                if detail_id:
                    detail_obj = OfferDetail.objects.get(id=detail_id, offer=instance)
                    for attr, value in detail_data.items():
                        if attr != "id":
                            setattr(detail_obj, attr, value)
                    detail_obj.save()

        return instance