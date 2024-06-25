import pygame
import random

class Window:
    def __init__(self, num_rows, num_cols, cell_height, cell_width):
        self.height, self.width = (cell_height * num_rows, cell_width * num_cols)
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED)

class Cell:
    def __init__(self, i, j, width, height, win):
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.win = win
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.neighbors = []

    def paint_current_cell(self, color):
        x = self.j * self.width
        y = self.i * self.height
        pygame.draw.rect(self.win.window, pygame.Color(color), (x + 3, y + 3, self.width - 3, self.height - 3))

    def draw(self, visited_color):
        x = self.j * self.width
        y = self.i * self.height
        wall_color = "black"
        if self.visited:
            pygame.draw.rect(self.win.window, pygame.Color(visited_color), pygame.Rect(x, y, self.width, self.height))
        if self.walls["top"]:
            pygame.draw.line(self.win.window, pygame.Color(wall_color), (x, y), (x + self.width, y), 3)
        if self.walls["right"]:
            pygame.draw.line(self.win.window, pygame.Color(wall_color), (x + self.width, y), (x + self.width, y + self.height), 3)
        if self.walls["bottom"]:
            pygame.draw.line(self.win.window, pygame.Color(wall_color), (x + self.width, y + self.height), (x, y + self.height), 3)
        if self.walls["left"]:
            pygame.draw.line(self.win.window, pygame.Color(wall_color), (x, y + self.height), (x, y), 3)

class Maze:
    def __init__(self, num_rows, num_cols, cell_height, cell_width, window):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.win = window
        self.cells = []
        self._create_grid_array()
        self._set_neighbors()

    def solve(self, entry_cell, exit_cell, stack, backtrack_path):
        for row in self.cells:
            for cell in row:
                if cell in backtrack_path:
                    cell.draw("white")
                else:
                    cell.draw("green")
        self.paint_entry_and_exit(entry_cell, exit_cell)
        if stack:
            current = stack.pop()
            current.visited = True
            move_to_neighbor = False
            if current == exit_cell:
                current.draw("green")
                pygame.display.update()
                return True
            current.paint_current_cell("orange")
            neighbors = {
                "top": self.cells[current.i - 1][current.j] if current.i > 0 else None,
                "right": self.cells[current.i][current.j + 1] if current.j < self.num_cols - 1 else None,
                "bottom": self.cells[current.i + 1][current.j] if current.i < self.num_rows - 1 else None,
                "left": self.cells[current.i][current.j - 1] if current.j > 0 else None,
            }
            for direction, neighbor in neighbors.items():
                if neighbor and not current.walls[direction] and not neighbor.visited:
                    neighbor.visited = True
                    stack.append(current)
                    stack.append(neighbor)
                    move_to_neighbor = True
                    break
            if not move_to_neighbor:
                backtrack_path.append(current)
        pygame.display.update()
        return False

    def generate(self, entry_cell, exit_cell, stack):
        for row in self.cells:
            for cell in row:
                cell.draw("white")
        if stack:
            current = stack.pop()
            current.paint_current_cell("orange")
            self.paint_entry_and_exit(entry_cell, exit_cell)
            unvisited_neighbors = [neighbor for neighbor in current.neighbors if not neighbor.visited]
            if unvisited_neighbors:
                stack.append(current)
                neighbor = random.choice(unvisited_neighbors)
                self.break_walls(current, neighbor)
                neighbor.visited = True
                stack.append(neighbor)
        pygame.display.update()

    def paint_entry_and_exit(self, entry_cell, exit_cell):
        if entry_cell is None or exit_cell is None:
            return -1
        pygame.draw.rect(
            self.win.window,
            pygame.Color("green"),
            pygame.Rect(
                (entry_cell.i * entry_cell.height) + 2,
                (entry_cell.j * entry_cell.width) + 2,
                entry_cell.width - 3,
                entry_cell.height - 3,
            ),
        )
        pygame.draw.rect(
            self.win.window,
            pygame.Color("green"),
            pygame.Rect(
                (exit_cell.i * exit_cell.height) + 2,
                (exit_cell.j * exit_cell.width) + 2,
                exit_cell.width - 3,
                exit_cell.height - 3,
            ),
        )

    def break_walls(self, current, neighbor):
        dy = current.i - neighbor.i
        dx = current.j - neighbor.j
        if dy == -1:
            current.walls["bottom"] = False
            neighbor.walls["top"] = False
        elif dy == 1:
            current.walls["top"] = False
            neighbor.walls["bottom"] = False
        if dx == -1:
            current.walls["right"] = False
            neighbor.walls["left"] = False
        elif dx == 1:
            current.walls["left"] = False
            neighbor.walls["right"] = False

    def _create_grid_array(self):
        self.cells = []  # Clear cells list to prevent double initialization
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                cell = Cell(i, j, self.cell_height, self.cell_width, self.win)
                row.append(cell)
            self.cells.append(row)

    def _set_neighbors(self):
        for row in self.cells:
            for cell in row:
                if cell.i > 0:
                    cell.neighbors.append(self.cells[cell.i - 1][cell.j])
                if cell.i < self.num_rows - 1:
                    cell.neighbors.append(self.cells[cell.i + 1][cell.j])
                if cell.j > 0:
                    cell.neighbors.append(self.cells[cell.i][cell.j - 1])
                if cell.j < self.num_cols - 1:
                    cell.neighbors.append(self.cells[cell.i][cell.j + 1])

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    cell_height, cell_width = 20, 20
    num_rows, num_cols = 30, 30
    win = Window(num_rows, num_cols, cell_height, cell_width)
    maze = Maze(num_rows, num_cols, cell_height, cell_width, win)
    is_maze_generated = False
    is_maze_solved = False
    entry_cell = maze.cells[0][0]
    exit_cell = maze.cells[num_rows - 1][num_cols - 1]
    stack = []
    current = entry_cell
    current.visited = True
    stack.append(current)
    backtrack_path = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if is_maze_generated:
            if not is_maze_solved:
                is_maze_solved = maze.solve(entry_cell, exit_cell, stack, backtrack_path)
            else:
                is_maze_solved = True
        else:
            win.window.fill(pygame.Color("black"))
            maze.generate(entry_cell, exit_cell, stack)
            if not stack:
                is_maze_generated = True
                stack.append(entry_cell)
                for row in maze.cells:
                    for cell in row:
                        cell.visited = False
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
