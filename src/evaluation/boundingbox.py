class BoundingBox:

    def __init__(self,top,left,width,height,index_in_ocr_data):
        self.top = top
        self.left =left
        self.width = width
        self.height = height
        self.middle_point = self.get_middle_point()
        self.index_in_ocr_data = index_in_ocr_data


    def get_middle_point(self):
        middle_point_x = self.left + 0.5 * self.width
        middle_point_y = self.top + 0.5 * self.height
        return middle_point_x,middle_point_y


    def is_point_inside_bounding_box(self,middlepoint:tuple):
        x = middlepoint[0]
        y = middlepoint[1]
        point_is_in_boundingbox = False
        if (
            x >=  self.left
            and x <=  (self.left + self.width)
            and y >=  self.top
            and y <=  (self.top +self.height)
        ):
            point_is_in_boundingbox = True
        return point_is_in_boundingbox