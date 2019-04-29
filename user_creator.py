import csv
import requests, json

url = 'localhost:5000/register'
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"}

def readFromFile(filename):	
	with open(filename, 'r') as reader:
		csv_reader = csv.DictReader(reader)
		for row in csv_reader:
			print(row)
			createUser(row)

def createUser(usr):
	url = 'localhost:5000/register'
	header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"}
	usr['username'] = usr['email'].split('@')[0]
	res = requests.post(url, data=usr, headers=headers)
	print(res)

def main():

	readFromFile('students.csv')

if __name__=='__main__':
	main()
