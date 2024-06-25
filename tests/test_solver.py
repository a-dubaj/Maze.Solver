import unittest
from unittest.mock import Mock, patch
import pygame

from solver import Window, Cell, Maze

class TestWindow(unittest.TestCase):
    def test_window_initialization(self):
        window = Window(10, 10, 20, 20)
        self.assertEqual(window.height, 200)
        self.assertEqual(window.width, 200)

class TestCell(unittest.TestCase):
    def setUp(self):
        self.win = Mock()
        self.cell = Cell(0, 0, 20, 20, self.win)
    
    def test_cell_initialization(self):
        self.assertEqual(self.cell.i, 0)
        self.assertEqual(self.cell.j, 0)
        self.assertEqual(self.cell.width, 20)
        self.assertEqual(self.cell.height, 20)
        self.assertFalse(self.cell.visited)
        self.assertEqual(len(self.cell.neighbors), 0)
    
    @patch('pygame.draw.rect')
    def test_paint_current_cell(self, mock_draw_rect):
        self.cell.paint_current_cell("blue")
        mock_draw_rect.assert_called_once()

    @patch('pygame.draw.line')
    @patch('pygame.draw.rect')
    def test_draw(self, mock_draw_rect, mock_draw_line):
        self.cell.visited = True
        self.cell.draw("red")
        self.assertEqual(mock_draw_rect.call_count, 1)
        self.assertEqual(mock_draw_line.call_count, 4)

class TestMaze(unittest.TestCase):
    def setUp(self):
        self.win = Mock()
        self.maze = Maze(10, 10, 20, 20, self.win)
    
    def test_maze_initialization(self):
        self.assertEqual(len(self.maze.cells), 10)
        self.assertEqual(len(self.maze.cells[0]), 10)
    
    def test_create_grid_array(self):
        self.maze._create_grid_array()
        self.assertEqual(len(self.maze.cells), self.maze.num_rows)
        self.assertEqual(len(self.maze.cells[0]), self.maze.num_cols)
        self.assertIsInstance(self.maze.cells[0][0], Cell)

    def test_set_neighbors(self):
        self.maze._create_grid_array()
        self.maze._set_neighbors()
        cell = self.maze.cells[0][0]
        self.assertEqual(len(cell.neighbors), 2)  # Top-left corner should have 2 neighbors
        cell = self.maze.cells[1][1]
        self.assertEqual(len(cell.neighbors), 4)  # Middle cell should have 4 neighbors

if __name__ == '__main__':
    unittest.main()
