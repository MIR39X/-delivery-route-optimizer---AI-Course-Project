import unittest

from src.models.grid import Grid
from src.pathfinding.astar import astar, multi_route
from src.utils.constants import START, DELIVERY, OBSTACLE, WEIGHT


class TestAstar(unittest.TestCase):
    def test_empty_grid(self):
        grid = Grid(5, 5)
        result = astar(grid, (0, 0), (0, 4))
        self.assertTrue(result["found"])
        self.assertEqual(result["cost"], 4)
        self.assertEqual(result["path"][0], (0, 0))
        self.assertEqual(result["path"][-1], (0, 4))

    def test_obstacle_route(self):
        grid = Grid(5, 5)
        grid.set_cell((0, 1), OBSTACLE)
        grid.set_cell((1, 1), OBSTACLE)
        result = astar(grid, (0, 0), (0, 2))
        self.assertTrue(result["found"])
        self.assertNotIn((0, 1), result["path"])

    def test_no_path(self):
        grid = Grid(3, 3)
        grid.set_cell((0, 1), OBSTACLE)
        grid.set_cell((1, 0), OBSTACLE)
        result = astar(grid, (0, 0), (2, 2))
        self.assertFalse(result["found"])

    def test_weight_cost(self):
        grid = Grid(3, 5)
        grid.set_cell((0, 1), WEIGHT)
        result = astar(grid, (0, 0), (0, 2))
        self.assertTrue(result["found"])
        self.assertLessEqual(result["cost"], 4)

    def test_multi_route(self):
        grid = Grid(5, 5)
        grid.set_cell((0, 0), START)
        grid.set_cell((0, 4), DELIVERY)
        grid.set_cell((4, 4), DELIVERY)
        result = multi_route(grid)
        self.assertTrue(result["found"])
        self.assertEqual(len(result["order"]), 2)
        self.assertEqual(result["path"][0], (0, 0))

    def test_euclidean_heuristic(self):
        grid = Grid(6, 6)
        result = astar(grid, (0, 0), (5, 5), "euclidean")
        self.assertTrue(result["found"])
        self.assertEqual(result["cost"], 10)

    def test_local_search_result_is_not_worse(self):
        grid = Grid(10, 10)
        grid.set_cell((0, 0), START)
        grid.set_cell((0, 9), DELIVERY)
        grid.set_cell((9, 9), DELIVERY)
        grid.set_cell((9, 0), DELIVERY)
        result = multi_route(grid)
        self.assertTrue(result["found"])
        self.assertLessEqual(result["cost"], result["nearest_cost"])
        self.assertEqual(result["saved_cost"], result["nearest_cost"] - result["cost"])

    def test_road_cells_block_houses(self):
        grid = Grid(4, 4)
        roads = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
        grid.set_road_cells(roads)
        result = astar(grid, (0, 0), (2, 2))
        self.assertTrue(result["found"])
        self.assertEqual(result["path"], [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])


if __name__ == "__main__":
    unittest.main()
