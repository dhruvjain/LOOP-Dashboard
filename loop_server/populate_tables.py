import os
os.environ['DJANGO_SETTINGS_MODULE']='loop_server.settings'
import csv
from dashboard.models import *
import MySQLdb
db = MySQLdb.connect("localhost","dg","password","value_chain")
# Dadanpur : Saran
# Larua : Samastipur
# Banbira : Samastipur
# Rajkarampur : Samastipur : Morwa
# Godiyari : Jamui
month = { 
	"Jan": 1,
	"Feb": 2,
	"Mar": 3,
	"Apr": 4,
	"May": 5,
	"Jun": 6,
	"Jul": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12}


def get_date(date_str):
	items = date_str.split("-")
	date =  "20" + items[2] + "-" + str(month[items[1]]) + "-" + items[0]
	return date

def drop_table(table_name):
    cursor =db.cursor()
    if table_name in 'people_mediator':
    	cursor.execute('delete from people_mediator_assigned_villages;')
    	sql = " ALTER TABLE people_mediator_assigned_villages AUTO_INCREMENT = 1;"
    	cursor.execute(sql)
    
    sql= "delete from %s; " % (table_name);
   
    cursor.execute(sql)
    sql=" ALTER TABLE %s AUTO_INCREMENT = 1;" %(table_name)
    cursor.execute(sql)

    db.commit()

# def get_distinct_villages():
# 	with open('farmers.csv', 'rb') as f:
# 	reader = csv.reader(f)
# 	next(reader)
# 	farmer_village=[]
# 	for row in reader:
# 		if row[0]!='' and row[4]!='':
# 			entry=row[4]
# 			if entry not in farmer_village:
# 				farmer_village.append(entry)
# 	return farmer_village

def fill_country():
	c = Geographies_Country(country_name='India')
	c.save()

def fill_state():
	s = Geographies_State(state_name='Bihar',country_id_id='1')
	s.save()

def fill_district():
	d = Geographies_District(district_name='Samastipur', state_id_id='1')
	d.save()

def fill_block():
	b = Geographies_Block(block_name='Morwa', district_id_id='1')
	b.save()

def fill_village():
	drop_table('geographies_village')
	village_list=['Dadanpur', 'Larua', 'Banbira', 'Mohammadpur', 'Banvira', 'Rajkarampur', 'Godiyari', 'Nikaspur', 'Anandpur']

	for item in village_list:
		entry = Geographies_Village(village_name=item,block_id_id='1')  # each village has block id as morwa
		entry.save()
 
def fill_farmer():
	drop_table('people_farmer')
	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, 'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
	with open('farmers.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader)
		farmer_village=[]
		for row in reader:
			if row[0]!='' and row[4]!='':
				entry=(row[0],row[4])
				if entry not in farmer_village:
					farmer_village.append(entry)
					entry_2 = People_Farmer(name=row[0],gender=row[1],phone=row[2],image_path=row[3],village_id_id=village_name_id[row[4]])
					entry_2.save()

def fill_language():
	drop_table('language')
	entry=Language(language_name='Hindi')
	entry.save()


def fill_People_Mediator():
	drop_table('people_mediator')
	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, 'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
	with open('farmers.csv', 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		vrp_village=[]
		vrp=[]
		for row in reader:
			if row[0]!='' and row[4]!='' and row[6]!='':
				data=(row[4],row[6])
				if data not in vrp_village:
					vrp_village.append(data)
					if row[6] not in vrp:
						vrp.append(row[6])
						entry=People_Mediator(name=row[6],gender='M',image_path='abc',village_id_id=1)
						entry.save()
					ent=People_Mediator.objects.filter(name=row[6])
					ent[0].assigned_villages.add(village_name_id[row[4]])


def fill_Crop():
	drop_table('crop')
	with open('farmers.csv', 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		crop_list=[]
		for row in reader:
			crop=row[5]
			if crop not in crop_list and crop!='':
				crop_list.append(crop)
				entry=Crop(crop_name=crop,measuring_unit='kg',image_path='abc')
				entry.save()

def fill_Mandi():
	drop_table('mandi')
	with open('mandi.csv', 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		mandi_list=[]
		for row in reader:
			if len(row):
				mandi=row[0]
				if mandi not in mandi_list and mandi!='':
					mandi_list.append(mandi)
					entry=Mandi(mandi_name=mandi,district_id_id=1)
					entry.save()



# def fill_Combined_Transaction():
# 	drop_table('combined_transaction')
# 	with open('farmers.csv' , 'rb') as f:
# 		reader=csv.reader(f)
# 		next(reader)
# 		for row in reader:
# 			if len(row)==12:
# 				if row[0] != '' and row[4] != '' and row[6] != '' and row[7] != '':
# 										ent=People_Mediator.objects.get(name=row[6])
# 					med_id=ent.id
# 					ent=People_Farmer.objects.get(name=row[0])
# 					farmer_id=ent[0].id
# 					ent = Crop.objects.get(name=row[5])
# 					crop_id=ent.id
# 					ent = Mandi.objects.get(name=row[7])
# 					mandi_id = ent.id
# 					pay_amount = float(row[11])
# 					pay_status = "Y"
# 					crop_price = float(row[10])
# 					entry = Combined_Transaction(mediator_id=med_id,farmer_id=farmer_id,\
# 						crop_id=crop_id,mandi_id=mandi_id,pay_amount=pay_amount,pay_status=pay_status\
# 						,crop_price=crop_price)
# 					entry.save()
			# ent.id
			# print ent.id

def fill_Farmer_Mediator_Assoc():
	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, \
	'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
	drop_table('farmer_mediator_assoc')
	with open('farmers.csv' , 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		farmer_med =[]
		for row in reader:
			if len(row)==12 and '' not in row:

				_date = get_date(row[8])
				ent=People_Mediator.objects.get(name=row[6])
				med_id=ent.id
				ent = People_Farmer.objects.filter(name=row[0], village_id_id = village_name_id[row[4]])
				_farmer_id=ent[0].id
				data = (_date,med_id,_farmer_id)
				if data not in farmer_med:
					farmer_med.append(data)
					entry = Farmer_Mediator_Assoc(day= _date, farmer_id_id = _farmer_id, mediator_id_id\
						= med_id, pay_status="Y", total_payment = 0)
					entry.save()

				ent=Farmer_Mediator_Assoc.objects.get(day= _date, farmer_id_id = _farmer_id, mediator_id_id = med_id)
				ent.total_payment+=float(row[11])
				ent.save()

def fill_Mediator_pickup():
	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, \
	'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
	drop_table('mediator_pickup')
	with open('farmers.csv' , 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		farmer_med =[]
		for row in reader:
			if len(row)==12 and '' not in row:
				_date = get_date(row[8])
				ent = People_Mediator.objects.get(name=row[6])
				med_id = ent.id
				ent = People_Farmer.objects.filter(name=row[0], village_id_id = village_name_id[row[4]])
				_farmer_id=ent[0].id
				ent=Farmer_Mediator_Assoc.objects.get(day= _date, farmer_id_id = _farmer_id, mediator_id\
						= med_id)
				_pickup_id = ent.id
				ent = Crop.objects.filter(crop_name=row[5])
 				_crop_id=ent[0].id
 				_quantity = float(row[9])
 				entry = Mediator_Pickup(pickup_id_id = _pickup_id, crop_id_id = _crop_id, quantity = _quantity )
 				entry.save()

def fill_Mandi_Transactions():
	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, \
	'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
	drop_table('mandi_transaction')
	with open('farmers.csv' , 'rb') as f:
		reader=csv.reader(f)
		next(reader)
		farmer_med =[]
		for row in reader:
			if len(row)==12 and '' not in row:

				_date = get_date(row[8])
				ent = People_Mediator.objects.get(name=row[6])
				med_id = ent.id
				ent = People_Farmer.objects.filter(name=row[0], village_id_id = village_name_id[row[4]])
				_farmer_id=ent[0].id
				data = (med_id,_farmer_id)

				ent=Farmer_Mediator_Assoc.objects.get(day= _date, farmer_id_id = _farmer_id, mediator_id\
						= med_id)
				_pickup_id = ent.id
				ent = Crop.objects.filter(crop_name=row[5])
 				_crop_id=ent[0].id
 				_quantity = float(row[9])
 				ent = Mediator_Pickup.objects.get(pickup_id_id = _pickup_id, crop_id = _crop_id, quantity = _quantity )
 				_selling_id = ent.id
 				sp = float(row[10])
 				ent = Mandi.objects.get(mandi_name=row[7],district_id_id=1)
 				mandi_id = ent.id

 				entry = Mandi_Transactions(selling_id_id = _pickup_id, selling_price = sp, quantity = _quantity, mandi_id_id = mandi_id  ) 
 				entry.save()

# def fill_Mediator_Purchase():
# 	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, \
# 	'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
# 	drop_table('mediator_purchase')
# 	with open('farmers.csv' , 'rb') as f:
# 		reader=csv.reader(f)
# 		next(reader)
# 		for row in reader:
# 			if len(row)==12:
# 				if row[0] != '' and row[4] != '' and row[6] != '' and row[7] != '' and row[8]!= '':
# 					_date = get_date(row[8])
# 					ent=People_Mediator.objects.get(name=row[6])
# 					med_id=ent.id
# 					ent=People_Farmer.objects.filter(name=row[0], village_id_id = village_name_id[row[4]])
# 					_farmer_id=ent[0].id
# 					ent = Crop.objects.filter(crop_name=row[5])
# 					_crop_id=ent[0].id
# 					print med_id, _farmer_id, _crop_id
# 					entry =  Mediator_Purchase(day= _date, farmer_id_id = _farmer_id, mediator_id_id = med_id\
# 						,crop_id_id = _crop_id)
# 					entry.save()

# def fill_Mediator_Selling():
# 	village_name_id={'Dadanpur':1, 'Larua':2, 'Banbira':3, 'Mohammadpur':4, 'Banvira':5, \
# 	'Rajkarampur':6, 'Godiyari':7, 'Nikaspur':8, 'Anandpur':9}
# 	drop_table('mediator_selling')
# 	with open('farmers.csv' , 'rb') as f:
# 		reader=csv.reader(f)
# 		next(reader)
# 		for row in reader:
# 			if len(row)==12:
# 				if '' in row:
# 					continue
# 				else:
# 				 _date = get_date(row[8])
# 				 ent=People_Farmer.objects.filter(name=row[0], village_id_id = village_name_id[row[4]])
# 				 _farmer_id=ent[0].id
# 				 ent=People_Mediator.objects.get(name=row[6])
# 				 med_id=ent.id
# 				 ent = Crop.objects.filter(crop_name=row[5])
# 				 _crop_id=ent[0].id
# 				 print row[10]
# 				 sp=float(row[10])
# 				 ent=Mandi.objects.get(mandi_name=row[7],district_id_id=1)
# 				 mandi_id = ent.id
# 				 _quantity = float(row[9])
# 				 _payment = float(row[11])
# 				 ent = Mediator_Purchase.objects.filter(day = _date, farmer_id_id =  _farmer_id, \
# 				 mediator_id_id = med_id, crop_id_id = _crop_id )
# 				 selling_id = ent[0].id 
# 				 entry = Mediator_Selling(selling_price = sp, sellings_id = selling_id \
# 				 ,mandi_id_id = mandi_id, quantity = _quantity,  total_payment = _payment  )
# 				 entry.save()


if __name__ == '__main__':
	fill_country()
	fill_state()
	fill_district()
	fill_block()
	fill_village()
	fill_farmer()
	fill_language()
	fill_Crop()
	fill_Mandi()
	fill_People_Mediator()
	
	fill_Farmer_Mediator_Assoc()
	fill_Mediator_pickup()
	fill_Mandi_Transactions()