import csv

def readCSV():
	with open(#INSERT_MODIFIED_CSV_HERE, 'r+', newline='') as csvfile:
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
					for j in range(1,9):
						data_dict.setdefault(keys[i], []).append(row[j]) #the making of vector
			csvfile.seek(0) #pointer back to zero for next i
	return data_dict

def analyseCSV(data_dict):
	players = list(data_dict.keys())
	for i in range(len(data_dict)):
		data_dict[players[i]][0] = int (data_dict[players[i]][0]) 
	data_dict = dict(sorted(data_dict.items(), key = lambda e: e[1][0], reverse = True))
	for i in range(len(data_dict)):
		data_dict[players[i]][0] = str (data_dict[players[i]][0])
	players = list(data_dict.keys())
	stats_dict_fresh = {}
	stats_dict_cleanup = {}
	for i in range(len(players)):
		stats_dict_fresh.setdefault(players[i], ['','','','','','']) #TH 11v11 11v10 10v11 10v10 9v9
		stats_dict_cleanup.setdefault(players[i], ['','','','','',''])
	
	for i in range(len(players)):
		playerTH = data_dict[players[i]][0]
		stats_dict_fresh[players[i]][0] = playerTH
		stats_dict_cleanup[players[i]][0] = playerTH
		player_list_len = len(data_dict[players[i]])
		stars_fresh = [0,0]
		stars_cleanup = [0,0]
		counter_fresh = [0,0]
		counter_cleanup = [0,0]
		counter = 0
		if playerTH == '11':
			for j in range(3, 6):
				stats_dict_fresh[players[i]][j] = 'NA'
				stats_dict_cleanup[players[i]][j] = 'NA'

			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '11':
					star = int(data_dict[players[i]][j-1])
					if star == 3 and data_dict[players[i]][j+1] == '1':
						stars_fresh[0] += star
						counter_fresh[0] += 1
					elif star == 3 and data_dict[players[i]][j+1] == '0':
						stars_cleanup[0] += star
						counter_cleanup[0] += 1
					else:
						counter += 1
				elif data_dict[players[i]][j] == '10':
					star = int(data_dict[players[i]][j-1])
					if star == 3 and data_dict[players[i]][j+1] == '1':
						stars_fresh[1] += star
						counter_fresh[1] += 1
					elif star == 3 and data_dict[players[i]][j+1] == '0':
						stars_cleanup[1] += star
						counter_cleanup[1] += 1
					else:
						counter += 1
				if flag == 0:
					j += 3
					flag = 1
				elif flag == 1:
					j += 5
					flag = 0
			#print (stars_cleanup)
			#print (stars_fresh)
			#print (counter_cleanup)
			#print (counter_fresh)
			#j is tracking 11v11 11v10, k is tracking fresh and cleanup
			k = 1
			for j in range(2):
				if counter_fresh[j] != 0:
					stats_dict_fresh[players[i]][k] = round(((stars_fresh[j]/(counter_fresh[j] + counter))/3)*100, 2)
				else:
					stats_dict_fresh[players[i]][k] = '0'
				if counter_cleanup[j] != 0:
					stats_dict_cleanup[players[i]][k] = round(((stars_cleanup[j]/(counter_cleanup[j] + counter))/3)*100, 2)
				else:
					stats_dict_cleanup[players[i]][k] = '0'
				k += 1

		elif playerTH == '10':
			for j in range(1, 3):
				stats_dict_fresh[players[i]][j] = 'NA'
				stats_dict_cleanup[players[i]][j] = 'NA'
			stats_dict_fresh[players[i]][5] = 'NA'
			stats_dict_cleanup[players[i]][5] = 'NA'
			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '11':
					star = int(data_dict[players[i]][j-1])
					if star == 2 and data_dict[players[i]][j+1] == '1':
						stars_fresh[0] += star
						counter_fresh[0] += 1
					elif star == 2 and data_dict[players[i]][j+1] == '0':
						stars_cleanup[0] += star
						counter_cleanup[0] += 1
					else:
						counter += 1
				elif data_dict[players[i]][j] == '10':
					star = int(data_dict[players[i]][j-1])
					if star == 3 and data_dict[players[i]][j+1] == '1':
						stars_fresh[1] += star
						counter_fresh[1] += 1
					elif star == 3 and data_dict[players[i]][j+1] == '0':
						stars_cleanup[1] += star
						counter_cleanup[1] += 1
					else:
						counter += 1
				if flag == 0:
					j += 3
					flag = 1
				elif flag == 1:
					j += 5
					flag = 0
			k = 3
			for j in range(2):
				if counter_fresh[j] != 0:
					stats_dict_fresh[players[i]][k] = round(((stars_fresh[j]/(counter_fresh[j] + counter))/3)*100, 2)
				else:
					stats_dict_fresh[players[i]][k] = '0'
				if counter_cleanup[j] != 0:
					stats_dict_cleanup[players[i]][k] = round(((stars_cleanup[j]/(counter_cleanup[j] + counter))/3)*100, 2)
				else:
					stats_dict_cleanup[players[i]][k] = '0'
				k += 1
		elif playerTH == '9':
			for j in range(1, 5):
				stats_dict_fresh[players[i]][j] = 'NA'
				stats_dict_cleanup[players[i]][j] = 'NA'
			flag = 0
			j = 2
			while j < player_list_len:
				if data_dict[players[i]][j] == '9':
					star = int(data_dict[players[i]][j-1])
					if star == 3 and data_dict[players[i]][j+1] == '1':
						stars_fresh[0] += star
						counter_fresh[0] += 1
					elif star == 3 and data_dict[players[i]][j+1] == '0':
						stars_cleanup[0] += star
						counter_cleanup[0] += 1
					else:
						counter += 1
				
				if flag == 0:
					j += 3
					flag = 1
				elif flag == 1:
					j += 5
					flag = 0
			#print (stars_cleanup)
			#print (stars_fresh)
			#print (counter_cleanup)
			#print (counter_fresh)
			if counter_fresh[0] != 0:
				stats_dict_fresh[players[i]][5] = round(((stars_fresh[0]/(counter_fresh[0] + counter))/3)*100, 2)
			else:
				stats_dict_fresh[players[i]][5] = '0'
			if counter_cleanup[0] != 0:
				stats_dict_cleanup[players[i]][5] = round(((stars_cleanup[0]/(counter_cleanup[0] + counter))/3)*100, 2)
			else:
				stats_dict_cleanup[players[i]][5] = '0'
		#print (stats_dict_cleanup)
		#print (stats_dict_fresh)
	with open(#INSERT_ANALYSIS_FILE_HERE, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		header = ['Fresh 3 star Percentage']
		writer.writerows([header])
		fields = ['Player Name', 'Player TH', '11v11', '11v10', '10v11', '10v10', '9v9']
		writer.writerows([fields])
		for i in range(len(players)):
			writer.writerows([[players[i]] + [str(stats_dict_fresh[players[i]][0])] + [str(stats_dict_fresh[players[i]][1])] + [str(stats_dict_fresh[players[i]][2])] + [str(stats_dict_fresh[players[i]][3])] + [str(stats_dict_fresh[players[i]][4])] + [str(stats_dict_fresh[players[i]][5])]])
		header = ['Cleanup 3 star Percentage']
		writer.writerows([header])
		writer.writerows([fields])
		for i in range(len(players)):
			writer.writerows([[players[i]] + [str(stats_dict_cleanup[players[i]][0])] + [str(stats_dict_cleanup[players[i]][1])] + [str(stats_dict_cleanup[players[i]][2])] + [str(stats_dict_cleanup[players[i]][3])] + [str(stats_dict_cleanup[players[i]][4])] + [str(stats_dict_cleanup[players[i]][5])]])

data = readCSV()
analyseCSV(data)