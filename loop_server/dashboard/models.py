from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Geographies_Country(models.Model):
	id = models.AutoField(primary_key=True)
	country_name = models.CharField(max_length=50)
	
	class Meta:
		db_table = 'geographies_country'
	
	def __unicode__(self):
		return self.country_name

class Geographies_State(models.Model):
	id = models.AutoField(primary_key=True)
	state_name = models.CharField(max_length=50)
	country_id = models.OneToOneField(Geographies_Country)

	class Meta:
		db_table = 'geographies_state'

	def __unicode__(self):
		return self.state_name

class Geographies_District(models.Model):
	id = models.AutoField(primary_key=True)
	district_name = models.CharField(max_length=50)
	state_id = models.ForeignKey(Geographies_State)
	
	class Meta:
		db_table = 'geographies_district'
		
	def __unicode__(self):
		return self.district_name

class Geographies_Block(models.Model):
	id = models.AutoField(primary_key=True)
	block_name = models.CharField(max_length=50)
	district_id = models.ForeignKey(Geographies_District)
	
	class Meta:
		db_table = 'geographies_block'

	def __unicode__(self):
		return self.block_name

class Geographies_Village(models.Model):
	id = models.AutoField(primary_key=True)
	village_name = models.CharField(max_length=50)
	latitude = models.FloatField(null=True)
	longitude = models.FloatField(null=True)
	block_id = models.ForeignKey(Geographies_Block, null=True, blank=True)
	
	class Meta:
		db_table = 'geographies_village'
	
	def __unicode__(self):
		return self.village_name

class Shg(models.Model):
	id = models.AutoField(primary_key=True)
	shg_name = models.CharField(max_length=50)
	village_id = models.ForeignKey(Geographies_Village)
	
	class Meta:
		db_table = 'shg'

	def __unicode__(self):
		return self.shg_name

class Village_Organization(models.Model):
	id = models.AutoField(primary_key=True)
	vo_name = models.CharField(max_length=50)
	village_id = models.ForeignKey(Geographies_Village)

	class Meta:
		db_table = 'village_organization'

	def __unicode__(self):
		return self.vo_name

class People_Farmer(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=1)		# M/F
	phone = models.CharField(max_length=13)
	image_path = models.CharField(max_length=100)
	village_id = models.ForeignKey(Geographies_Village)
	shg_id = models.ForeignKey(Shg, null=True, blank=True)
	vo_id = models.ForeignKey(Village_Organization, null=True, blank=True)

	class Meta:
		db_table = 'people_farmer'

	def __unicode__(self):
		return self.name;

class Language(models.Model):
	id = models.AutoField(primary_key=True)
	language_name = models.CharField(max_length=50)
	
	class Meta:
		db_table = 'language'
	
	def __unicode__(self):
		return self.language_name

class People_Mediator(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=1)
	phone = models.CharField(max_length=13, null=True)
	image_path = models.CharField(max_length=100)
	village_id = models.ForeignKey(Geographies_Village)
	preferred_lang = models.ForeignKey(Language, null=True, blank=True)
	assigned_villages = models.ManyToManyField(Geographies_Village, related_name='assigned_villages')
	class Meta:
		db_table = 'people_mediator'

	def __unicode__(self):
		return self.name;

class Crop(models.Model):
	id = models.AutoField(primary_key=True)
	crop_name = models.CharField(max_length=30)
	measuring_unit = models.CharField(max_length=20)
	image_path = models.CharField(max_length=100)
	
	class Meta:
		db_table = 'crop'
	
	def __unicode__(self):
		return self.crop_name

class Mandi(models.Model):
	id = models.AutoField(primary_key=True)
	mandi_name = models.CharField(max_length=90)
	latitude = models.FloatField(null=True)
	longitude =  models.FloatField(null=True)
	district_id = models.ForeignKey(Geographies_District)
	
	class Meta:
		db_table = 'mandi'
	
	def __unicode__(self):
		return self.mandi_name

class Farmer_Mediator_Assoc(models.Model):
	id = models.AutoField(primary_key=True)
	day = models.DateField()
	farmer_id = models.ForeignKey(People_Farmer)
	mediator_id = models.ForeignKey(People_Mediator)
	pay_status = models.CharField(max_length=1)
	total_payment = models.FloatField()

	class Meta:	
		db_table =  'farmer_mediator_assoc'

class Mediator_Pickup(models.Model):
	id = models.AutoField(primary_key=True)
	pickup_id = models.ForeignKey(Farmer_Mediator_Assoc)
	crop_id = models.ForeignKey(Crop)
	quantity = models.FloatField()

	class Meta():
		db_table = 'mediator_pickup'
			
class Mandi_Transactions(models.Model):
	id = models.AutoField(primary_key=True)
	selling_id = models.ForeignKey(Mediator_Pickup)
	selling_price = models.FloatField()	
	quantity = models.FloatField()
	mandi_id = models.ForeignKey(Mandi)

	class Meta:
		db_table = 'mandi_transaction'

class Aggregator(models.Model):
	id = models.AutoField(primary_key=True)
	day = models.DateField()
	crop_id = models.ForeignKey(Crop)
	mandi_id = models.ForeignKey(Mandi)
	quantity = models.FloatField()
	selling_price = models.FloatField()

	class Meta:
		db_table = 'aggregator'


# class Mediator_Purchase(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	day = models.DateField()
# 	farmer_id = models.ForeignKey(People_Farmer)
# 	mediator_id = models.ForeignKey(People_Mediator)
# 	crop_id = models.ForeignKey(Crop)

# 	class Meta:
# 		db_table =  'mediator_purchase'

# class Mediator_Selling(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	selling_price = models.FloatField()
# 	selling_id = models.ForeignKey(Mediator_Purchase)
# 	mandi_id = models.ForeignKey(Mandi)
# 	quantity = models.FloatField()
# 	total_payment = models.FloatField()

# 	class Meta:
# 		db_table =  'mediator_selling'
		
class Mediator_Expenditure(models.Model):
	id = models.AutoField(primary_key=True)
	day = models.DateField()
	mediator_id = models.ForeignKey(People_Mediator)
	vrp_fees = models.FloatField()
	transport_cost = models.FloatField()
	other_cost = models.FloatField(null=True)

	class Meta:
		db_table = 'mediator_expenditure'


# class Day_Transaction(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	transaction_date = models.DateField()
# 	mediator_id = models.ForeignKey(People_Mediator)
# 	transport_cost = models.FloatField()
# 	other_cost = models.FloatField(null=True)
# 	vrp_fees = models.FloatField()
# 	comment = models.CharField(max_length=50, null=True, blank=True)
	
# 	class Meta:
# 		db_table = 'day_transaction'

# class Village_Transaction(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	transaction_date = models.DateField()
# 	entry_time = models.DateTimeField()
# 	village_id = models.ForeignKey(Geographies_Village)
# 	mediator_id = models.ForeignKey(People_Mediator)
# 	farmer_id = models.ForeignKey(People_Farmer)
# 	crop_id = models.ForeignKey(Crop)
# 	quantity = models.PositiveIntegerField()
# 	payment_amount = models.FloatField()
# 	payment_status = models.CharField(max_length=1) # Y/N
# 	day_transaction_id = models.ForeignKey(Day_Transaction)
	
# 	class Meta:
# 		db_table = 'village_transaction'

# class Mandi_Transaction(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	transaction_date = models.DateField()
# 	entry_time =  models.DateTimeField()
# 	mandi_id = models.ForeignKey(Mandi)
# 	mediator_id = models.ForeignKey(People_Mediator)
# 	crop_id = models.ForeignKey(Crop)
# 	quantity_sold = models.FloatField()
# 	total_amount = models.FloatField()
# 	day_transaction_id = models.ForeignKey(Day_Transaction)

# 	class Meta:
# 		db_table = 'mandi_transaction'

# class Combined_Transaction(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	mediator_id = models.ForeignKey(People_Mediator)
# 	farmer_id = models.ForeignKey(People_Farmer)
# 	crop_id = models.ForeignKey(Crop)
# 	mandi_id = models.ForeignKey(Mandi)
# 	# quality = models.FloatField()
# 	pay_amount = models.FloatField()
# 	pay_status = models.CharField(max_length=1)
# 	crop_price = models.FloatField()

# 	class Meta:
# 		db_table = 'combined_transaction'

