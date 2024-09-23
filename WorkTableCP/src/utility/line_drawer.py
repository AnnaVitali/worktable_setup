class LineDrawer():

    def draw_line(self, start_point, end_point, matrix, value):
        start_x, start_y = start_point
        end_x, end_y = end_point

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        sx = -1 if start_x > end_x else 1
        sy = -1 if start_y > end_y else 1

        x, y = start_x, start_y
        matrix[y][x] = value

        if dx > dy:
            err = dx / 2.0
            while x != end_x:
                matrix[y][x] = value
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != end_y:
                matrix[y][x] = value
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def draw_thick_line(self, start_point, end_point, matrix, value, thickness, thickness_direction):
        start_x, start_y = start_point
        end_x, end_y = end_point
        max_y, max_x = matrix.shape

        match thickness_direction:
            case "down":
                for i in range(thickness):
                    y1 = max(start_y - i, 0)
                    y2 = max(end_y - i, 0)
                    self.draw_line((start_x, y1), (end_x, y2), matrix, value)

            case "up":
                for i in range(thickness):
                    y1 = min(start_y + i, max_y - 1)
                    y2 = min(end_y + i, max_y - 1)
                    self.draw_line((start_x, y1), (end_x, y2), matrix, value)
            case "left":
                for i in range(thickness):
                    x1 = max(start_x - i, 0)
                    x2 = max(end_x - i, 0)
                    self.draw_line((x1, start_y), (x2, end_y), matrix, value)
            case "right":
                for i in range(thickness):
                    x1 = min(start_x + i, max_x - 1)
                    x2 = min(end_x + i, max_x - 1)
                    self.draw_line((x1, start_y), (x2, end_y), matrix, value)