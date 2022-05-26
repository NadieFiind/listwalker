import sys
import unittest
sys.path.append("..")

from src.listwalker import (  # noqa E402
	ListWalker1D, ListWalker2D, ListWalkerElement, CannotMoveException
)

walker1D = ListWalker1D[int]([1, 2, 3, 4, 5])
walker1D.ignored_elements.append(2)
walker1D.ignored_elements.append(3)
walker1D.move_right()
walker1D.move_right()

walker2D_ignored = [[1, 0], [2, 0], [3, 0], [0, 3]]
walker2D = ListWalker2D[int]([
	[1, 2, 3, 4, 5],
	[6, 7, 8, 9, 10],
	[11, 12, 13, 14, 15],
	[16, 17, 18, 19, 20],
	[21, 22, 23, 24, 25],
	[26, 27, 28, 29, 30]
])
walker2D.ignored_elements = walker2D_ignored
walker2D.move_down()


class TestListWalker1D(unittest.TestCase):
	
	def test_size(self) -> None:
		self.assertEqual(walker1D.size, 5)
	
	def test_cursor_element(self) -> None:
		self.assertEqual(walker1D.cursor_element.position, 4)
	
	def test_is_ignored(self) -> None:
		self.assertFalse(walker1D.get(0).is_ignored)
		self.assertFalse(walker1D.get(1).is_ignored)
		self.assertTrue(walker1D.get(2).is_ignored)
		self.assertTrue(walker1D.get(3).is_ignored)
		self.assertFalse(walker1D.get(4).is_ignored)
	
	def test_get(self) -> None:
		for position in range(walker1D.size):
			element = walker1D.get(position)
			self.assertIsInstance(element, ListWalkerElement)
			self.assertEqual(element.position, position)
			self.assertEqual(element.value, position + 1)
			self.assertEqual(element.walker, walker1D)
	
	def test_get_left(self) -> None:
		self.assertEqual(walker1D.get_left().value, 4)
	
	def test_get_right(self) -> None:
		self.assertRaises(IndexError, walker1D.get_right)
	
	def test_get_neighbors(self) -> None:
		neighbors = walker1D.get_neighbors()
		self.assertTrue(neighbors.get("left"))
		self.assertFalse(neighbors.get("right"))
	
	def test_move_left(self) -> None:
		walker1D.cursor = walker1D.size - 1
		self.assertRaises(CannotMoveException, walker1D.move_left, jump=False)
		
		walker1D.move_left(jump=False, silent=True)
		self.assertEqual(walker1D.cursor_element.value, 5)
		
		walker1D.move_left()
		self.assertEqual(walker1D.cursor_element.value, 2)
		
		walker1D.move_left()
		self.assertEqual(walker1D.cursor_element.value, 1)
		
		walker1D.move_left(silent=True)
		self.assertEqual(walker1D.cursor_element.value, 1)
		
		self.assertRaises(IndexError, walker1D.move_left)
	
	def test_move_right(self) -> None:
		walker1D.cursor = 0
		
		walker1D.move_right()
		self.assertEqual(walker1D.cursor_element.value, 2)
		
		self.assertRaises(CannotMoveException, walker1D.move_right, jump=False)
		
		walker1D.move_right(jump=False, silent=True)
		self.assertEqual(walker1D.cursor_element.value, 2)
		
		walker1D.move_right()
		self.assertEqual(walker1D.cursor_element.value, 5)
		
		walker1D.move_right(silent=True)
		self.assertEqual(walker1D.cursor_element.value, 5)
		
		self.assertRaises(IndexError, walker1D.move_right)


class TestListWalker2D(unittest.TestCase):
	
	def test_size(self) -> None:
		self.assertEqual(walker2D.size, [6, 5])
	
	def test_cursor_element(self) -> None:
		self.assertEqual(walker2D.cursor_element.position, [4, 0])
	
	def test_is_ignored(self) -> None:
		for rowpos, row_element in enumerate(walker2D.data):
			for colpos, col_element in enumerate(row_element):
				position = [rowpos, colpos]
				element = walker2D.get(position)
				
				if position in walker2D_ignored:
					self.assertTrue(element.is_ignored)
				else:
					self.assertFalse(element.is_ignored)
	
	def test_get(self) -> None:
		for rowpos, row_element in enumerate(walker2D.data):
			for colpos, col_element in enumerate(row_element):
				position = [rowpos, colpos]
				element = walker2D.get(position)
				
				self.assertIsInstance(element, ListWalkerElement)
				self.assertEqual(element.position, position)
				self.assertEqual(element.value, 5 * position[0] + position[1] + 1)
				self.assertEqual(element.walker, walker2D)
	
	def test_get_up(self) -> None:
		self.assertEqual(walker2D.get_up().value, 16)
	
	def test_get_right(self) -> None:
		self.assertEqual(walker2D.get_right().value, 22)
	
	def test_get_down(self) -> None:
		self.assertEqual(walker2D.get_down().value, 26)
	
	def test_get_left(self) -> None:
		self.assertRaises(IndexError, walker2D.get_left)
	
	def test_get_neighbors(self) -> None:
		neighbors = walker2D.get_neighbors()
		self.assertTrue(neighbors.get("up"))
		self.assertTrue(neighbors.get("right"))
		self.assertTrue(neighbors.get("down"))
		self.assertFalse(neighbors.get("left"))
	
	def test_move_up(self) -> None:
		walker2D.cursor = [4, 0]
		self.assertRaises(CannotMoveException, walker2D.move_up, jump=False)
		
		walker2D.move_up(jump=False, silent=True)
		self.assertEqual(walker2D.cursor_element.value, 21)
		
		walker2D.move_up()
		self.assertEqual(walker2D.cursor_element.value, 1)
		
		walker2D.move_up(silent=True)
		self.assertEqual(walker2D.cursor_element.value, 1)
		
		self.assertRaises(IndexError, walker2D.move_up)
	
	def test_move_right(self) -> None:
		walker2D.cursor = [0, 0]
		
		walker2D.move_right()
		self.assertEqual(walker2D.cursor_element.value, 2)
		
		walker2D.move_right()
		self.assertEqual(walker2D.cursor_element.value, 3)
		
		self.assertRaises(CannotMoveException, walker2D.move_right, jump=False)
		
		walker2D.move_right(jump=False, silent=True)
		self.assertEqual(walker2D.cursor_element.value, 3)
		
		walker2D.move_right()
		self.assertEqual(walker2D.cursor_element.value, 5)
		
		walker2D.move_right(silent=True)
		self.assertEqual(walker2D.cursor_element.value, 5)
		
		self.assertRaises(IndexError, walker2D.move_right)
	
	def test_move_down(self) -> None:
		walker2D.cursor = [0, 0]
		self.assertRaises(CannotMoveException, walker2D.move_down, jump=False)
		
		walker2D.move_down(jump=False, silent=True)
		self.assertEqual(walker2D.cursor_element.value, 1)
		
		walker2D.move_down()
		self.assertEqual(walker2D.cursor_element.value, 21)
		
		walker2D.move_down()
		self.assertEqual(walker2D.cursor_element.value, 26)
		
		walker2D.move_down(silent=True)
		self.assertEqual(walker2D.cursor_element.value, 26)
		
		self.assertRaises(IndexError, walker2D.move_down)
	
	def test_move_left(self) -> None:
		walker2D.cursor = [0, 4]
		self.assertRaises(CannotMoveException, walker2D.move_left, jump=False)
		
		walker2D.move_left(jump=False, silent=True)
		self.assertEqual(walker2D.cursor_element.value, 5)
		
		walker2D.move_left()
		self.assertEqual(walker2D.cursor_element.value, 3)
		
		walker2D.move_left()
		self.assertEqual(walker2D.cursor_element.value, 2)
		
		walker2D.move_left()
		self.assertEqual(walker2D.cursor_element.value, 1)
		
		walker2D.move_left(silent=True)
		self.assertEqual(walker2D.cursor_element.value, 1)
		
		self.assertRaises(IndexError, walker2D.move_left)


if __name__ == "__main__":
	unittest.main()
