import csv

if __name__ == '__main__':
	with open('farmers.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader)
		farmer_village=[]
		for row in reader:
			if row[0]!='' and row[4]!='':
				entry=row[4]
				if entry not in farmer_village:
					farmer_village.append(entry)
	print farmer_village
