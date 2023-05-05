import numpy as np
import nibabel as nib
import time
import os

def cal_subject_level_kappa(prediction, target, class_num):# class_num是你分割的目标的类别个数, 包括背景
    '''
    :param prediction: the automated segmentation result, a numpy array with shape of (h, w, d)
    :param target: the ground truth mask, a numpy array with shape of (h, w, d)
    :param class_num: total number of categories
    :return:
    '''
    eps = 1e-10
    empty_value = -1.0
    kappas = empty_value * np.ones((class_num), dtype=np.float32)
    for i in range(0, class_num):
        if i not in target and i not in prediction:
            continue
        target_per_class = np.where(target == i, 1, 0).astype(np.float32)
        prediction_per_class = np.where(prediction == i, 1, 0).astype(np.float32)

        n = target_per_class.size
        tp = np.sum(prediction_per_class * target_per_class)
        fp = np.sum(prediction_per_class) - tp
        fn = np.sum(target_per_class) - tp
        tn = n - tp - fp - fn

        fa = tp + tn
        fc = ((tn+fn)*(tn+fp)+(fp+tp)*(fn+tp))/n

        kappa = (fa - fc)/(n - fc)
        kappas[i] = kappa

    kappas = np.where(kappas == -1.0, np.nan, kappas)
    
    return kappas[1:]

# Change name list here
lst= [i for i in range(1,59)]
class_number = 3

kappa_list_left = []
kappa_list_right = []
print('This is Kappa test(consistency) for segmentation \n')
_time = time.time()
for i in lst:
    pre1_path = 'fang_label/CBCT-TEST_' + str(i) + '.nii.gz'
    pre2_path = 'wu_label_new/CBCT-TEST_' + str(i) + '.nii.gz'
    if os.path.exists(pre1_path)
    gt = nib.load('origin/gt1/{}.nii.gz'.format(i)).get_fdata()
    pre = nib.load('origin/gt2self/{}.nii.gz'.format(i)).get_fdata()
    print('Running ' + str(i) + '....')
    kap = cal_subject_level_kappa(pre, gt, class_number)
    print(str(i) + ' finished!')
    kappa_list_left.append(kap[0])
    kappa_list_right.append(kap[1])

print('\nTime spent: ' + str(time.time() - _time) + 's')
print('Kappa list left: ' + str(kappa_list_left))
print('Kappa list right: ' + str(kappa_list_right))
print('\nAvg Kappa left: ' + str(np.mean(kappa_list_left)))
print('\nAvg Kappa right: ' + str(np.mean(kappa_list_right)))