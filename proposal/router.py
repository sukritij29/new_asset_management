from rest_framework import routers

from proposal.views import ProposalViewSet

ProposalRouter = routers.DefaultRouter()

ProposalRouter.register('proposals', ProposalViewSet, basename='Proposal')
