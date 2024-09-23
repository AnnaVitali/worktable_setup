class RectangleDrawer():

    def draw_rectangle(self, up_left_corner, bottom_right_corner, matrix, value, thickness=1):
        start_x, start_y = up_left_corner
        end_x, end_y = bottom_right_corner

        for i in range(thickness):
            # horizontal sides
            for x in range(start_x, end_x):
                matrix[start_y + i, x] = value
                matrix[end_y - i, x] = value

            # vertical sides
            for y in range(start_y, end_y):
                matrix[y, start_x + i] = value
                matrix[y, end_x - i] = value