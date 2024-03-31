# SVI4Waste
This is to train a model for waste detection from street view images. 

Pano image: 126,414  
total image: 505,656

# /Data Explanation
for output data folder:
output: identified with dirt and gravel, 126,414  
img_path: added path to the img (WL), 126,414  
Data_long: separate dataset with direction, 505,656
Waste4Yolo: 135 file for training  
  
0119 progress:  15000  


Confusing factors: leaves, sparse grass / leaves,  informal markets, 
wet and dry dirt, gravel, haystack etc.



1. Self data:   
*   Original data (2935):  
/Users/wenlanzhang/Downloads/PhD_UCL/Data/Mapillary/Self_GeoReferenced/SVILocation.csv (local)   
/Users/wenlanzhang/PycharmProjects/SVI_Waste/Data/Output/Self/SVILocation.csv (local)  
they are the same  
*   Nan cleaned (2328):  
/content/drive/Shareddrives/Wenlan/SVI_Waste/self.csv (online)   
/PycharmProjects/SVI_Waste/Data/Output/Self/self.csv (local)
*   Uniformed:  
/content/drive/Shareddrives/Wenlan/SVI_Waste/self_uni.csv (online)  
/PycharmProjects/SVI_Waste/Data/Output/Self/self_uni.csv (local)  
*   Test output  
run with the 0311 trained model, output generated on 0314:  
/content/drive/Shareddrives/Wenlan/SVI_Waste/self_M0311.csv (online)
  
  
2. GSVI:   
*   Original data (113341, Nan cleaned?):  
/content/drive/Shareddrives/Wenlan/SVI_Waste/GSVI_img_path.csv (online)
/PycharmProjects/SVI_Waste/Data/Output/GSVI/GSVI_img_path.csv (local)    
*   Convert to long (453364):  
/content/drive/Shareddrives/Wenlan/SVI_Waste/GSVI_long.csv (online)  
/PycharmProjects/SVI_Waste/Data/Output/GSVI/GSVI_long.csv (local)  
*   Uniformed (453364):  
/content/drive/Shareddrives/Wenlan/SVI_Waste/GSVI_uni.csv (online)  
/PycharmProjects/SVI_Waste/Data/Output/GSVI/GSVI_uni.csv  (local)

3. Combined:  
*   Combined unanalysis 455692 = 453364 + 2328  
/content/drive/Shareddrives/Wenlan/SVI_Waste/self_uni.csv (online)  
/PycharmProjects/SVI_Waste/Data/Output/Combined_uni.csv (local)
