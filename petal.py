import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class Petal():
    def __init__(self):
        self.kp = {1:[{'points':[[5,5],[6,30],[7,40],[8,50],[10,65],[18,95]],
                        'smooth_available':True},
                       {'points':[[18,95],[30,95],[42,85],[50,70]],
                       'smooth_available':True},
                       {'points':[[50,70],[65,82],[90,90],[91,91]],
                       'smooth_available':True}],
                   2:[{'points':[[9,9],[8,13],[2,30],[3,40],[4,50]],
                       'smooth_available':False},
                      {'points':[[4,50],[10,65],[20,77],[25,79],[30,81],[40,83]],
                         'smooth_available':True},
                      {'points':[[40,83],[50,85],[65,87],[80,90],[100,100]],
                         'smooth_available':True}],
                   3: [{'points':[[8,10],[6,20],[4,35],[5,40],[7,50],[15,65]],
                      'smooth_available':False},
                        {'points':[[15,65],[30,80],[50,85],[70,90]],
                         'smooth_available':True},
                        {'points':[[70,90],[65,65]],
                         'smooth_available':False}],
                   4:[{'points':[[6,6],[7,20],[9,40],[11,50],[20,70],[30,80],[40,87],[55,92],[75,95],[87,90]],
                        'smooth_available':True}],
                   5:[{'points':[[10,10],[8,20],[12,40],[14,50],[20,65],[30,80],[40,85],[55,92]],
                      'smooth_available':True},
                     {'points':[[57,80],[62,77],[70,77],[92,92]],
                      'smooth_available':True}],
                   6:[{'points':[ [10,10],[8,20],[7,30],[7,40]],
                      'smooth_available':False},
                    {'points':[[7,40],[9,50],[12,65],[15,75],[20,83],[27,90],[40,96]],
                      'smooth_available':True},
                     {'points':[[40,96],[45,97],[55,95],[60,90],[63,80],[65,65]],
                      'smooth_available':True}]}
        
    def draw(self,img_size=100,kind=1,smooth=True,uz=0):
        kp = self.kp[kind]
        contour = []
        for elem in kp:
            d = [[int(np.round(v[0] * img_size/100))+uz,
                  int(np.round(v[1] * img_size/100))-uz] for v in elem['points']]
            if smooth:
                if (elem['smooth_available']) and (len(set([v[0] for v in d])) == len(d)):
                    smooth_fun = interp1d([p[0] for p in d],[p[1] for p in d],kind='cubic')
                    interp_x = np.arange(d[0][0],d[-1][0],1)
                    interp_y = smooth_fun(interp_x)
                    contour_part = [[x,int(np.round(y))] for x,y in zip(interp_x,interp_y)]
                    contour = contour + contour_part
                else:
                    contour = contour + d
            else:
                contour = [a for a in d['points'] for d in kp ]
        contour = contour + [[p[1],p[0]] for p in reversed(contour)]
#         img = np.ones((img_size,img_size,3))
#         cv2.fillPoly(img, pts =[np.array(contour)], color=(255,0,255))
#         plt.figure(figsize=(8, 8))
#         plt.imshow(img)
        return contour

    def split_colors(self,color_count,color_from,color_to):
        colors = []
        for c in range(3):#RGB
            step = np.abs(color_from[c] - color_to[c])/color_count
            if step:
                if color_from[c]>color_to[c]:
                    color = np.arange(color_from[c],color_to[c],-step)
                else:
#                     print(color_from[c],color_to[c],step)
                    color = np.arange(color_from[c],color_to[c],step)
            else:
                color = [color_from[c] for i in np.arange(color_count)]


            colors.append(color)
        colors = [(a,b,c) for a,b,c in zip(colors[0],colors[1],colors[2])]
        return colors
    
    def fill_grad(self,img,contour,points,color_from, color_to,fill_color):
        color_count = len(points)
        colors = self.split_colors(color_count,color_from,color_to)

        for i,row in enumerate(points):
            color = colors[i]
            for point in row:
                if (all(img[point[1], point[0]] ==fill_color)):
                    img[point[1], point[0]] = color
                if (all(img[point[1]+1, point[0]+1] ==fill_color)):
                    img[point[1]+1, point[0]+1] = color
                if (all(img[point[1]+1, point[0]][0] ==fill_color)):
                    img[point[1]+1, point[0]] = color

    
    def get_cntr_points(self,contour, img_size):
        res_arr = []
        for row in range(img_size):
            tmp_arr = []
            for col in range(img_size):
                if cv2.pointPolygonTest(contour,(row,col),True)> 0:
                    tmp_arr.append([row,col])
            if len(tmp_arr):
                res_arr.append(tmp_arr)
        return res_arr
    
    def get_cntr_points_center(self,contour, img_size):
        res_arr = []
        for row in range(img_size):
            tmp_arr = []
            curr_row = row
            curr_col = 0
            while curr_row != -1:
                if cv2.pointPolygonTest(contour,(curr_row,curr_col),True)> 0:
                    tmp_arr.append([curr_row,curr_col])
                curr_row = curr_row -1
                curr_col = curr_col +1
            if len(tmp_arr):
                res_arr.append(tmp_arr)
                
        for row in range(img_size):
            tmp_arr = []
            curr_row = row
            curr_col = img_size -1
            while curr_row != img_size:
                if cv2.pointPolygonTest(contour,(curr_row,curr_col),True)> 0:
                    tmp_arr.append([curr_row,curr_col])
                curr_row = curr_row +1
                curr_col = curr_col -1
            if len(tmp_arr):
                res_arr.append(tmp_arr)
        return res_arr
    
    def draw_test_petal(self,img_size=100):
        kp = {0:[20,20],
          1:[15,30],
          2:[10,40],
         3:[10,50],
         4:[15,65],
         5:[30,80],
         6:[50,85],
         7:[65,87],
         8:[80,90],
         9:[100,100]}
        for k,v in kp.items():
            kp[k] = [int(np.round(v[0] * img_size/100)),int(np.round(v[1] * img_size/100))]

        contour = [p for p in list(kp.values())]
        contour = contour + [[p[1],p[0]] for p in reversed(list(kp.values()))]
        return contour