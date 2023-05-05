import numpy as np
import nibabel as nib
import time

 
def cal_subject_level_precision(prediction, target, class_num):# class_num是你分割的目标的类别个数, 包括背景
    '''
    :param prediction: the automated segmentation result, a numpy array with shape of (h, w, d)
    :param target: the ground truth mask, a numpy array with shape of (h, w, d)
    :param class_num: total number of categories
    :return:
    '''
    eps = 1e-10
    empty_value = -1.0
    pres = empty_value * np.ones((class_num), dtype=np.float32)
    for i in range(0, class_num):
        if i not in target and i not in prediction:
            continue
        target_per_class = np.where(target == i, 1, 0).astype(np.float32)
        prediction_per_class = np.where(prediction == i, 1, 0).astype(np.float32)

        tp = np.sum(prediction_per_class * target_per_class)
        fp = np.sum(prediction_per_class) - tp
        
        pre = tp / (tp + fp)
        pres[i] = pre
    pres = np.where(pres == -1.0, np.nan, pres)
    
    return pres[1:]

# Change name list here
lst= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
class_number= 3

precision_list_left = []
precision_list_right = []
print('This is average Precision test \n')
_time = time.time()
for i in lst:
    gt = nib.load('origin/gt2self/{}.nii.gz'.format(i)).get_fdata()
    pre = nib.load('pre_nerve/00{}.nii.gz'.format(i)).get_fdata()
    print('Running ' + str(i) + '....')
    prec = cal_subject_level_precision(pre, gt, class_number)
    print(str(i) + ' finished!')
    precision_list_left.append(prec[0])
    precision_list_right.append(prec[1])

print('\nTime spent: ' + str(time.time() - _time) + 's')
print('Precision list left: ' + str(precision_list_left))
print('Precision list right: ' + str(precision_list_right))
print('Avg Precision left: ' + str(np.mean(precision_list_left)))
print('Var Precision left: ' + str(np.var(precision_list_left)))
print('Avg Precision right: ' + str(np.mean(precision_list_right)))
print('Var Precision right: ' + str(np.var(precision_list_right)))