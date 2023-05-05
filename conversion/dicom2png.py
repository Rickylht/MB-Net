import pydicom
import cv2
import glob
from tqdm import tqdm

def process(f, size=1024, save_folder=""):
    patient = f.split('/')[-2]
    image = f.split('/')[-1][:-4]

    dicom = pydicom.dcmread(f)

    try:
        img = load_img_dicomsdl(f)
    except:
        img = dicom.pixel_array

    img = (img - img.min()) / (img.max() - img.min())

    if dicom.PhotometricInterpretation == "MONOCHROME1":
        img = 1 - img

    img = cv2.resize(img, (size, size))
    
    #crop
    #img = crop_ROI(img)
    
    cv2.imwrite(save_folder + f"{patient}_{image}.png", (img * 255).astype(np.uint8))#default to 3 channel

test_images = glob.glob("/workspace/RSNA-main/data/rsna-origin/train_images/*/*.dcm")
output_dir = "data/self_1024x1024/"

for uid in tqdm(test_images):
    process(uid, size=1024, save_folder=output_dir)