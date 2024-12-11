#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json 
from unittest.mock import patch, Mock
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises a KeyError for invalid paths.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])


    class TestGetJson(unittest.TestCase):
        @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    '''@patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
            """
            Test that the get_json function returns the expected result
            without making actual external HTTP calls.
            """
            # Create a Mock object for the response
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call get_json with the test_url
            result = get_json(test_url)

            # Ensure that requests.get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Assert that the result returned from get_json is the same as the mock_payload
            self.assertEqual(result, test_payload)
'''
class TestMemoize(unittest.TestCase):
    """
    Unit test class to test the memoization functionality of the 'memoize' decorator.
    """

    @patch("path_to_your_module.TestClass.a_method")  # Correct path to the method being patched
    def test_memoize(self, mock_method):
        """
        Test that the memoize decorator caches the result and calls the method only once.

        This method creates a class with a memoized property, then calls the property twice to
        ensure the method is only called once. The test ensures that the value returned by the
        property is cached correctly and the method is not repeatedly called.
        
        Args:
            mock_method (Mock): The mocked version of the 'a_method' in TestClass.
        
        Asserts:
            - The 'a_method' is called only once.
            - The result of the memoized property is consistent across calls.
            - The result of the property matches the expected value (42 in this case).
        """
        # Define the class with the method and property
        class TestClass:
            def a_method(self):
                """
                A simple method that returns a fixed value of 42.
                
                This method is patched in the test to avoid actual execution.
                
                Returns:
                    int: The value 42.
                """
                return 42  # This should be the mocked method

            @memoize  # Apply memoize decorator
            def a_property(self):
                """
                A property that is memoized using the 'memoize' decorator.
                
                The first call to this property will compute the result, and subsequent calls 
                will return the cached value without calling the underlying method.
                
                Returns:
                    int: The result of calling a_method (which is 42).
                """
                return self.a_method()

        # Create an instance of the TestClass
        test_instance = TestClass()

        # Mock the a_method to return a specific value
        mock_method.return_value = 42

        # Call a_property twice
        result_first_call = test_instance.a_property
        result_second_call = test_instance.a_property

        # Assert that a_method was only called once
        mock_method.assert_called_once()

        # Assert that the result of both calls is the same (memoized result)
        self.assertEqual(result_first_call, result_second_call)
        self.assertEqual(result_first_call, 42)  

if __name__ == "__main__":
    unittest.main()
