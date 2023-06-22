from shapely.geometry import Polygon

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


    def is_comparison_boundingbox_inside_boundingbox(self, comparison_boundingbox):
        left_top_corner_source_boundingbox =  self.left, self.top
        right_top_corner_source_boundingbox = self.left+self.width, self.top
        left_bottom_corner_source_boundingbox = self.left, self.top+self.height
        right_bottom_corner_source_boundingbox = self.left+self.width, self.top+self.height
        source_boundingbox_as_polygon = Polygon([left_top_corner_source_boundingbox, right_top_corner_source_boundingbox, left_bottom_corner_source_boundingbox, right_bottom_corner_source_boundingbox])

        left_top_corner_comparison_boundingbox =  comparison_boundingbox.left, comparison_boundingbox.top
        right_top_corner_comparison_boundingbox = comparison_boundingbox.left+comparison_boundingbox.width, comparison_boundingbox.top
        left_bottom_corner_comparison_boundingbox = comparison_boundingbox.left, comparison_boundingbox.top+comparison_boundingbox.height
        right_bottom_corner_comparison_boundingbox = comparison_boundingbox.left+comparison_boundingbox.width, comparison_boundingbox.top+comparison_boundingbox.height
        comparison_boundingbox_as_polygon = Polygon([left_top_corner_comparison_boundingbox, right_top_corner_comparison_boundingbox, left_bottom_corner_comparison_boundingbox, right_bottom_corner_comparison_boundingbox])
        
        return comparison_boundingbox_as_polygon.intersects(source_boundingbox_as_polygon)