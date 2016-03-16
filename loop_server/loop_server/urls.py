from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from dashboard.api.resources import CountryResource, StateResource, DistrictResource, BlockResource, \
	VillageResource, VillageNameResource, ShgResource, VOResource, FarmerResource, FarmerNameResource, \
    LanguageResource, MediatorResource, MediatorNameResource, CropResource, MandiResource, \
    MandiNameResource, AssocResource, PickupResource, MandiTrResource, AggregatorResource, \
    ExpenditureResource
from django.contrib import admin

v1_api = Api(api_name = 'v1')
v1_api.register(CountryResource())
v1_api.register(StateResource())
v1_api.register(DistrictResource())
v1_api.register(BlockResource())
v1_api.register(VillageResource())
v1_api.register(VillageNameResource())
v1_api.register(ShgResource())
v1_api.register(VOResource())
v1_api.register(FarmerResource())
v1_api.register(FarmerNameResource())
v1_api.register(LanguageResource())
v1_api.register(MediatorResource())
v1_api.register(MediatorNameResource())
v1_api.register(CropResource())
v1_api.register(MandiResource())
v1_api.register(MandiNameResource())
v1_api.register(AssocResource())
v1_api.register(PickupResource())
v1_api.register(MandiTrResource())
v1_api.register(AggregatorResource())
v1_api.register(ExpenditureResource())

urlpatterns = patterns('',
					   # Examples:
					   # url(r'^$', 'loop_server.views.home', name='home'),
					   # url(r'^blog/', include('blog.urls')),

					   url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
					   url(r'^admin/', include(admin.site.urls)),

					   # Tastypie stuff
					   url(r'^api/', include(v1_api.urls)),
#) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
					   ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()

