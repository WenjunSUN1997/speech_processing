import os
import math
ref_files = os.listdir('ref/')
print(ref_files)
result_file_path = 'result/'
with open('wrong.txt') as file_wrong:
    file_wrong_name = file_wrong.readlines()

for index in range(len(file_wrong_name)):
    file_wrong_name[index] = file_wrong_name[index].replace('\n', '')

file_wrong_name = set(file_wrong_name)


for file in ref_files:
    correct_loop = 0
    correct_sequence = 0
    if file[:-4] in file_wrong_name:
        continue
    with open('ref/'+file, 'r') as file_ref:
        ref = file_ref.readlines()
    with open('result/'+file[:-4]+'_loop.hyp', 'r') as file_result_loop:
        result_loop = file_result_loop.readlines()
    with open('result/'+file[:-4]+'_sequence.hyp', 'r') as file_result_sequence:
        result_sequence = file_result_sequence.readlines()

    for index in range(len(ref)):
        if ref[index] != result_loop[index]:
            correct_loop +=1
        if ref[index] != result_sequence[index]:
            correct_sequence += 1

    positive_rate_loop = correct_loop / len(ref)
    positive_rate_sequence = correct_sequence / len(ref)
    con_int_loop = 1.96 * math.sqrt((positive_rate_loop * (1-positive_rate_loop)) / len(ref))
    con_int_sequence = 1.96 * math.sqrt((positive_rate_sequence * (1 - positive_rate_sequence)) / len(ref))
    print(file[:-4]+'\t'+'%.2f%%'%(positive_rate_loop*100)+
          '\t'+'%.2f%%'%(con_int_loop*100))
    print(file[:-4] + '\t' + '%.2f%%' % (positive_rate_sequence * 100) +
          '\t' + '%.2f%%' % (con_int_sequence * 100))