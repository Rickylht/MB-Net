import SimpleITK as sitk
import os
#检查本路径下每个nii.gz文件的尺寸

def checkdim(path):
    img = sitk.ReadImage(path)

    print("原点位置:{}".format(img.GetOrigin()))
    print("尺寸：{}".format(img.GetSize()))
    print("体素大小(x,y,z):{}".format(img.GetSpacing()) )
    print("图像方向:{}".format(img.GetDirection()))

    #查看图像相关的纬度信息
    print("维度:{}".format(img.GetDimension()))
    print("宽度:{}".format(img.GetWidth()))
    print("高度:{}".format(img.GetHeight()))
    print("深度(层数):{}".format(img.GetDepth()))

    #体素类型查询
    print("数据类型:{}".format(img.GetPixelIDTypeAsString()))

if __name__=="__main__":
    root = './'
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if  ".nii.gz" in f:
                print(f+'尺寸:')
                checkdim(os.path.join(dirpath,f))
                print('\n')