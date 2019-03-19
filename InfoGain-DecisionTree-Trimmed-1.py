import math
dataset = []

#--------------load and prepare dataset----------------
'''
attrs == ['age', 'income', 'student', 'credit_rating', 'buy_computer']
dataset == [['<=30', 'high', 'no', 'fair', 'no'], 
			['<=30', 'high', 'no', 'excellent', 'no'], 
			['31...40', 'high', 'no', 'fair', 'yes'], 
			['>40', 'medium', 'no', 'fair', 'yes'], 
			['>40', 'low', 'yes', 'fair', 'yes'], 
			['>40', 'low', 'yes', 'excellent', 'no'], 
			['31...40', 'low', 'yes', 'excellent', 'yes'], 
			['<=30', 'medium', 'no', 'fair', 'no'], 
			['<=30', 'low', 'yes', 'fair', 'yes'], 
			['>40', 'medium', 'yes', 'fair', 'yes'], 
			['<=30', 'medium', 'yes', 'excellent', 'yes'], 
			['31...40', 'medium', 'no', 'excellent', 'yes'], 
			['31...40', 'high', 'yes', 'fair', 'yes'], 
			['>40', 'medium', 'no', 'excellent', 'no']]

classes == [['<=30', '31...40', '>40'], ['high', 'medium', 'low'], ['no', 'yes'], ['fair', 'excellent'], ['no', 'yes']]
classcount == [{'<=30': 5, '31...40': 4, '>40': 5}, {'high': 4, 'medium': 6, 'low': 4}, {'no': 7, 'yes': 7}, {'fair': 8, 'excellent': 6}, {'no': 5, 'yes': 9}]
'''
with open('AllElectronicsDataset.csv') as f:
	for line in f:
		l = line.split(',')
		for i in range(len(l)):
			l[i]=l[i].strip()
			l[i]=l[i].replace('\n','')
		dataset.append(l)

attrs = dataset[0]
dataset = dataset[1:]
classes = []
classcount = []
for j in range(len(attrs)):	#for Columns
	col = j
	c=[]
	count = {}
	for i in range(len(dataset)):	#For Rows
		#print(dataset[i][col])
		
		if(dataset[i][col] not in c):
			c.append(dataset[i][col])
			count[dataset[i][col]] = 1	
		else:
			count[dataset[i][col]] += 1	
	classes.append(c)
	classcount.append(count)

'''
counts= {'<=30': [{'no': 0}, {'yes': 0}], '31...40': [{'no': 0}, {'yes': 0}], '>40': [{'no': 0}, {'yes': 0}]}
'''
def getClassCount(attr_index):
	counts={}
	for i in range(len(classes[attr_index])):
		#print(classes[attr_index][i])
		counts[classes[attr_index][i]] = []
		for y in classes[len(classes)-1]:
			counts[classes[attr_index][i]].append({y:0})

	#print('counts=',counts)
	for x in dataset:
		last_attr=len(attrs)-1
		class_index0 = classes[attr_index].index(x[attr_index])
		class_index1 = classes[last_attr].index(x[last_attr])

		counts[classes[attr_index][class_index0]][classes[len(classes)-1].index(x[last_attr])][x[last_attr]] += 1

	return counts
'''
infogain += (classcount[attr][k]/total)*(-r1*log r1 -r2*log r2)
'''
def computeInfoOn(attr):
	total = 0
	for k in classcount[attr]:
		#print('CCAK',classcount[attr][k])
		total += int(classcount[attr][k])
	
	counts = getClassCount(attr)	
	#info_gain = (-(r1)*math.log(r1,2)-r2*math.log(r2,2))
	info_gain = 0
	for k in classes[attr]:
		yes_count = counts[k][1]['yes']
		no_count = counts[k][0]['no']
		total_tuples = yes_count + no_count
		
		r1 = counts[k][0]['no']/total_tuples	# counts[k][0]['no'] = No count
		r2 = counts[k][1]['yes']/total_tuples	# counts[k][1]['yes'] = Yes Count
		#print('=>({}/{})*(-{}log {}-{} log {})'.format(classcount[attr][k],total,r1,r1,r2,r2 ))
		
		if (r1==0 or r2==0):
			if (r1==0 and r2==0):
				info_gain += 0
			elif(r1==0 and r2!=0):
				tmp = (classcount[attr][k]/total)*(-r2*math.log(r2,2))
				info_gain += tmp
			elif(r1!=0 and r2==0):
				tmp = (classcount[attr][k]/total)*(-(r1)*math.log(r1,2))
				info_gain += tmp
		else:
			tmp = (classcount[attr][k]/total)*(-(r1)*math.log(r1,2)-r2*math.log(r2,2))
			info_gain += tmp
		#print('infoGain for {} = {}'.format(k,info_gain))
	
	#print(attrs[attr],':Info gain = ',info_gain)
	return info_gain
	
yes_count = classcount[4]['yes']
no_count = classcount[4]['no']
total_tuples = yes_count + no_count
r1 = yes_count/total_tuples
r2 = no_count/total_tuples

info_all = -(r1)*math.log(r1,2)-r2*math.log(r2,2)
print('Info Overall=',info_all)

infoAge = computeInfoOn(0)
infoIncome = computeInfoOn(1)
infoStudent = computeInfoOn(2)
infoCredit_rating = computeInfoOn(3)

print('Info for Age = %.4f'%infoAge)
print('Info for Income = %.4f'%infoIncome)
print('Info for Student = %.4f'%infoStudent)
print('Info for Credit Raring = %.4f'%infoCredit_rating)

gainAge = info_all - infoAge
gainIncome = info_all - infoIncome
gainStudent = info_all - infoStudent
gainCredit_rating = info_all - infoCredit_rating

print()
print('Gain for Age = %.4f'%gainAge)
print('Gain for Income = %.4f'%gainIncome)
print('Gain for Student = %.4f'%gainStudent)
print('Gain for Credit Raring = %.4f'%gainCredit_rating)
