import numpy as np
import cv2
from petal import Petal
from colorer import Colorer

class Flower():
    """
    Flower class. Draw the flower level by level with another count of petals on each level.
    Draw center of flower.
    
    Parameters
    ---------
    img_size: int
        The image size, where flower should be drawn, default=300
        
    center_size: int
        Size of flower center default=40
        
    center_color: tuple
        Color of flower center default=(1,1,0)
        
    fill_color: tuple
        Color of petal filling before gradient filling to check petal borders default=(0.5,0.5,0.5)
        
    levels_cnt: int
        Flower levels count default=2
    
    fill_type: str
        Gradient filling type, can be 'top_down', 'diagonal' or 'center' default='center'
        
    petal_cnt: list or int or 'random'
        List of petal count for each level with length = levels_cnt, default='random'
        
    petal_kinds: list or int or 'random'
        List of petal kind (id) for each level with length = levels_cnt, default='random'
        
    scale: list or int or 'random'
        List of scale values for each level with length = levels_cnt, default='random'
        
    scale_x: list or int or 'random'
        List of scale_x values (to narrow or wide) for each level with length = levels_cnt, default='random'

    Attributes
    ---------
    petal: Petal
        Petal object, generates new petal for each level
        
    colorer: Colorer
        Colorer object make gradient filling and manage colors
        
    fill_color: tuple
        Color to fill petal before making gradient filling
        
    levels_cnt: int
        Flower levels count
        
    img: numpy.array
        Image containing flower
        
    img_size: int
        One number for square image, value of square side
        
    petal_cnt: list or int or 'random'
        list : a list of petal count for each level
        int: means that on each level there will be same petal count
        'random': a list of random petal count for each level will be generated
        
    petal_kinds: list or int or 'random'
        list : a list of petal kind for each level
        int: means that on each level there will be same petal kind
        'random': a list of random petal kind for each level will be generated
        
    scale: list or int or 'random'
        list : a list of petal scaling (common petal size) for each level
        int: means that on each level there will be same petal scaling
        'random': a list of random petal scaling for each level will be generated
        
    scale_x: list or int or 'random'
        list : a list of petal scaling (narrow or wide) for each level
        int: means that on each level there will be same petal scaling
        'random': a list of random petal scaling for each level will be generated
    """
    PETAL_CNT_MAX = 7
    PETAL_CNT_MIN = 4
    SHIFT_DEGREE = 60
    SCALE_LEFT = 90
    SCALE_RIGHT = 100
    BORDER_DARKNESS = 2.5
    def __init__(self, 
                 img_size=300,
                 center_size=40,
                 center_color=(1,1,0),
                 fill_color=(0.5,0.5,0.5),
                 levels_cnt=2,
                 fill_type = 'center',
                 petal_cnt='random',
                 petal_kinds='random',
                 scale='random',
                 scale_x='random'):
        self.petal = Petal()
        self.colorer = Colorer(fill_type)
        self.fill_color = fill_color
        self.levels_cnt = levels_cnt
        self.img = np.ones((img_size,img_size,3))#RGB channels
        self.img_size = img_size
        self.make_center(center_color,center_size)
        self.__parse_petal_count(petal_cnt)
        self.__parse_petal_kinds(petal_kinds)
        self.__parse_scale(scale)
        self.__parse_scale_x(scale_x)
        
    def make_center(self, color,center_size):
        center_coordinate = int(np.round(self.img_size/2))
        cv2.circle(self.img, (center_coordinate,center_coordinate), center_size, color,-1)
        
    def rotate(self ,point,f):
        b = [[np.cos(np.deg2rad(f)),np.sin(np.deg2rad(f))],
         [-np.sin(np.deg2rad(f)), np.cos(np.deg2rad(f))]]
        res = [a for a in np.dot(point,b)]
        return [int(np.round(a,5)) for a in res]
    
    def prepare_points(self, contour, points_in_contour, center_dist, angle, shift):
        cntr = [[a[0] -center_dist, a[1]-center_dist] for a in contour]
        cntr = [self.rotate(a,angle) for a in cntr]
        cntr = [[a[0] + shift, a[1]+shift] for a in cntr]

        points_in = [[[a[0] -center_dist, a[1]-center_dist] for a in row] for row in points_in_contour]
        points_in = [[self.rotate(a,angle) for a in row] for row in points_in]
        points_in = [[[a[0] +shift, a[1]+shift] for a in row] for row in points_in]
        return np.array(cntr), points_in
            
    def draw_level(self,level_size, petal_cnt, petal_num,center_dist = 0,grad_colors=None,scale=100,scale_x=0):
        grad_color_from, grad_color_to, border_color = self.__parse_grad_colors(grad_colors)
        
        # the div numbers is based on logic - center and proportion of petals to image
        img_size_div_2 = int(np.round(self.img_size/2))
        lvl_size_div_3 = int(np.round(level_size/3))
        
        # probability to make petal more narrow or wide
        uz  = np.random.randint(0,10) > 5
        contour = self.petal.draw(lvl_size_div_3, petal_num, True, uz, scale, scale_x)
        img_size_new = int(np.round((lvl_size_div_3/scale)*120))
        
        points_in_contour = self.colorer.get_points(contour, img_size_new)
        
        # find angle to rotate every petal by petal
        angle = int(np.round(360/petal_cnt))
        pred_angle = np.random.randint(self.SHIFT_DEGREE)

        for i in range(petal_cnt):
            cntr, points_in = self.prepare_points(contour,
                                                  points_in_contour,
                                                  center_dist,
                                                  pred_angle,
                                                  img_size_div_2)

            pred_angle = pred_angle + angle
            cv2.fillPoly(self.img, pts =[cntr], color=self.fill_color)
            cv2.drawContours(self.img, [cntr], -1, color = border_color,thickness=1)
            self.colorer.fill(self.img, cntr, points_in, grad_color_from, grad_color_to, self.fill_color)
    
    def draw(self, grad_colors='hot'):
        level_size = self.img_size
        for i in range(self.levels_cnt):
            self.draw_level(level_size,
                            self.petal_cnt[i],
                            self.petal_kinds[i],
                            grad_colors=grad_colors,
                            center_dist=np.random.randint(0,20)-10,
                            scale=self.scale[i],
                            scale_x=self.scale_x[i])
            level_size = int(np.round(level_size*(np.random.randint(5,8)/10)))
            
    def __parse_grad_colors(self, grad_colors):
        if not grad_colors:
            [grad_color_from, grad_color_to, border_color] = self.colorer.get_random_colors()
        elif type(grad_colors) == str:
            [grad_color_from, grad_color_to, border_color] = self.colorer.get_colors(grad_colors)
        else:
            [grad_color_from, grad_color_to, border_color] = grad_colors
            
        border_color = [a/self.BORDER_DARKNESS for a in border_color]
        return grad_color_from, grad_color_to, border_color
    
    def __parse_petal_count(self, petal_cnt):
        if petal_cnt == 'random':
            self.petal_cnt = [np.random.randint(self.PETAL_CNT_MIN,
                                           self.PETAL_CNT_MAX) for i in range(self.levels_cnt)]
        elif type(petal_cnt) == int:
            self.petal_cnt = [petal_cnt for i in range(self.levels_cnt)]
        else:
            self.petal_cnt = petal_cnt
            
    def __parse_petal_kinds(self, petal_kinds):
        if petal_kinds == 'random':
            self.petal_kinds = [np.random.randint(1,len(self.petal.kp)+1) for i in range(self.levels_cnt)] 
        elif type(petal_kinds) == int:
            self.petal_kinds = [petal_kinds for i in range(self.levels_cnt)]
        else:
            self.petal_kinds = petal_kinds
            
    def __parse_scale(self, scale):
        if scale == 'random':
            self.scale = [np.random.randint(self.SCALE_LEFT, self.SCALE_RIGHT) for i in range(self.levels_cnt)]
        elif type(scale) == int:
            self.scale = [scale for i in range(self.levels_cnt)]
        else:
            self.scale = scale
            
    def __parse_scale_x(self, scale_x):
        if scale_x == 'random':
            self.scale_x = [np.random.randint(0,40)/100 for i in range(self.levels_cnt)]
        elif type(scale_x) == int:
            self.scale_x = [scale_x for i in range(self.levels_cnt)]
        else:
            self.scale_x = scale_x