from shapely.geometry import Polygon

# Class to describe the boundingboxes that are created as a result of OCR

class BoundingBox:
    

    def __init__(self, top, left, width, height, index_in_ocr_data):
        """
        Define the width and height of the boundingbox, as well as its top (vertical position of the top edge of the box), 
        left (horizontal position of the left edge of the boxtop), its middle point and its index in the OCR-Data
        """
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.middle_point = self.get_middle_point()
        self.index_in_ocr_data = index_in_ocr_data

    def get_middle_point(self):
        """ Get the middle point of the boundingbox """

        # Calculate the x value of the middle point 
        middle_point_x = self.left + 0.5 * self.width
        # Calculate the y value of the middle point 
        middle_point_y = self.top + 0.5 * self.height
        return middle_point_x, middle_point_y

    def is_comparison_boundingbox_inside_boundingbox(self, comparison_boundingbox):
        """ Check if another boundingbox (comparison_boundingbox) interects with the boundingbox """

        # Define the corner points of the source boundingbox
        left_top_corner_source_boundingbox = self.left, self.top
        right_top_corner_source_boundingbox = self.left + self.width, self.top
        left_bottom_corner_source_boundingbox = self.left, self.top + self.height
        right_bottom_corner_source_boundingbox = self.left + self.width, self.top + self.height
        
        # Create a polygon for the source boundingbox
        source_boundingbox_as_polygon = Polygon(
            [
                left_top_corner_source_boundingbox,
                right_top_corner_source_boundingbox,
                left_bottom_corner_source_boundingbox,
                right_bottom_corner_source_boundingbox,
            ]
        )

        # Define the corner points of the comparison boundingbox
        left_top_corner_comparison_boundingbox = (
            comparison_boundingbox.left,
            comparison_boundingbox.top,
        )
        right_top_corner_comparison_boundingbox = (
            comparison_boundingbox.left + comparison_boundingbox.width,
            comparison_boundingbox.top,
        )
        left_bottom_corner_comparison_boundingbox = (
            comparison_boundingbox.left,
            comparison_boundingbox.top + comparison_boundingbox.height,
        )
        right_bottom_corner_comparison_boundingbox = (
            comparison_boundingbox.left + comparison_boundingbox.width,
            comparison_boundingbox.top + comparison_boundingbox.height,
        )
        
        # Create a polygon for the comparison boundingbox
        comparison_boundingbox_as_polygon = Polygon(
            [
                left_top_corner_comparison_boundingbox,
                right_top_corner_comparison_boundingbox,
                left_bottom_corner_comparison_boundingbox,
                right_bottom_corner_comparison_boundingbox,
            ]
        )

        # Check if the comparison bounding box intersects the source bounding box
        return comparison_boundingbox_as_polygon.intersects(source_boundingbox_as_polygon)
