
ans = open("./queries/ans_train.csv")
# out = open("./queries/output_train.csv")
out = open("./output.csv")
line = ans.readline(); line = out.readline()
Sum = 0
for i in range(10):
	line_ans = ans.readline()[4:-1]
	line_out = out.readline()[4:-1]
	ans_list = line_ans.split(' ')
	out_list = line_out.split(' ')
	AP = 0
	correct_num = 0
	for i in range(len(out_list)):
		if out_list[i] in ans_list:
			correct_num += 1
			AP += (correct_num)/(i+1)
	Sum += (AP/len(ans_list))
	print(AP/len(ans_list))

print("MAP =",Sum/10)

'''
k = 1.5, b = 0.4, MAP = 0.7968108174592483  / 
k = 1.4, b = 0.4, MAP = 0.7953526678211351  / 
k = 1.3, b = 0.4, MAP = 0.7951079228692393  / 
k = 1.2, b = 0.4, MAP = 0.7887070000515493  / 


0.7750711665513065
0.778605841418991
0.7661319904450518
0.7763877553647258
0.786564379289086
0.7675284295560686

0.7968108174592483  0.7842484996928061
'''