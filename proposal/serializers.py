from rest_framework import serializers

from proposal.models import Proposal, Vendor, Documentation
from users_module.models import User


class ProposalListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = '__all__'

    def get_owner(self, instance):
        user = instance.owner
        return {
            'employee_id': user.employee_id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }


class ProposalMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
        read_only_fields = ('proposal_slug', 'title', 'due_date')


class ProposalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ('form_complete',)
        read_only_fields = ('title', 'owner')


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = (
            'proposal_slug', 'title', 'owner', 'description', 'due_date', 'delivery_date', 'email', 'address')
        read_only_fields = ('proposal_slug',)


class ProposalDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        exclude = ('form_complete',)

    def get_owner(self, instance):
        user = instance.owner
        return {
            'employee_id': user.employee_id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }


class ApproveSerializer(serializers.Serializer):
    pass


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['vendor_id', 'proposal']


class VendorPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['vendor_id', 'proposal']


class DocumentationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=1000, required=True)
    link = serializers.URLField(required=False)
    amount = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = Documentation
        fields = '__all__'
        read_only_fields = ['proposal', 'document_id']


class DocumentationDeleteSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()


class SlugVerifySerializer(serializers.Serializer):
    slug = serializers.SlugField()
