import numpy as np

class Colorer():
    def __init__(self):
        self.color_dict = {'hot':{'min':[3,0,0],
                                     'max':[11,11,1]},
                          'cold':{'min':[0,0,3],
                                     'max':[2,8,11]},
                          'pink':{'min':[1,1,1],
                                     'max':[11,3,11]}}
    
    def get_random_colors(self,colors_cnt=3):
        random_colors = []
        for i in range(colors_cnt):
            random_colors.append([np.random.rand() for i in range(3)])
        return random_colors
    
    def get_colors(self,colormap,colors_cnt=3):
        colors = []
        for i in range(colors_cnt):
            colors.append([np.random.randint(self.color_dict[colormap]['min'][0],
                                            self.color_dict[colormap]['max'][0])/10,
                          np.random.randint(self.color_dict[colormap]['min'][1],
                                            self.color_dict[colormap]['max'][1])/10,
                          np.random.randint(self.color_dict[colormap]['min'][2],
                                            self.color_dict[colormap]['max'][2])/10,])
        return colors