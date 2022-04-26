import xlsxwriter
from turtle import distance
from torchreid.utils import FeatureExtractor
import torch
# from pytorch_metric_learning.distances import DotProductSimilarity
from scipy.spatial import distance
import io

# categories
categories = ["Same-Same", "Different-Same", "Different-Different"]
# categories = ["Different-Same", "Different-Different"]

for category in categories:

    # Create a workbook and add a worksheet.
    workbookName = category + ".xlsx"
    workbook = xlsxwriter.Workbook(workbookName)
    worksheet = workbook.add_worksheet()

    # define models
    model_names = ["shufflenet", "mobilenetv2_x1_4", "osnet_x1_0", "mlfn"]
    model_paths = ["shufflenet-bee1b265.pth.tar", "mobilenetv2_1.4-bc1cc36b.pth", "osnet_x1_0_imagenet.pth", "mlfn-9cb5a267.pth.tar"]

    for col in range(4): # col = model

        extractor = FeatureExtractor(
            model_name = model_names[col],
            model_path = model_paths[col],
            device='cpu' #should be cuda
        )

        image_list = []
        # populate file names
        for i in range(100):
            num = i+1
            if num < 10:
                image_path = '100test/' + category + '/person00' + str(num)
            elif num < 100:
                image_path = '100test/' + category + '/person0' + str(num)
            else:
                image_path = '100test/' + category + '/person' + str(num)

            image_list.append(image_path + "A.jpg")
            image_list.append(image_path + "B.jpg")
        
        print("Length of image list is: " + str(len(image_list)))
        print("Length should be 200")

        # feature extraction
        features = extractor(image_list)

        for row in range(100): # row = similarities
                idx = row*2
                dist = distance.euclidean(features[idx],features[idx+1]) # euclidean distance
                simStr = str(dist)
                worksheet.write(row, col, simStr)

    # close workbook
    workbook.close()



