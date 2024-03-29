from django.contrib import admin

# Register your models here.
from proposal.models import Proposal, Documentation, Vendor


class ProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'proposal_slug', 'owner', 'status')
    list_filter = ('status', 'owner')
    prepopulated_fields = {"proposal_slug": ("title",)}


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Documentation)
admin.site.register(Vendor)
