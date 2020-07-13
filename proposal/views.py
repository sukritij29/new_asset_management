# Create your views here.
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from asset.decorators import method_permission_classes
from asset.permissions import IsOwner, IsAdmin, IsVerified
from proposal.models import Proposal, Vendor, Documentation
from proposal.serializers import ProposalListSerializer, ProposalMeSerializer, ProposalCreateSerializer, \
    ProposalDetailSerializer, ProposalUpdateSerializer, ApproveSerializer,VendorSerializer, VendorPatchSerializer,\
    DocumentationSerializer, DocumentationDeleteSerializer, \
    SlugVerifySerializer


class ProposalViewSet(ModelViewSet):
    lookup_field = 'proposal_slug'
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)

    def get_queryset(self):

        queryset = Proposal.objects.all()

        if self.action == 'list' and self.request.query_params.get('user_id', None) is None:
            return queryset.exclude(status='Draft').exclude(status='Completed')

        elif self.action == 'list' and self.request.query_params.get('user_id', None) is not None:
            if IsAdmin.has_permission(IsAdmin(), request=self.request, view=ProposalViewSet):
                return queryset.filter(owner__user_id=self.request.query_params.get('user_id'))
            else:
                return queryset.filter(owner__user_id=self.request.query_params.get('user_id'))

        elif self.action == 'retrieve' or self.action == 'approve' or self.action == 'verify_slug' or self.action == 'documentation' or self.action == 'vendors' or self.action == 'update' or self.action == 'partial_update':
            return Proposal.objects.all()

        else:
            return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ProposalListSerializer
        elif self.action == 'me':
            return ProposalMeSerializer
        elif self.action == 'update':
            return ProposalUpdateSerializer
        elif self.action == 'create':
            return ProposalCreateSerializer
        elif self.action == 'approve':
            return ApproveSerializer
        elif self.action == 'vendors' and self.request.method == 'GET':
            return VendorSerializer
        elif self.action == 'vendors' and self.request.method == 'POST':
            return VendorSerializer
        elif self.action == 'vendors' and self.request.method == 'PATCH':
            return VendorPatchSerializer
        elif self.action == 'documentation' and self.request.method == 'GET':
            return DocumentationSerializer
        elif self.action == 'documentation' and self.request.method == 'POST':
            return DocumentationSerializer
        elif self.action == 'documentation' and self.request.method == 'PATCH':
            return DocumentationSerializer
        elif self.action == 'documentation' and self.request.method == 'DELETE':
            return DocumentationDeleteSerializer
        elif self.action == 'verify_slug':
            return SlugVerifySerializer
        else:
            return ProposalDetailSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user}

    @method_permission_classes([IsAuthenticated, IsVerified])
    def retrieve(self, request, *args, **kwargs):
        return super(ProposalViewSet, self).retrieve(request, *args, **kwargs)

    @method_permission_classes([IsAuthenticated, IsOwner, IsVerified])
    def update(self, request, *args, **kwargs):
        return super(ProposalViewSet, self).update(request, *args, **kwargs)

    @method_permission_classes([IsAuthenticated, IsOwner, IsVerified])
    def partial_update(self, request, *args, **kwargs):
        return super(ProposalViewSet, self).partial_update(request, *args, **kwargs)

    @method_permission_classes([IsAuthenticated, IsVerified])
    def destroy(self, request, *args, **kwargs):
        return super(ProposalViewSet, self).destroy(request, *args, **kwargs)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsOwner])
    def me(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        return Response(data=serializer(queryset, many=True).data, status=200)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated, IsAdmin, IsVerified])
    def approve(self, request, *args, **kwargs):
        proposal = self.get_object()
        if proposal.status not in ['Approved', 'Ongoing', 'Completed']:
            proposal.approved_by = self.request.user
            proposal.status = 'Approved'
            proposal.save()
            return Response({'detail': "The proposal has been approved"}, status=200)
        else:
            return Response({'detail': "This proposal is already approved"}, status=400)

    @action(methods=['get', 'post', 'patch'], detail=True)
    def vendors(self, request, *args, **kwargs):
        proposal = self.get_object()

        if request.method == 'GET':
            data = self.get_serializer_class()(proposal.vendors.all(), many=True).data
            return Response(data=data, status=200)

        elif request.method == 'POST':
            if IsOwner.has_object_permission(IsOwner(), request=self.request, view=ProposalViewSet,
                                             obj=self.get_object()):
                data = self.get_serializer_class()(request.data).data
                vendor = Vendor.objects.create(proposal=proposal, **data)
                return Response({"detail": "The vendor has been created",
                                 "vendor_id": vendor.vendor_id,
                                 "proposal": proposal.proposal_slug,
                                 "email_address": vendor.email_address
                                 }, status=201)
            else:
                return Response({
                    "detail": "You do not have permissions to perform this action. Only the owner or an Admin of the proposal can create a vendor"})

    @action(methods=['get', 'post', 'delete'], detail=True)
    def documentation(self, request, *args, **kwargs):

        proposal = self.get_object()
        if request.method == 'GET':
            data = self.get_serializer_class()(proposal.documentation.all(), many=True).data
            return Response(data=data, status=200)
        elif request.method == 'POST':
            print("Request Received")
            data = self.get_serializer_class()(request.data).data
            try:
                document = Documentation.objects.create(proposal=proposal, **data)
                print("Document Created")

            except IntegrityError:
                return Response({'detail': "A document with this id already exists in this proposal"})

            return Response({
                "detail": "Document added to proposal",
                'proposal': proposal.proposal_slug,
                'document_id': document.document_id,
                'document_title': document.title
                }, status=201)

        elif request.method == 'DELETE':
            if IsOwner.has_object_permission(IsOwner(), request, ProposalViewSet, self.get_object()):
                proposal = self.get_object()
                document_id = self.get_serializer_class()(request.data).data.get('document_id')
                try:
                    document = proposal.documentation.get(document_id=document_id)
                    document.delete()
                except ObjectDoesNotExist as e:
                    print(e)
                    return Response({"detail": "Such a document does not exist"}, status=400)

                return Response({"detail": "The document was deleted", 'proposal': proposal.proposal_slug}, status=201)
            else:
                return Response({
                    "detail": "You do not have permission to perform this action. Only Admins and the owner of this proposal can delete documentation"})


    @action(methods=['post'], detail=False)
    def verify_slug(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.data)
        print(Proposal.objects.all().values_list('proposal_slug', flat=True))
        if serializer.data.get('slug') in Proposal.objects.all().values_list('proposal_slug', flat=True):
            return Response({
                'detail': "This slug is already in use"
            }, status=400)
        else:
            return Response({
                'detail': "This slug is available",
            }, status=200)
