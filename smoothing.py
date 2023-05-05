import SimpleITK as sitk
import time 

PATH = 'tooth/005.nii.gz'
SAVE_PATH = 'tooth/post_005.nii.gz'

#template
def smoothing(path, save_path):
    sitkImage = sitk.ReadImage(path)
    #write smoothing method here


    sitkImage = sitkFilter.Execute(sitkImage)
    sitk.WriteImage(sitkImage, save_path)
    pass

def dilation(path, save_path):
    sitkImage = sitk.ReadImage(path)
    #write smoothing method here

    dilateFilter = sitk.BinaryDilateImageFilter()
    dilateFilter.SetBackgroundValue(0)
    for i in range(5):
        dilateFilter.SetForegroundValue(i+1)
        dilateFilter.SetKernelRadius(3)
        print(str(i+1) + '...')
        sitkImage = dilateFilter.Execute(sitkImage)

    sitk.WriteImage(sitkImage, save_path)
    
def erosion(path, save_path):
    sitkImage = sitk.ReadImage(path)
    #write smoothing method here

    erodeFilter = sitk.BinaryErodeImageFilter()
    erodeFilter.SetBackgroundValue(0)
    for i in range(3):
        erodeFilter.SetForegroundValue(i+1)
        erodeFilter.SetKernelRadius(3)
        print(str(i+1) + '...')
        sitkImage = erodeFilter.Execute(sitkImage)

    sitk.WriteImage(sitkImage, save_path)

def closing(path, save_path):
    sitkImage = sitk.ReadImage(path)

    closeFilter = sitk.BinaryMorphologicalClosingImageFilter()
    for i in range(3):
        closeFilter.SetForegroundValue(i+1)
        closeFilter.SetKernelRadius(3)
        print(str(i+1) + '...')
        sitkImage = closeFilter.Execute(sitkImage)
    
    sitk.WriteImage(sitkImage, save_path)

def median(path, save_path):
    sitkImage = sitk.ReadImage(path)

    medianFilter = sitk.MedianImageFilter()
    medianFilter.SetRadius(2)

    sitkImage = medianFilter.Execute(sitkImage)

    sitk.WriteImage(sitkImage, save_path)

def post(path, save_path):
    sitkImage = sitk.ReadImage(path)

    medianFilter = sitk.MedianImageFilter()
    medianFilter.SetRadius(2)
    sitkImage = medianFilter.Execute(sitkImage)
    
    dilateFilter = sitk.BinaryDilateImageFilter()
    dilateFilter.SetBackgroundValue(0)
    for i in range(32):
        dilateFilter.SetForegroundValue(i+1)
        dilateFilter.SetKernelRadius(1)
        print(str(i+1) + '...')
        sitkImage = dilateFilter.Execute(sitkImage)
    
    sitk.WriteImage(sitkImage, save_path)

if __name__=="__main__":

    _time = time.time()

    #closing(PATH, SAVE_PATH)
    #dilation(PATH, SAVE_PATH)
    #erosion(PATH, SAVE_PATH)
    #median(PATH, SAVE_PATH)
    post(PATH, SAVE_PATH)

    print('\nTime spent: ' + str(time.time() - _time) + 's')
    