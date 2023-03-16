#!/usr/bin/env python
import os
import csv


def cal_sequence(num, names, labels, gap):
    leftlen = 0
    rightlen = 0
    a = num-1
    b = num+1
    while a >= 1 + gap:
        if '-1' in labels[a-gap]:
            break
        else:
            leftlen += 1
            a -= 1
    while b <= len(names):
        if '-1' in labels[b-gap]:
            break
        else:
            rightlen += 1
            b += 1
    min_len = min(leftlen, rightlen) * 2 + 1
    return leftlen, rightlen, min_len


imagepath = '../data/Aff-Wild2/Faces'
labelpath = '../data/Aff-Wild2/5th_ABAW_Annotations/EXPR_Classification_Challenge/EXPR_txt'
newlabelpath = '../data/Aff-Wild2/5th_ABAW_Annotations/EXPR_Classification_Challenge/EXPR_csv'
os.makedirs(newlabelpath, exist_ok=True)

filenames = os.listdir(labelpath)
n = 0
for filename in filenames:
    # filename = '327.txt'
    txtpath = os.path.join(labelpath, filename)
    # txt to list
    labelarray = []
    with open(txtpath, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            l = line.split('\n')[0]
            labelarray.append(l)

    filename = filename.split('.')[0]
    # creat new label array
    csvfile = open(os.path.join(newlabelpath, filename+'.csv'), 'w', newline='', encoding='gbk')
    writer = csv.writer(csvfile)
    writer.writerow(['frame', 'EXPR', 'left seq', 'right seq', 'min seq'])
    filepath = os.path.join(imagepath, filename)
    imagenames = sorted(os.listdir(filepath), key=lambda x: int(x.split('.')[0]))
    if len(imagenames) <= len(labelarray)-1:
        gap = 0
    else:
        gap = len(imagenames) - len(labelarray) + 1
    for num in range(gap+1, len(imagenames)+1):
        frame = str(num).zfill(5)
        # get label
        label = labelarray[num - gap]
        if label == -1:
            left_seq, right_seq, min_seq = 0, 0, 0
            writer.writerow([frame, label, left_seq, right_seq, min_seq])
        else:
            left_seq, right_seq, min_seq = cal_sequence(num, imagenames, labelarray, gap)
            writer.writerow([frame, label, left_seq, right_seq, min_seq])
    csvfile.close()
    n += 1
    print(n, filename)
