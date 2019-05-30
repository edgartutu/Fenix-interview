import mysql.connector
import datetime

db = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="hris",
	  database="fenix_staff"
	)

mysql = db.cursor()

def addEmployee() :
	employee_id = int(input("Enter employee id: "))
	st_date = input("Enter date(yyyy/mm/dd): ")
	seniority = input("Enter seniority: ")

	date = st_date.split("/")
	start_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
	db_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
	seniority = seniority.upper()

	mysql.execute("INSERT INTO fenix_employees (employee_id, start_date, seniority) VALUES (%s, %s, %s)", (employee_id, db_date, seniority))
	db.commit()
	print("\n\n")

def accessBenefit() :
	total_points = 0
	user_id = int(input("Enter employee id: "))
	#mysql = db.cursor()
	mysql.execute("SELECT employee_id FROM fenix_employees")
	result = mysql.fetchall()
	user = False
	
	for x in result:
		if user_id in result :
			user = True

	if True:
		benefit = 0
		while benefit != 3 :
			print("1. Check balance")
			print("2. Redeem Benefit")
			print("3. Exit")
			benefit = int(input())

			if benefit == 1 :
				total_points = checkBalance(user_id)
				print('Available points ', total_points)
				print("\n\n")
			elif benefit == 2 :
				total_points = checkBalance(user_id)
				print('Available points ', total_points)
				redeem = int(input("Redeem points: "))
				manager = int(input("Enter Supervisor ID: "))
				if redeem <= total_points :
					mysql.execute("INSERT INTO fenix_redeemed_points (redeem, employee_id, manager_id, approved) VALUES (%s, %s, %s, %s)", (redeem, user_id, manager, 0))
					db.commit()
					print("Requested")
					print("\n\n")
				else:
					print("Requested points less than available points")
					print("\n\n")

			elif benefit == 3 :
				break
			else :
				continue
	else :
		print("User does not exist")
		print("\n\n")
	

def checkBalance(employee_id) :
	points = 0
	#mysql = db.cursor()
	mysql.execute("SELECT start_date, seniority FROM fenix_employees WHERE employee_id = %s ORDER BY start_date ASC", (employee_id, ))
	result = mysql.fetchall()

	previous_date = None
	months = 0
	years = 0.0
	seniority = None
	count = 0
	start_date = None

	for x in result :
		count = count + 1
		#print(seniority)

		if count == 1 :
			start_date = x[0]

		if count == len(result) :
			if not previous_date is None :
				r = x[0] - previous_date
				_months = r.days // 30

				calculate_points = benefitCalculator(_months, None, seniority)
				points = points + calculate_points
			r = datetime.datetime.now() - x[0]
			_months = r.days // 30
			calculate_points = benefitCalculator(_months, None, seniority)
			points = points + calculate_points

			r = datetime.datetime.now() - start_date
			_years = r.days / 365
			_list = [_years, points]

			points = benefitCalculator(None, _list, None)
			
		else :
			if x[0] is None:
				print('Date is null')
				continue
			else :
				if not previous_date is None:
					r = x[0] - previous_date

					_months = r.days // 30
					calculate_points = benefitCalculator(_months, None, seniority)
					points = points + calculate_points

		previous_date = x[0]
		seniority = x[1]

	mysql.execute("SELECT redeem FROM fenix_redeemed_points WHERE employee_id = %s AND approved = %s", (employee_id, 1),)
	result = mysql.fetchall()

	if len(result) == 0 :
		return points
	else :
		redeemed = 0
		for x in result :
			redeemed = redeemed + x[0]

		return points - redeemed



def benefitCalculator(months, years,seniority):
	if seniority == "A" :
		return months * 5
	elif seniority == "B" :
		return months * 10
	elif seniority == "C" :
		return months * 15
	elif seniority == "D" :
		return months * 20
	elif seniority == "E" :
		return months * 25 

	if not years is None:
		points = years[1]
		if years[0] <= 2.0 :
			return points * 1
		elif years[0] <=4.0 :
			return points * 1.25
		elif years[0] > 4 :
			return points * 1.5

def approveBenefit():
	_id = int(input("Enter employee id: "))
	#mysql = db.cursor()
	mysql.execute("SELECT employee_id FROM fenix_employees")
	result = mysql.fetchall()
	employee = False
	for x in result:
		if _id in x:
			employee = True

	if employee :
		mysql.execute("SELECT id, employee_id, redeem FROM fenix_redeemed_points WHERE manager_id = %s AND approved = %s", (_id, 0),)

		result = mysql.fetchall()

		if len(result) > 0:
			count = 1
			_dict = dict()
			for x in result:
				print(str(x[0]) + ". Employee " + str(x[1]) + " wants to redeem " + str(x[2]) + " points")
				_dict[str(x[0])] = x[0]
				if count == len(result):
					print("Select redeem number to redeem points: ")

				count = count + 1

			approve = input()
			if approve in _dict :
				mysql.execute("UPDATE fenix_redeemed_points SET approved = 1 WHERE id = %s", (int(approve), ))
				db.commit()

		else :
			print("Not requests for points to be redeemed")
			print("\n\n")
	else :
		print("User Id does not exist")
		print("\n\n")


num = 0

while num != 4:

	print("1. Enter Employee")
	print("2. Employee Benefit Access")
	print("3. Benefit Approval")
	print("4. Exit")

	num = int(input("Select number (between 1 to 4): "))

	if not (num >= 1 and num <=4) :
		continue
	else :
		if num == 1 :
			addEmployee()
		elif num == 2 :
			accessBenefit()
		elif num == 3 :
			pass
			approveBenefit()
		elif num == 4 :
			mysql.close()
			exit()

