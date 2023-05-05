import SimpleITK as sitk
import nibabel as nib
import numpy as np
import time
import math
import os

GT1 = 'gt1'
GT2 = 'gt2'
i = 1
while i <= 110:
    path1 = GT1 + f'/NERVETEST_{i}.nii.gz'
    path2 = GT2 + f'/NERVETEST_{i}.nii.gz'
    if os.path.exists(path1) and os.path.exists(path2):
        _gt1 = nib.load(path1)
        gt1 = _gt1.get_fdata()
        _gt2 = nib.load(path2)
        gt2 = _gt2.get_fdata()
        
        #pad if size different match in z direction
        if gt1.shape[2] < gt2.shape[2]:
            padsize = gt2.shape[2] - gt1.shape[2]
            up = math.floor(padsize/2)
            down = math.ceil(padsize/2)
            print('padding size: '+ str(padsize) + ' ....')
            gt1 = np.pad(gt1,[(0,0),(0,0),(up,down)], constant_values = 0)
        elif gt1.shape[2] > gt2.shape[2]:
            padsize = gt1.shape[2] - gt2.shape[2]
            up = math.floor(padsize/2)
            down = math.ceil(padsize/2)
            print('padding size: '+ str(padsize) + ' ....')
            gt2 = np.pad(gt2,[(0,0),(0,0),(up,down)], constant_values = 0)
        
        gt1_left = np.where(gt1 == 1, 1, 0)
        gt1_right = np.where(gt1 == 2, 1, 0)
        gt2_left = np.where(gt2 == 1, 1, 0)
        gt2_right = np.where(gt2 == 2, 1, 0)
        gtunion_left = np.logical_or(gt1_left,gt2_left)
        gtunion_left = gtunion_left.astype(int)
        gtunion_right = np.logical_or(gt1_right,gt2_right)
        gtunion_right = gtunion_right.astype(int)
        gtunion = gtunion_left + 2 * gtunion_right
        _gtunion = nib.Nifti1Image(gtunion,_gt1.affine,_gt1.header)
        _path = f'union_gt1gt2/NERVETEST_{i}.nii.gz'
        nib.save(_gtunion,_path)
        print(f'Union {i} saved')
    
    i += 1

