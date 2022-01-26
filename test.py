import unittest
from textparser import *

class Tests(unittest.TestCase):

    def testCheckInputType(self):
        self.assertEqual(checkInputType('123456'), 'digits')
        self.assertEqual(checkInputType('abcdef'), 'word_characters')
        self.assertEqual(checkInputType('xy z'), 'word_characters')
        self.assertEqual(checkInputType('.'), 'others')
    
    def testCheckErrors(self):
        self.assertEqual(checkErrors('digits', 'digits', 2, 3, False), 'E01')
        self.assertEqual(checkErrors('digits', 'word_characters', 2, 2, False), 'E02')
        self.assertEqual(checkErrors('digits', 'digits', 5, 1, False), 'E03')
        self.assertEqual(checkErrors('digits', 'word_characters', 2, 1, False), 'E04')
        self.assertEqual(checkErrors('digits', 'digits', 2, 3, True), 'E05')
    
    def testGetContents(self):
        expectedOutput = ['L1&99&&A', 'L4&9']
        self.assertEqual(getContents('sample/input.txt'), expectedOutput)
    
    def testGetParsedData(self):
        expectedOutput = [
            ['L1', 'L11', 'digits', 'digits', 2, 1, 'E03'],
            ['L1', 'L12', '', 'word_characters', '', 3, 'E04'],
            ['L1', 'L13', 'word_characters', 'word_characters', 1, 2, 'E01'],
            ['L4', 'L41', 'digits', 'word_characters', 1, 1, 'E02'],
            ['L4', 'L42', '', 'digits', '', 6, 'E05']
        ]
        self.assertEqual(getParsedData('sample/input.txt'), expectedOutput)

    if __name__ == '__main__':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)