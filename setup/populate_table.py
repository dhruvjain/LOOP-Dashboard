import csv
import MySQLdb

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

db = MySQLdb.connect("localhost","dg","password","value_chain")


def get_date(date_str):
	items = date_str.split("-")
	date =  "20" + items[2] + "-" + str(month[items[1]]) + "-" + items[0]
	return date

def main():
	cursor = db.cursor()

	with open('aggregator_pilot_data.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		head_row = next(reader)
		count = 0
		for row in reader:
			if not row[0] or not row[8]:
				continue

			row[0] = get_date(row[0])
			if row[7] == 'Y' or row[7] == 'y':
				row[7] = '1'
			elif row[7] == 'N' or row[7] == 'n':
				row[7] = '0'
			else:
				row[7] = 'NULL'
			del row[3]
			row = tuple(row)
			# print row
			sql = """INSERT INTO farmer_transaction 
				(day, village, farmer, crop, qunatity, unit, paid, member_rate, total_payment, market, vrp)
				VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s')""" % row
			print sql
			cursor.execute(sql)
			db.commit()
			count += 1
			 
		print count

def fill_geographies_country():
	cursor = db.cursor()
	c_name='Afghanistan'
	sql="""INSERT INTO geographies_country (country_name) VALUES ('%s')""" %c_name 
	print sql
	cursor.execute(sql)
	db.commit()

def fill_geographies_state():
	cursor = db.cursor()
	state_name='Bihar'
	sql="""INSERT INTO geographies_state (`state_name`,`country_id_id`) VALUES ('%s', '%s')""" %(state_name,'1')
	cursor.execute(sql)
	db.commit() 

if __name__ == '__main__':
	fill_geographies_state()