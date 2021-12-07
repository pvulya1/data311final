import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

host = 'localhost'
user = 'root'
passwd = '1Chas234.'
database = 'it_company'

def connect_db(host, user, passwd, database = None):
    db = None
    
    try:
        db = mysql.connector.connect(
    
        host = host,
        user = user,
        passwd = passwd,
        database = database
    
        )
        print('Connection succsessfull')
    except Error as err:
        print(f'Error: {err}')
    
    return db

def create_db(connection, query):
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        print('DB created successfully')
    except Error as err:
        print(f'Error: {err}')

#establishing connection with the server
connection = connect_db(host, user, passwd)

#creating 'it_company' db
db_name = 'it_company'
create_db(connection, f'CREATE DATABASE {db_name}')

#reconnecting to the server + to the database created above
connection = connect_db(host, user, passwd, db_name)

#creating a 'cursor' to further manipulations with our db_name
mycursor = connection.cursor()

#creating 'Department' table
mycursor.execute(''' CREATE TABLE `Department` (
  `DepID` int PRIMARY KEY AUTO_INCREMENT,
  `Department_Name` varchar(50),
  `Department_location` varchar(50)
); ''')

connection.commit()

#creating our 'Projects' table
mycursor.execute(''' CREATE TABLE `Projects` (
  `ProjectID` int PRIMARY KEY AUTO_INCREMENT,
  `Duration` int,
  `Name` varchar(50),
  `DepID` int,
  FOREIGN KEY (`DepID`) REFERENCES `Department`(`DepID`)
); ''')  

connection.commit()

#creating 'Employee' table
mycursor.execute(''' CREATE TABLE `Employee` (
  `EmployeeID` int PRIMARY KEY AUTO_INCREMENT,
  `First_Name` varchar(50),
  `Last_Name` varchar(50),
  `Age` int,
  `DepID` int,
  `Job_Title` varchar(50),
  `Salary` decimal(15,2),
  `ProjectID` int,
  FOREIGN KEY (`DepID`) REFERENCES `Department`(`DepID`),
  FOREIGN KEY (`ProjectID`) REFERENCES `Projects`(`ProjectID`)
); ''')

connection.commit()

#inserting values into 'Department' table
sql_query_department = "INSERT INTO `Department` (`Department_Name`, `Department_location`) VALUES (%s, %s)"
                        
values_department = [
    ('HR', 'Calgary'),
    ('Marketing', 'Calgary'),
    ('Server & Security', 'Edmonton'),
    ('Development', 'Edmonton'),
    ('Media & Communication', 'Calgary'),
    ('Business Development', 'Calgary')
    ]

mycursor.executemany(sql_query_department, values_department)

connection.commit()

#inserting values into 'Projects' table
sql_query_projects = "INSERT INTO `Projects` (`Duration`, `Name`, `DepID`) VALUES (%s, %s, %s)"

values_projects = [
    ('5', 'DBMS testing', '4'),
    ('25', 'Back-end developers recruitment', '1'),
    ('15', 'VPN issues troubleshooting', '3'),
    ('30', 'Attracting new investors', '6'),
    ('10', 'Finish up official website', '2'),
    ('5', 'Scheduling CBC News interview with CEO', '5')
]

mycursor.executemany(sql_query_projects, values_projects)

connection.commit()

#insetring values into 'Employee' table
sql_query_employee = """ INSERT INTO `Employee` (`First_Name`, `Last_Name`, `Age`, `DepID`, `Job_Title`, `Salary`, `ProjectID`) VALUES (%s, %s, %s, %s, %s, %s, %s) """

values_employee = [
    ('Eugene', 'Paulia', '20', '4', 'Python developer', '115250.50', '1'),
    ('Rusaln', 'Muratov', '22', '4', 'Python developer', '115300.25', '1'),
    ('Jack', 'Barlowe', '25', '1', 'HR recruiter', '78000.50', '2'),
    ('Mary', 'Elrod', '30', '6', 'Business development specialist', '83000.35', '4'),
    ('Kevin', 'Caddel', '45', '2', 'Creative director', '95000.00', '5'),
    ('Patty', 'Hart', '23', '1', 'HR recruiter', '68000.00', '2'),
    ('Aida', 'Bugg', '37', '6', 'Business development specialist', '97560.67', '4'),
    ('Olive', 'Yew', '41', '3', 'IT support technician', '95300.50', '3'),
    ('Allie', 'Grater', '27', '2', 'Content marketing specialist', '78900.00', '5'),
    ('Peg', 'Legge', '33', '5', 'Communication specialist', '88000.60', '6'),
    ('Teri', 'Dactyl', '29', '4', 'Data engineer', '105000.70', '1'),
    ('Paddy', 'O\'Furniture', '22', '6', 'Business development representative', '55000.00', '4')
]

mycursor.executemany(sql_query_employee, values_employee)

connection.commit()

#Question 1: What is the average age of all employees in the company?
sql_query1 = "SELECT AVG(`Age`) FROM `Employee`;"

mycursor.execute(sql_query1)
 
print(f'Average age of the company\'s employees is {mycursor.fetchone()[0]}')

#Question 2: How many people work in each department?
sql_query2 = """ SELECT COUNT(DISTINCT employee.EmployeeID ) AS `Amount of employees`, department.Department_Name
FROM employee
INNER JOIN department ON department.DepID = employee.DepID 	
GROUP BY department.DepID """

mycursor.execute(sql_query2)

temp_arr = mycursor.fetchall()

q2_df = []

for el in temp_arr:
    q2_df.append(list(el))

#printing a resulting query as a data frame
col_names = ['Num of employees', 'Department']
q2_df = pd.DataFrame(q2_df, columns = col_names)
print(q2_df)

#Creating explode data
explode = (0.1, 0.0, 0.2, 0.3, 0.0, 0.0)

#Creating color parameters
colors = ("beige", "orange", "cyan", "brown", "grey", "indigo")

#Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "green" }

#Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%".format(pct, absolute)

#Creating a pie chart
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(q2_df['Num of employees'],
                                  autopct = lambda pct: func(pct, q2_df['Num of employees']),
                                  explode = explode,
                                  labels = q2_df['Department'],
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))

#Adding legend
ax.legend(wedges, cars,
          title ="Departments",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))
 
plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Question 2\nPrecentage of all employees per every Department")
#show plot
plt.show()

#Question 3: Who has the max Salary and the min Salary?

#Query for Min Salary
sql_query3 = """ SELECT Salary, First_Name, Last_Name
FROM employee 
WHERE (Salary) IN (select MIN(Salary) FROM employee)  """

#Query for Max Salary
sql_query4 = """ SELECT Salary, First_Name, Last_Name
FROM employee 
WHERE (Salary) IN (select MAX(Salary) FROM employee)  """

mycursor.execute(sql_query3)

min_salary = mycursor.fetchone()

print(f'{min_salary[1]} {min_salary[2]} has the min Salary of {min_salary[0]}')

mycursor.execute(sql_query4)

max_salary = mycursor.fetchone()

print(f'{max_salary[1]} {max_salary[2]} has the max Salary of {max_salary[0]}')

#Question 4: