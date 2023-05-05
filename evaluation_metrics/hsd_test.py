import SimpleITK as sitk
import nibabel as nib
import numpy as np
import time

def cal_subject_level_hsd(prediction, target, class_num):
    empty_value = -1.0
    hsds = empty_value * np.ones((class_num), dtype=np.float32)
    hsdFilter = sitk.HausdorffDistanceImageFilter()
    for i in range(0, class_num):
        if i not in target and i not in prediction:
            continue
        target_per_class = np.where(target == i, 1, 0).astype(np.float32)
        prediction_per_class = np.where(prediction == i, 1, 0).astype(np.float32)

        sitk_target_per_class = sitk.GetImageFromArray(target_per_class)
        sitk_prediction_per_class = sitk.GetImageFromArray(prediction_per_class)

        hsdFilter.Execute(sitk_target_per_class, sitk_prediction_per_class)
        hsds[i] = hsdFilter.GetAverageHausdorffDistance()
    
    hsds = np.where(hsds == -1.0, np.nan, hsds)
    
    return hsds[1:]

lst= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
class_number = 3

hsd_list_left = []
hsd_list_right = []

print('This is average Hausdorff Distance test \n')
_time = time.time()
for i in lst:
    gt = nib.load('origin/gt2self/{}.nii.gz'.format(i)).get_fdata()
    pre = nib.load('pre_nerve/00{}.nii.gz'.format(i)).get_fdata()
    print('Running ' + str(i) + '....')
    dsc = cal_subject_level_hsd(pre, gt, class_number)
    print(str(i) + ' finished!')
    hsd_list_left.append(dsc[0])
    hsd_list_right.append(dsc[1])

print('\nTime spent: ' + str(time.time() - _time) + 's')
print('HSD list left: ' + str(hsd_list_left))
print('HSD list right: ' + str(hsd_list_right))
print('Avg HSD left: ' + str(np.mean(hsd_list_left)))
print('Var HSD left: ' + str(np.var(hsd_list_left)))
print('Avg HSD right: ' + str(np.mean(hsd_list_right)))
print('Var HSD right: ' + str(np.var(hsd_list_right)))