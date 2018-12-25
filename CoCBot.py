import json
import requests
import traceback

url = #INSERT_CURRENT_WAR_URL_HERE
api_key = #INSERT_API_HERE

headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + api_key}
r = requests.get(url, headers = headers)

data = r.json()
teamSize = data['teamSize']
opponentClan = data['opponent']['name']
clanName = #INSERT_CLAN_NAME_HERE
stats = {}
defenses = {}

for i in range(teamSize):
	name = data['clan']['members'][i]['name'] #store clan member name in str
	thLevel = data['clan']['members'][i]['townhallLevel']
	stats.setdefault(name, []).append(thLevel)
	if 'attacks' in data['clan']['members'][i]:
		length = len(data['clan']['members'][i]['attacks']) #number of attacks done
		if length == 2:
			for j in range(length):
				defenderTag = data['clan']['members'][i]['attacks'][j]['defenderTag']
				for k in range(teamSize - 1):
					if defenderTag == data['opponent']['members'][k]['tag']:
						defenderTH = data['opponent']['members'][k]['townhallLevel']
				stats.setdefault(name, []).append(data['clan']['members'][i]['attacks'][j]['stars']) #add stars to stats
				stats.setdefault(name, []).append(defenderTH)
		else:
			defenderTag = data['clan']['members'][i]['attacks'][0]['defenderTag']
			for k in range(teamSize - 1):
				if defenderTag == data['opponent']['members'][k]['tag']:
					defenderTH = data['opponent']['members'][k]['townhallLevel']
			stats.setdefault(name, []).append(data['clan']['members'][i]['attacks'][0]['stars'])
			stats.setdefault(name, []).append(defenderTH)
			stats.setdefault(name, []).append(0)
			stats.setdefault(name, []).append(0)
	else:
		stats.setdefault(name, []).append(0)
		stats.setdefault(name, []).append(0)
	defenses[name] = data['clan']['members'][i]['opponentAttacks']

players_main = list(stats.keys())
for i in range(len(stats)):
	stats[players_main[i]][0] = int (stats[players_main[i]][0]) 
stats = dict(sorted(stats.items(), key = lambda e: e[1][0], reverse = True))
for i in range(len(stats)):
	stats[players_main[i]][0] = str (stats[players_main[i]][0])

#print (stats)
import csv

def writeData(stats, opponentClan, clanName, teamSize):
	with open(#INSERT_CSV_PATH, 'a+', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		keys = list(stats.keys())
		i = 0
		statement = clanName + " Vs " + opponentClan + ", War Size: " + str(teamSize)
		writer.writerows([[statement]])
		field = ["Player Name", "Player TH", "A1", "Against TH", "A2", "Against TH", "Defenses"]
		writer.writerows([field])

		for k in range(0,teamSize):
			name = keys[i].encode('utf-8', 'ignore') #storing name as string
			if b"Throck" in name:
				name_actual = "Throck"
			elif b"Pain Train" in name:
				name_actual = "Pain Train"
			elif "Đại Ca Bú Dú Da".encode('utf-8') in name:
				name_actual = "Dai Ca Bu Du Da"
			else:
				name_actual = name.decode('utf-8')
				#try: 
				#	name_actual = name.decode('utf-8')
				#except TypeError:
				#	traceback.print_exc()
				#finally:
				#	name_actual = keys[i].encode('utf-8', 'ignore')
			stats_row = stats[keys[i]] #storing stars of name as list
			defensenum = str(defenses[keys[i]]) #storing defenses as string
			writer.writerows([[name_actual] + [str(stats_row[0])] + [str(stats_row[1])] + [str(stats_row[2])] + [str(stats_row[3])] + [str(stats_row[4])] + [defensenum]])
			if i < teamSize-1:
				i = i + 1
			else:
				break

def retrieveData():
	#load file
	with open(#INSERT_STATS_CSV_PATH_HERE, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		#iterating csv and storing unique names in a set
		data = set([])
		for row in reader:
			#discard Player Name and Reddit Echo values
			full_name = None
			if row[0] == "Player Name":
				full_name = row[0]
			if "Reddit Echo" in row[0]:
				full_name = row[0]
			data.add(row[0])
			data.discard(str(full_name))
		#data dict based on set (maybe use numpy if dimensions of list get too big)
		data_dict = {}
		for i in range(len(data)):
			elem = data.pop()
			data_dict.setdefault(elem, [])
		#reader pointer back to row 0
		csvfile.seek(0)
		#storing dict_keys in keys var
		keys = list(data_dict.keys())
		#iterating over 20 keys over n rows
		for i in range(len(keys)):
			for row in reader:
				if keys[i] in row[0]:
					for j in range(1,7):
						data_dict.setdefault(keys[i], []).append(row[j]) #the making of vector
			csvfile.seek(0) #pointer back to zero for next i
		analyseData(data_dict)
		#TO-DO: Conversion to data_dict to appropriate measures. Create new function. Print CSV to new analysis file.

def analyseData(data_dict):
	#to be changed
	players = list(data_dict.keys())
	for i in range(len(data_dict)):
		data_dict[players[i]][0] = int (data_dict[players[i]][0]) 
	data_dict = dict(sorted(data_dict.items(), key = lambda e: e[1][0], reverse = True))
	for i in range(len(data_dict)):
		data_dict[players[i]][0] = str (data_dict[players[i]][0])
	#print(type(data_dict))
	#print(data_dict)
	players = list(data_dict.keys())
	stats_dict = {}
	stats_dict_3 = {}
	for i in range(len(players)):
		stats_dict.setdefault(players[i], ['','','','','','','','','',''])
		stats_dict_3.setdefault(players[i], ['','','','','','','','','',''])

	for i in range(len(players)):
		playerTH = data_dict[players[i]][0]
		stats_dict[players[i]][0] = playerTH
		stats_dict_3[players[i]][0] = playerTH
		player_list_len = len(data_dict[players[i]])
		stars_3_11 = 0
		stars_3_10 = 0
		stars_3_9 = 0
		stars_11 = 0
		stars_10 = 0
		stars_9 = 0
		counter_11 = 0
		counter_10 = 0
		counter_9 = 0
		counter_3_11 = 0
		counter_3_10 = 0
		counter_3_9 = 0
		if playerTH == '11':
			for j in range(4, 10): 
				stats_dict[players[i]][j] = 'NA'
				stats_dict_3[players[i]][j] = 'NA'
			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '11':
					star = int(data_dict[players[i]][j-1])
					stars_11 += star
					counter_11 += 1
					if star == 3:
						stars_3_11 += star
						counter_3_11 += 1
				elif data_dict[players[i]][j] == '10':
					star = int(data_dict[players[i]][j-1])
					stars_10 += star
					counter_10 += 1
					if star == 3:
						stars_3_10 += star
						counter_3_10 += 1
				elif data_dict[players[i]][j] == '9':
					star = int(data_dict[players[i]][j-1])
					stars_9 += star
					counter_9 += 1
					if star == 3:
						stars_3_9 += star
						counter_3_9 += 1
				if flag == 0:
					j +=2
					flag = 1
				elif flag == 1:
					j += 4
					flag = 0
			if counter_11 != 0:
				stats_dict[players[i]][1] = round((((stars_11)/(counter_11))/3)*100, 2)
			else:
				stats_dict[players[i]][1] = '0'
			if counter_3_11 != 0:
				stats_dict_3[players[i]][1] = round((((stars_3_11)/(counter_11))/3)*100, 2)
			else:
				stats_dict_3[players[i]][1] = '0'
			if counter_10 != 0:
				stats_dict[players[i]][2] = round((((stars_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict[players[i]][2] = '0'
			if counter_3_10 != 0:
				stats_dict_3[players[i]][2] = round((((stars_3_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict_3[players[i]][2] = '0'
			if counter_9 != 0:
				stats_dict[players[i]][3] = round((((stars_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict[players[i]][3] = '0'
			if counter_3_9 != 0:
				stats_dict_3[players[i]][3] = round((((stars_3_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict_3[players[i]][3] = '0'
		elif playerTH == '10':
			for j in range(1, 4): 
				stats_dict[players[i]][j] = 'NA'
				stats_dict_3[players[i]][j] = 'NA'
			for j in range(7, 10): 
				stats_dict[players[i]][j] = 'NA'
				stats_dict_3[players[i]][j] = 'NA'
			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '11':
					star = int(data_dict[players[i]][j-1])
					stars_11 += star
					counter_11 += 1
					if star == 3:
						stars_3_11 += star
						counter_3_11 += 1
				elif data_dict[players[i]][j] == '10':
					star = int(data_dict[players[i]][j-1])
					stars_10 += star
					counter_10 += 1
					if star == 3:
						stars_3_10 += star
						counter_3_10 += 1
				elif data_dict[players[i]][j] == '9':
					star = int(data_dict[players[i]][j-1])
					stars_9 += star
					counter_9 += 1
					if star == 3:
						stars_3_9 += star
						counter_3_9 += 1
				if flag == 0:
					j +=2
					flag = 1
					continue
				if flag == 1:
					j += 4
					flag = 0
					continue
			if counter_11 != 0:
				stats_dict[players[i]][4] = round((((stars_11)/(counter_11))/3)*100, 2)				
			else:
				stats_dict[players[i]][4] = '0'				
			if counter_3_11 != 0:
				stats_dict_3[players[i]][4] = round((((stars_3_11)/(counter_11))/3)*100, 2)
			else:
				stats_dict_3[players[i]][4] = '0'
			if counter_10 != 0:
				stats_dict[players[i]][5] = round((((stars_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict[players[i]][5] = '0'				
			if counter_3_10 != 0:
				stats_dict_3[players[i]][5] = round((((stars_3_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict_3[players[i]][5] = '0'
			if counter_9 != 0:
				stats_dict[players[i]][6] = round((((stars_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict[players[i]][6] = '0'				
			if counter_3_9 != 0:				
				stats_dict_3[players[i]][6] = round((((stars_3_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict_3[players[i]][6] = '0'
		elif playerTH == '9':
			for j in range(1, 7): 
				stats_dict[players[i]][j] = 'NA'
				stats_dict_3[players[i]][j] = 'NA'
			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '11':
					star = int(data_dict[players[i]][j-1])
					stars_11 += star
					counter_11 += 1
					if star == 3:
						stars_3_11 += star
						counter_3_11 += 1
				elif data_dict[players[i]][j] == '10':
					star = int(data_dict[players[i]][j-1])
					stars_10 += star
					counter_10 += 1
					if star == 3:
						stars_3_10 += star
						counter_3_10 += 1
				elif data_dict[players[i]][j] == '9':
					star = int(data_dict[players[i]][j-1])
					stars_9 += star
					counter_9 += 1
					if star == 3:
						stars_3_9 += star
						counter_3_9 += 1
				if flag == 0:
					j +=2
					flag = 1
					continue
				if flag == 1:
					j += 4
					flag = 0
					continue
			if counter_11 != 0:
				stats_dict[players[i]][7] = round((((stars_11)/(counter_11))/3)*100, 2)
			else:
				stats_dict[players[i]][7] = '0'				
			if counter_3_11 != 0:
				stats_dict_3[players[i]][7] = round((((stars_3_11)/(counter_11))/3)*100, 2)
			else:
				stats_dict_3[players[i]][7] = '0'
			if counter_10 != 0:
				stats_dict[players[i]][8] = round((((stars_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict[players[i]][8] = '0'
			if counter_3_10 != 0:
				stats_dict_3[players[i]][8] = round((((stars_3_10)/(counter_10))/3)*100, 2)
			else:
				stats_dict_3[players[i]][8] = '0'
			if counter_9 != 0:
				stats_dict[players[i]][9] = round((((stars_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict[players[i]][9] = '0'
			if counter_3_9 != 0:
				stats_dict_3[players[i]][9] = round((((stars_3_9)/(counter_9))/3)*100, 2)
			else:
				stats_dict_3[players[i]][9] = '0'
		#print("Player: "+ players[i] + " Stars: "+ str(stars_11) + " Counter: " + str(counter_11))
		#print("\t"+ " Stars: "+ str(stars_10) + " Counter: " + str(counter_10))
		#print("\t" + " Stars: "+ str(stars_9) + " Counter: " + str(counter_9))
	#print(stats_dict)
	#print(len(stats_dict))
	with open(#INSERT_ANALYSIS_CSV_HERE, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		fields = ['Player Name', 'Player TH', '11v11', '11v10', '11v9', '10v11', '10v10', '10v9', '9v11', '9v10', '9v9']
		writer.writerows([fields])
		for i in range(len(players)):
			writer.writerows([[players[i]] + [str(stats_dict[players[i]][0])] + [str(stats_dict[players[i]][1])] + [str(stats_dict[players[i]][2])] + [str(stats_dict[players[i]][3])] + [str(stats_dict[players[i]][4])] + [str(stats_dict[players[i]][5])] + [str(stats_dict[players[i]][6])] + [str(stats_dict[players[i]][7])] + [str(stats_dict[players[i]][8])] + [str(stats_dict[players[i]][9])]])

	with open(#INSERT_3STAR_ANALYSIS_CSV_HERE, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		fields = ['Player Name', 'Player TH', '11v11', '11v10', '11v9', '10v11', '10v10', '10v9', '9v11', '9v10', '9v9']
		writer.writerows([fields])
		for i in range(len(players)):
			writer.writerows([[players[i]] + [str(stats_dict_3[players[i]][0])] + [str(stats_dict_3[players[i]][1])] + [str(stats_dict_3[players[i]][2])] + [str(stats_dict_3[players[i]][3])] + [str(stats_dict_3[players[i]][4])] + [str(stats_dict_3[players[i]][5])] + [str(stats_dict_3[players[i]][6])] + [str(stats_dict_3[players[i]][7])] + [str(stats_dict_3[players[i]][8])] + [str(stats_dict_3[players[i]][9])]])
choice = True
while choice:
	try:
		choice = int(input("Do you want to write data (Press 1), analyse data (Press 2) or to quit (Press 3)? "))
	except ValueError:
		print ("Invalid input.")
		continue
	if choice == 1:
		writeData(stats, opponentClan, clanName, teamSize)
		print ("Writing successful")
	elif choice == 2:
		retrieveData()
	elif choice == 3:
		choice = False
	else:
		print ("Invalid choice. Try again.")
