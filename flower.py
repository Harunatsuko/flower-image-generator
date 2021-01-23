import numpy as np
import cv2
from petal import Petal
from colorer import Colorer

class Flower():
    PETAL_CNT_MAX = 9
    PETAL_CNT_MIN = 3
    def __init__(self, center_size,img_size):
        self.petal = Petal()
        self.colorer = Colorer()
        self.fill_color = (0.5,0.5,0.5)
        self.img = np.ones((img_size,img_size,3))
        self.img_size = img_size
        self.make_center((1,1,0),center_size)
        
    def make_center(self, color,center_size):
        center_coordinate = int(np.round(self.img_size/2))
        cv2.circle(self.img, (center_coordinate,center_coordinate), center_size, color,-1)
        
    def rotate(self,point,f):
        b = [[np.cos(np.deg2rad(f)),np.sin(np.deg2rad(f))],
         [-np.sin(np.deg2rad(f)), np.cos(np.deg2rad(f))]]
        res = [a for a in np.dot(point,b)]
        return [int(np.round(a,5)) for a in res]
        
    def draw_level(self,level_size, cnt, petal_num,center_dist = 0,grad_colors=None):
        if not grad_colors:
            [grad_color_from, grad_color_from, border_color] = self.colorer.get_random_colors()
        elif type(grad_colors) == str:
            [grad_color_from, grad_color_to, border_color] = self.colorer.get_colors(grad_colors)
        else:
            [grad_color_from, grad_color_to, border_color] = grad_colors
            
        border_color = [a/3 for a in border_color]
        img_size_div_2 = int(np.round(self.img_size/2))
        lvl_size_div_3 = int(np.round(level_size/3))
        contour = self.petal.draw(lvl_size_div_3,petal_num,True,np.random.randint(0,3))
        points_in_contour = self.petal.get_cntr_points(np.array(contour),lvl_size_div_3)
        print('Contour points detected')
        angle = int(np.round(360/cnt))
        pred_angle = np.random.randint(30)
        center_row = np.random.randint(int(np.round(len(points_in_contour)/3)),
                                                     int(np.round((len(points_in_contour)/3)*2)))
        for i in range(cnt):
            cntr = [[a[0] -center_dist, a[1]-center_dist] for a in contour]
            cntr = [self.rotate(a,pred_angle) for a in cntr]
            cntr = [[a[0] + img_size_div_2, a[1]+img_size_div_2] for a in cntr]

            points_in = [[[a[0] -center_dist, a[1]-center_dist] for a in row] for row in points_in_contour]
            points_in = [[self.rotate(a,pred_angle) for a in row] for row in points_in]
            points_in = [[[a[0] +img_size_div_2, a[1]+img_size_div_2] for a in row] for row in points_in]

            pred_angle = pred_angle + angle
            cntr = np.array(cntr)
            cv2.fillPoly(self.img, pts =[cntr], color=self.fill_color)
            cv2.drawContours(self.img, [cntr], -1, color = border_color,thickness=1)
            self.petal.fill_grad(self.img,cntr,points_in,grad_color_from,grad_color_to,self.fill_color)
    
    def draw(self,levels_cnt,petal_cnt=None,petal_kinds=None,grad_colors='hot'):
        level_size = self.img_size
        if not petal_cnt:
            petal_cnt = [np.random.randint(self.PETAL_CNT_MIN,self.PETAL_CNT_MAX) for i in range(levels_cnt)]
        if not petal_kinds:
            petal_kinds = [np.random.randint(1,len(self.petal.kp)+1) for i in range(levels_cnt)]
        for i in range(levels_cnt):
            self.draw_level(level_size,
                            petal_cnt[i],
                            petal_kinds[i],
                            grad_colors=grad_colors,
                            center_dist=np.random.randint(0,6)-3)
            level_size = int(np.round(level_size*0.7))