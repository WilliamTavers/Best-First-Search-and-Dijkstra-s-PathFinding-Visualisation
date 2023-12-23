import pygame
import math
from queue import PriorityQueue 
import heapq
import random 



colors = {
    "red": (255, 0, 0),
    "green": (0,255, 0),
    "white": (255,255,255), 
    "black": (0,0,0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "grey": (128, 128, 128), 
    "lgrey": (211,211,211),
    "turqoise": (64, 224, 208),
    "bblue": (0,191,255),
    "olive": (128,128,0)

}
width = 800
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("Dijkstra's PathFinding Algorithm")


class cell:
    def  __init__(self, row, col, width, total_rows): 
        self.row = row
        self.col = col 
        self.x = row * width 
        self.y = col * width 
        self.color = colors["white"]
        self.neighbours = []
        self.width = width 
        self.total_rows = total_rows
    
    
    def get_pos(self):
        return self.row, self.col 
    
    def is_closed(self):
        return self.color == colors['lgrey']
    
    def is_open(self):
        return self.color == colors['green']
    
    def is_wall(self):
        return self.color == colors['black']
    
    def wipe(self):
        self.color = colors['white']
    
    def close(self):
        self.color = colors['lgrey']
    
    def open(self):
        self.color = colors['green']
    
    def wall(self):
        self.color = colors['black']
    
    def start(self):
        self.color = colors['bblue']
    
    def end(self):
        self.color = colors['red']
    
    def path(self):
        self.color = colors['purple']
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def neighbours_update(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_wall():
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbours.append(grid[self.row][self.col - 1])
        
    def __lt__(self, other): ## less than
        return False
    
def heuristic(cell, end):
    x1, y1 = cell.get_pos()
    x2, y2 = end.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)


def dijkstra(draw, grid, start, end):
    count = 0
    pq = PriorityQueue()
    pq.put((0, count, start))
    came_from = {}
    distance = {cell: float("inf") for row in grid for cell in row}
    distance[start] = 0
    
    unvisited = {start} 
    
    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = pq.get()[2] # node lowest distance start node
        unvisited.remove(current)
        
        if current == end: 
            while current in came_from:
                current = came_from[current]
                current.path()
                draw()
            end.end()
            return True
        
        for neighbour in current.neighbours:
            temp_distance = distance[current]+1 
            
            if temp_distance < distance[neighbour]:
                came_from[neighbour] = current
                distance[neighbour] = temp_distance
                if neighbour not in unvisited:
                    count += 1
                    pq.put((distance[neighbour], count, neighbour))
                    unvisited.add(neighbour)
                    neighbour.open()
        draw()
        
        if current != start:
            current.close()
    return False


def best_first_search(draw, grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    distance = {cell: float("inf") for row in grid for cell in row}
    distance[start] = 0
    
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = heapq.heappop(open_set)[1] 
        
        if current == end: 
            while current in came_from:
                current = came_from[current]
                current.path()
                draw()
            end.end()
            return True

        for neighbour in current.neighbours: 
            temp_distance = heuristic(neighbour, end)
            
            if temp_distance < distance[neighbour]:
                came_from[neighbour] = current
                distance[neighbour] = temp_distance
                heapq.heappush(open_set, (distance[neighbour], neighbour))
                neighbour.open()
        
        draw()
        if current != start:
            current.close()
    
    return False
        
def create_grid(row, width):
    grid = []
    # distance = width // row 
    # return [[cell(i, j, distance, row) for j in range(row) for i in range(row)]]
    distance = width // row 
    
    for i in range(row):
        grid.append([])
        for j in range(row):
            cells = cell(i,j,distance, row)
            grid[i].append(cells)
    
    return grid

def render_grid(window, row, width):
    distance = width // row 
    for i in range(row):
        pygame.draw.line(window, colors['grey'], (0, i * distance), (width, i * distance)) # horiz
        pygame.draw.line(window, colors['grey'], (i*distance, 0), (i * distance, width)) # vert

def draw(window, grid, rows, width):
    window.fill(colors['white'])
    for row in grid:
        for cell in row:
            cell.draw(window)
    
    render_grid(window, rows, width)
    pygame.display.update()

def clicked_position(coordinate, row, width):
    distance = width // row
    y,x = coordinate
    grid_row = y // distance 
    grid_col = x // distance 
    
    return grid_row, grid_col 

def run(window, width):
    dimensions = 50
    grid = create_grid(dimensions, width)
    starting_cell = None 
    destination_cell = None 
    running = True 
    
    while running:
        draw(window, grid, dimensions, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
            if pygame.mouse.get_pressed()[0]: # left mouse
                position = pygame.mouse.get_pos()
                grid_row, grid_col = clicked_position(position, dimensions, width)
                cell = grid[grid_row][grid_col]
                
                if not starting_cell and cell != destination_cell:
                    starting_cell = cell 
                    starting_cell.start()
                
                elif not destination_cell and cell != starting_cell:
                    destination_cell = cell 
                    destination_cell.end() 
                
                elif cell != destination_cell and cell != starting_cell:
                    cell.wall()
                    
            elif pygame.mouse.get_pressed()[2]: # right mouse 
                position = pygame.mouse.get_pos()
                grid_row, grid_col = clicked_position(position, dimensions, width)
                cell = grid[grid_row][grid_col]
                cell.wipe()
                
                if cell == starting_cell:
                    starting_cell = None 
                elif cell == destination_cell:
                    destination_cell = None 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and starting_cell and destination_cell:
                    for row in grid:
                        for cell in row:
                            cell.neighbours_update(grid)
                    
                    dijkstra(lambda: draw(window, grid, dimensions, width), grid, starting_cell, destination_cell)
                
                elif event.key == pygame.K_b and starting_cell and destination_cell:
                    for row in grid:
                        for cell in row:
                            cell.neighbours_update(grid)
                    
                    best_first_search(lambda: draw(window, grid, dimensions, width), grid, starting_cell, destination_cell)
                
                elif event.key == pygame.K_r:
                    for row in grid: 
                        for cell in row: 
                            if cell!= starting_cell and cell != destination_cell:
                                cell.wipe()
                    
                    for row in grid: 
                        for cell in row:
                            if cell != starting_cell and cell != destination_cell:
                                if random.random() < 0.3:
                                    cell.wall()
                                
                if event.key == pygame.K_c:
                    starting_cell = None 
                    destination_cell = None 
                    grid = create_grid(dimensions, width)
                    

    pygame.quit()

run(window, width)