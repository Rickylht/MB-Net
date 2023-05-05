import numpy as np
import SimpleITK as sitk
import os

def dicom2nii(folderPath, output_path):
    '''
        folderPath: dicom图片所在文件夹
        output_path: 文件保存的路径
    '''
    reader = sitk.ImageSeriesReader()

    folder_list = os.listdir(folderPath)
    for folder in folder_list:
        # print(folder)
        dicom_images_path = os.path.join(output_path, folder+'.nii.gz')
        # print(dicom_images_path)
        folder_path = os.path.join(folderPath, folder)
        # print(folder_path)
        dicom_names = reader.GetGDCMSeriesFileNames(folder_path)
        reader.SetFileNames(dicom_names)

        dicom_images = reader.Execute()
        sitk.WriteImage(dicom_images, dicom_images_path)
        print(f'save successfully! folder path:{dicom_images_path}')
