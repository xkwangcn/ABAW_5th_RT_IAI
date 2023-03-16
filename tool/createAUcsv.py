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
labelpath = '../data/Aff-Wild2/5th_ABAW_Annotations/AU_Detection_Challenge/AU_txt'
newlabelpath = '../data/Aff-Wild2/5th_ABAW_Annotations/AU_Detection_Challenge/AU_csv'
os.makedirs(newlabelpath, exist_ok=True)

filenames = os.listdir(labelpath)
n = 0
for filename in filenames:
    txtpath = os.path.join(labelpath, filename)
    # txt to list
    labelarray = []
    with open(txtpath, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            a = line.split('\n')[0]
            labelarray.append(a)

    filename = filename.split('.')[0]
    # creat new label array
    csvfile = open(os.path.join(newlabelpath, filename+'.csv'), 'w', newline='', encoding='gbk')
    writer = csv.writer(csvfile)
    writer.writerow(['frame', 'AU1', 'AU2', 'AU3', 'AU4', 'AU5', 'AU6', 'AU7', 'AU8', 'AU9', 'AU10', 'AU11', 'AU12',
                     'left seq', 'right seq', 'min seq'])
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
        if '-1' in label:
            left_seq, right_seq, min_seq = 0, 0, 0
            writer.writerow([frame, label.split(',')[0], label.split(',')[1], label.split(',')[2], label.split(',')[3],
                             label.split(',')[4], label.split(',')[5], label.split(',')[6], label.split(',')[7],
                             label.split(',')[8], label.split(',')[9], label.split(',')[10], label.split(',')[11],
                             left_seq, right_seq, min_seq])
        else:
            left_seq, right_seq, min_seq = cal_sequence(num, imagenames, labelarray, gap)
            writer.writerow([frame, label.split(',')[0], label.split(',')[1], label.split(',')[2], label.split(',')[3],
                             label.split(',')[4], label.split(',')[5], label.split(',')[6], label.split(',')[7],
                             label.split(',')[8], label.split(',')[9], label.split(',')[10], label.split(',')[11],
                             left_seq, right_seq, min_seq])
    csvfile.close()
    n += 1
    print(n, filename)
