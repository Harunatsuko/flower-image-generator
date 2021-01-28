import numpy as np
import cv2

class Colorer():
    """
    Colorer class. Manages colormaps as predefined as generated.
    Splits colors for gradient filling.
    Finds contour point in predefined order
    Gradient fill prepared array of points.

    Attributes
    ---------
    color_dict: dict
        Min and max values to generate some froup of colors (colormap)
    """
    color_dict = {'hot':{'min':[3,3,0],
                             'max':[11,10,1]},
                  'cold':{'min':[0,0,3],
                             'max':[4,8,11]},
                  'pink':{'min':[2,1,2],
                             'max':[11,3,11]},
                  'green':{'min':[0,3,0],
                            'max':[8,11,8]}}

    def __init__(self, fill_type):
        self.fill_type = fill_type
        self.gradient_fill = {'top_down':{'get_points':self.get_cntr_points,
                                 'fill':self.fill_grad},
                            'diagonal':{'get_points':self.get_cntr_points_center,
                                'fill':self.fill_grad},
                            'center':{'get_points':self.get_cntr_points_from_center,
                                 'fill':self.fill_grad_diff}}
        
    def get_points(self,*args):
        return self.gradient_fill[self.fill_type]['get_points'](*args)
    
    def fill(self,*args):
        self.gradient_fill[self.fill_type]['fill'](*args)
    
    def get_random_colors(self, colors_cnt=3):
        random_colors = []
        for i in range(colors_cnt):
            random_colors.append([np.random.rand() for i in range(3)])
        return random_colors
    
    def get_colors(self, colormap, colors_cnt=3):
        colors = []
        for i in range(colors_cnt):
            color = [np.random.randint(self.color_dict[colormap]['min'][0],
                                            self.color_dict[colormap]['max'][0])/10,
                          np.random.randint(self.color_dict[colormap]['min'][1],
                                            self.color_dict[colormap]['max'][1])/10,
                          np.random.randint(self.color_dict[colormap]['min'][2],
                                            self.color_dict[colormap]['max'][2])/10]
            if colormap == 'hot':
                if color[1] > color[0]:
                    color[1],color[0] = color[0],color[1]
            colors.append(color)
        return colors
    
    def split_colors(self, color_count, color_from, color_to):
        """
        Split colors for gradient filling depends on color count

        Parameters
        ---------
        color_count: int, required
            Color count, for example in row or some area
            
        color_from: list or tuple, required
            First color of gradient filling
            
        color_to: list or tuple, required
            Second color of gradient filling
            
        Returns
        ----------
        list:
            list of colors for gradient filling
        """
        colors = []
        for c in range(3):#RGB
            step = np.abs(color_from[c] - color_to[c])/color_count
            if step:
                if color_from[c]>color_to[c]:
                    color = np.arange(color_from[c],color_to[c],-step)
                else:
                    color = np.arange(color_from[c],color_to[c],step)
            else:
                color = [color_from[c] for i in np.arange(color_count)]


            colors.append(color)
        colors = [(a,b,c) for a,b,c in zip(colors[0],colors[1],colors[2])]
        return colors

    
    def get_cntr_points(self, contour, img_size):
        """
        Finds the contour points in order of all rows and columns from 0 to image_size

        Parameters
        ---------
        contour: numpy.array, required
            The countour to find points in
            
        img_size: int, required
            The image size, where petal should be drawn
            
        Returns
        ----------
        list:
            points in contour in predefined order
        """
        res_arr = []
        # for each row
        for row in range(img_size):
            tmp_arr = []
            # for each column
            for col in range(img_size):
                # if point in contour
                if cv2.pointPolygonTest(contour,(row,col),True)> 0:
                    # add point to current line
                    tmp_arr.append([row,col])
            if len(tmp_arr):
                # add current line to result array
                res_arr.append(tmp_arr)
        return res_arr
    
    def get_cntr_points_center(self, contour, img_size):
        """
        Finds the contour points in order from image border to main diagonal

        Parameters
        ---------
        contour: numpy.array, required
            The countour to find points in
            
        img_size: int, required
            The image size, where petal should be drawn
            
        Returns
        ----------
        list:
            points in contour in predefined order
        """
        res_arr = []
        
        # first border line
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
              
        # second border line
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
    
    def get_cntr_points_from_center(self, contour, img_size):
        """
        Finds the points in order from center of countour to image border

        Parameters
        ---------
        contour: numpy.array, required
            The countour to find points in
            
        img_size: int, required
            The image size, where petal should be drawn
            
        Returns
        ----------
        list:
            points in contour in predefined order
        """
        res_arr = []
        half_img_size = int(np.round(img_size/3))
        diag_coord = np.random.randint(half_img_size,2*half_img_size)
        # find the center point
        center_point = [diag_coord,diag_coord]
        # define all borders point
        border = ([[0,i] for i in np.arange(0,img_size)] + 
                 [[img_size,i] for i in np.arange(0,img_size)] +
                    [[i,0] for i in np.arange(0,img_size)] + 
                 [[i,img_size] for i in np.arange(0,img_size)])
        for point in border:
            tmp_res = []
            row_diff = point[0] - center_point[0]
            col_diff = point[1] - center_point[1]
            # find the distance between center point and border point
            dist = int(np.round(np.sqrt(row_diff*row_diff+col_diff*col_diff)))
            # find steps for row and column to go from center to border
            row_step = row_diff/dist
            col_step = col_diff/dist
            
            row_diff = center_point[0]
            col_diff = center_point[1]
            c_point = [int(np.round(row_diff)),
                        int(np.round(col_diff))]

            # go from center to border until points inside image
            while ((c_point[0]>= 0) 
                   and (c_point[0] < img_size) 
                   and (c_point[1]>= 0) 
                   and (c_point[1] < img_size)):
                if cv2.pointPolygonTest(contour,(c_point[0],c_point[1]),True)> 0:
                    tmp_res.append(c_point)
                row_diff = row_diff + row_step
                col_diff = col_diff + col_step
                c_point = [int(np.round(row_diff)),
                           int(np.round(col_diff))]
            if len(tmp_res):
                res_arr.append(tmp_res)
        return res_arr
    
    def fill_grad(self,img, contour, points, color_from, color_to, fill_color):
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
                    
    def fill_grad_diff(self, img, contour, points, color_from, color_to, fill_color):
        for i,line in enumerate(points):
            color_count = len(line)
            colors = self.split_colors(color_count,color_from,color_to)
            for i,point in enumerate(line):
                if (all(img[point[1], point[0]] ==fill_color)):
                    img[point[1], point[0]] = colors[i]
                if (all(img[point[1]+1, point[0]+1] ==fill_color)):
                    img[point[1]+1, point[0]+1] = colors[i]
                if (all(img[point[1]+1, point[0]][0] ==fill_color)):
                    img[point[1]+1, point[0]] = colors[i]
                if (all(img[point[1], point[0]+1] ==fill_color)):
                    img[point[1], point[0]+1] = colors[i]
                if (all(img[point[1]-1, point[0]-1] ==fill_color)):
                    img[point[1]-1, point[0]-1] = colors[i]
                if (all(img[point[1]-1, point[0]][0] ==fill_color)):
                    img[point[1]-1, point[0]] = colors[i]
                if (all(img[point[1], point[0]-1] ==fill_color)):
                    img[point[1], point[0]-1] = colors[i]
                if (all(img[point[1]-1, point[0]][0]+1 ==fill_color)):
                    img[point[1]-1, point[0]+1] = colors[i]
                if (all(img[point[1]+1, point[0]-1] ==fill_color)):
                    img[point[1]+1, point[0]-1] = colors[i]