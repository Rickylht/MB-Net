import numpy as np
import nibabel as nib
import time

#Also IoU test here
 
def cal_subject_level_dice(prediction, target, class_num):# class_num是你分割的目标的类别个数, 包括背景
    '''
    step1: calculate the dice of each category
    step2: remove the dice of the empty category and background, and then calculate the mean of the remaining dices.
    :param prediction: the automated segmentation result, a numpy array with shape of (h, w, d)
    :param target: the ground truth mask, a numpy array with shape of (h, w, d)
    :param class_num: total number of categories
    :return:
    '''
    eps = 1e-10
    empty_value = -1.0
    dscs = empty_value * np.ones((class_num), dtype=np.float32)
    for i in range(0, class_num):
        if i not in target and i not in prediction:
            continue
        target_per_class = np.where(target == i, 1, 0).astype(np.float32)
        prediction_per_class = np.where(prediction == i, 1, 0).astype(np.float32)

        tp = np.sum(prediction_per_class * target_per_class)
        fp = np.sum(prediction_per_class) - tp
        fn = np.sum(target_per_class) - tp
        dsc = 2 * tp / (2 * tp + fp + fn + eps)
        dscs[i] = dsc
    dscs = np.where(dscs == -1.0, np.nan, dscs)
    subject_level_dice = np.nanmean(dscs[1:])
    return subject_level_dice

# Change name list here
lst= [5,6]
class_number = 33#前景数+1（背景数）


dice_list = []
print('This is average Dice test \n')
_time = time.time()
for i in lst:
    gt = nib.load('gt/TOOTH_00{}.nii.gz'.format(i)).get_fdata()
    pre = nib.load('pre/TOOTH_00{}.nii.gz'.format(i)).get_fdata()
    print('Running ' + str(i) + '....')
    dsc = cal_subject_level_dice(pre, gt, class_number)
    print(str(i) + ' finished!')
    dice_list.append(dsc)

print('\nTime spent: ' + str(time.time() - _time) + 's')
print('Dice list: ' + str(dice_list))
print('Avg Dice: ' + str(np.mean(dice_list)))
print('Var Dice: ' + str(np.var(dice_list)))

print('\nAvg IoU: ' + str(np.mean(dice_list)/(2 - np.mean(dice_list))))
print('Var IoU: ' + str(np.var(dice_list)/(2 - np.var(dice_list))))