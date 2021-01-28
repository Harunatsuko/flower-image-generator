import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class Petal():
    """
    Main petal class. Kepps key points to draw petals, can draw petal and .

    Attributes
    ---------
    kp: dict
        The dict for key points of petals, where keys is petal unique id,
        and value is some group of points, that can be smoothed or can't.
        All base values are in [0,100] border of rows and columns

    """
    kp = {1:[{'points':[[4,4],[5,30],[6,40],[7,50]],
             'smooth_available':True},
            {'points':[[7,50],[14,65],[20,70],[33,75],[47,88]],
            'smooth_available':True},
           {'points':[[47,88],[49,86],[50,84],[55,70]],
            'smooth_available':True},
           {'points':[[55,70],[65,76],[70,77],[81,81]],
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
          'smooth_available':True}],
      7:[{'points':[[2,2],[5,30],[8,40],[10,50],[15,65],[23,78],[35,90]],
         'smooth_available':True},
        {'points':[[35,90],[37,91],[41,93],[43,94],[46,94],[50,94],[62,92]],
         'smooth_available':True},
        {'points':[[62,92],[64,82],[71,85],[75,87],[84,84]],
         'smooth_available':True}],
      8:[{'points':[[2,2],[5,30],[8,40],[10,50],[11,70]],
         'smooth_available':True},
        {'points':[[11,70],[18,83],[21,85],[25,86],[38,83]],
         'smooth_available':True},
        {'points':[[38,83],[42,90],[50,95],[56,94],[62,89],[64,82]],
         'smooth_available':True},
        {'points':[[64,82],[71,85],[75,86],[84,84]],
         'smooth_available':True}]}
    def __init__(self):
        pass
        
    def draw(self,img_size=100, kind=1, smooth=True, uz=True, scale=100, scale_x=0):
        """
        Draw petal

        Parameters
        ---------
        img_size: int, required
            The image size, where petal should be drawn, default=100
            
        kind: int, required
            Petal kind, this is petal id - key from kp attribute, default=1
            
        smooth: bool, required
            Smooth or not petal contour, default=True. This parameter is recommended to set True,
            when image_size is > 100
            
        uz: bool, required
            Make petal more narrow or make petal more wide, default=True
            More narrow if True, more wide if False
            
        scale: int, required
            How to scale petal on image: more value, less petal, default=100 (percents)
            If set less than 90, it can break the border of image and produce error,
            because of base key points petal values
            
        scale_x: float, required
            How match to make petal narrow or wide. Extreme values here 0 at min, 0.6 at max
            
        Returns
        ----------
        numpy.array:
            contour of petal to draw
        """
        
        # get the key points
        kp = self.kp[kind]
        contour = []
        for elem in kp:
            # scale to current image size
            d = [[int(np.round(v[0] * img_size/scale)),
                  int(np.round(v[1] * img_size/scale))] for v in elem['points']]
            if smooth:
                if (elem['smooth_available']) and (len(set([v[0] for v in d])) == len(d)):
                    smooth_fun = interp1d([p[0] for p in d],[p[1] for p in d],kind='cubic')
                    interp_x = np.arange(d[0][0],d[-1][0]+1,1)
                    interp_y = smooth_fun(interp_x)
                    contour_part = [[x,int(np.round(y))] for x,y in zip(interp_x,interp_y)]
                    contour = contour + contour_part
                else:
                    contour = contour + d
            else:
                contour = [a for a in d['points'] for d in kp ]
                
        # make petal contour more narrow or more wide
        if uz:
            contour = [[int(np.round(v[0] * (1-(np.abs(v[0]-v[1])/img_size)*scale_x))),
                        int(np.round(v[1] * (1-(np.abs(v[0]-v[1])/img_size)*scale_x)))] for v in contour]
        else:
            contour = [[int(np.round(v[0] / (1-(np.abs(v[0]-v[1])/img_size)*scale_x))),
                        int(np.round(v[1] / (1-(np.abs(v[0]-v[1])/img_size)*scale_x)))] for v in contour]
            
        # make full contour, mirror part about the main diagonal
        contour = contour + [[p[1],p[0]] for p in reversed(contour)]
        
# #         this part is for testing
#         img = np.ones((img_size,img_size,3))
#         cv2.fillPoly(img, pts =[np.array(contour)], color=(255,0,255))
#         plt.figure(figsize=(8, 8))
#         plt.imshow(img)
        return np.array(contour)