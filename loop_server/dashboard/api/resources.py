from functools import partial

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import ModelForm
from django.forms.models import model_to_dict, ModelChoiceField

from tastypie import fields
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse, NotFound
from tastypie.resources import ModelResource

from dashboard.models import Geographies_Country as Country
from dashboard.models import Geographies_State as State
from dashboard.models import Geographies_District as District
from dashboard.models import Geographies_Block as Block
from dashboard.models import Geographies_Village as Village
from dashboard.models import Shg, Language, Crop, Mandi, Aggregator
from dashboard.models import Village_Organization as VO
from dashboard.models import People_Farmer as Farmer
from dashboard.models import People_Mediator as Mediator
from dashboard.models import Farmer_Mediator_Assoc as Assoc
from dashboard.models import Mediator_Pickup as Pickup
from dashboard.models import Mandi_Transactions as MandiTr
from dashboard.models import Mediator_Expenditure as Expenditure

#---------HELP NOTES------------------------------------------#
# TastyPie doesn't instrospect the ToOneField fields
# Therefore, we have to explicitly handle them in TastyPie Resources
# While acquiring data related to a particular resource if you want 
# the foriegn key data along with it, you'll have to pul full=True
# while mentioning ToOneField
#--------------------------------------------------------------#
class CountryResource(ModelResource):
	class Meta:
		queryset = Country.objects.all()
		resource_name = 'country'
		fields = ["country_name"]
		authorization = Authorization()

class StateResource(ModelResource):
	country = fields.ToOneField(CountryResource, attribute='country_id', full=True)
	class Meta:
		queryset = State.objects.all()
		resource_name = 'state'
		fields = ["state_name"]
		authorization = Authorization()

class DistrictResource(ModelResource):
	state = fields.ToOneField(StateResource, 'state_id', full=True)
	class Meta:
		queryset = District.objects.all()
		resource_name = 'district'
		fields = ["district_name"]
		authorization = Authorization()

class BlockResource(ModelResource):
	district = fields.ToOneField(DistrictResource, 'district_id', full=True)
	class Meta:
		queryset = Block.objects.all()
		resource_name = 'block'
		fields = ["block_name"]
		authorization = Authorization()

class VillageResource(ModelResource):
	block = fields.ToOneField(BlockResource, 'block_id', full=True)
	class Meta:
		queryset = Village.objects.all()
		resource_name = 'village'
		authorization = Authorization()

class VillageNameResource(ModelResource):
	class Meta:
		queryset = Village.objects.all()
		resource_name = 'village_name'
		fields = ["village_name"]
		authorization = Authorization()

class ShgResource(ModelResource):
	village = fields.ToOneField(VillageNameResource, 'village_id', full=True)
	class Meta:
		queryset = Shg.objects.all()
		resource_name = 'shg'
		fields = ["shg_name"]
		authorization = Authorization()

class VOResource(ModelResource):
	village = fields.ToOneField(VillageNameResource, 'village_id', full=True)
	class Meta:
		queryset = VO.objects.all()
		resource_name = 'vo'
		fields = ["vo_name"]
		authorization = Authorization()

class FarmerResource(ModelResource):
	village = fields.ToOneField(VillageNameResource, 'village_id', full=True)
	shg = fields.ToOneField(ShgResource, 'shg_id', full=True, null=True)
	vo = fields.ToOneField(VOResource, 'vo_id', full=True, null=True)
	class Meta:
		queryset = Farmer.objects.all()
		resource_name = 'farmer'
		authorization = Authorization()

class FarmerNameResource(ModelResource):
	village = fields.ToOneField(VillageNameResource, 'village_id', full=True)
	class Meta:
		queryset = Farmer.objects.all()
		resource_name = 'farmer_name'
		fields = ["name","gender"]
		authorization = Authorization()

class LanguageResource(ModelResource):
	class Meta:
		queryset = Language.objects.all()
		resource_name = 'language'
		authorization = Authorization()

class MediatorResource(ModelResource):
	village = fields.ToOneField(VillageNameResource, 'village_id', full=True)
	assigned_villages = fields.ToManyField(VillageNameResource, 'assigned_villages', full=True)
	class Meta:
		queryset = Mediator.objects.all()
		resource_name = 'mediator'
		authorization = Authorization()

class MediatorNameResource(ModelResource):
	class Meta:
		queryset = Mediator.objects.all()
		resource_name = 'mediator'
		fields = ["name"]
		authorization = Authorization()

class CropResource(ModelResource):
	class Meta:
		queryset = Crop.objects.all()
		resource_name = 'crop'
		fields = ["crop_name", "measuring_unit"]
		authorization = Authorization()

class MandiResource(ModelResource):
	district = fields.ToOneField(DistrictResource, 'district_id', full=True)
	class Meta:
		queryset = Mandi.objects.all()
		resource_name = 'mandi'
		authorization = Authorization()

class MandiNameResource(ModelResource):
	class Meta:
		queryset = Mandi.objects.all()
		resource_name = 'mandi'
		fields = ["mandi_name"]
		authorization = Authorization()

class AssocResource(ModelResource):
	farmer = fields.ToOneField(FarmerNameResource, 'farmer_id', full=True)
	mediator = fields.ToOneField(MediatorNameResource, 'mediator_id', full=True)
	class Meta:
		queryset = Assoc.objects.all().order_by('day')
		resource_name = 'assoc'
		authorization = Authorization()
		excludes = ["pay_status"]
		filtering = {
			'day' : ALL
		}

class PickupResource(ModelResource):
	pickup = fields.ToOneField(AssocResource, 'pickup_id', full=True)
	crop = fields.ToOneField(CropResource, 'crop_id', full=True)
	class Meta:
		queryset = Pickup.objects.all()
		resource_name = 'pickup'
		authorization = Authorization()
		filtering = {
			'pickup' : ALL_WITH_RELATIONS
		}

class MandiTrResource(ModelResource):
	mandi = fields.ToOneField(MandiNameResource, 'mandi_id', full=True)
	selling = fields.ToOneField(PickupResource, 'selling_id', full=True)
	class Meta:
		queryset = MandiTr.objects.all()
		resource_name = 'manditr'
		authorization = Authorization()
		filtering = {
			'selling' : ALL_WITH_RELATIONS
		}

class AggregatorResource(ModelResource):
	class Meta:
		queryset = Aggregator.objects.all()
		resource_name = 'aggregator'
		authorization = Authorization()

class ExpenditureResource(ModelResource):
	mediator = fields.ToOneField(MediatorResource, 'mediator_id', full=True)
	class Meta:
		queryset = Expenditure.objects.all()
		resource_name = 'expenditure'
		authorization = Authorization()


