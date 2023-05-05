import SimpleITK as sitk
import os
import shutil

def nrrd2nii(oldpath, newpath):
    img = sitk.ReadImage(oldpath)
    sitk.WriteImage(img, newpath)

root = './' #遍历当前文件夹的root
i = 1
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if '.nrrd' in f:
            oldpath = os.path.join(dirpath,f)
            newpath= '{}.nii.gz'.format(i)
            nrrd2nii(oldpath, newpath)
            print(oldpath + ' to ' + newpath)
            i += 1
