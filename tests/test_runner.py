"""Точка запуска всех тестов сразу"""


import unittest

from tests.test_ABSSorter import TestABSSorter
from tests.test_CommentItem import TestCommentItem
from tests.test_DataSorter import TestDataSorter
from tests.test_NewsItem import TestNewsItem
from tests.test_NewsItemResponse import TestNewsResponse
from tests.test_SpecificNewsDataSorter import TestSpecificNewsDataSorter
from tests.test_db_reader import TestMyShinyDBReader
from tests.test_env_setter import TestEnvSetter


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestABSSorter))
    test_suite.addTest(unittest.makeSuite(TestSpecificNewsDataSorter))
    test_suite.addTest(unittest.makeSuite(TestCommentItem))
    test_suite.addTest(unittest.makeSuite(TestDataSorter))
    test_suite.addTest(unittest.makeSuite(TestMyShinyDBReader))
    test_suite.addTest(unittest.makeSuite(TestEnvSetter))
    test_suite.addTest(unittest.makeSuite(TestNewsItem))
    test_suite.addTest(unittest.makeSuite(TestNewsResponse))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
