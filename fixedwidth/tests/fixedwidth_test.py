#!/usr/bin/env python

"""
Tests for the FixedWidth class.
"""

import unittest
from datetime import datetime
from copy import deepcopy

from ..fixedwidth import FixedWidth

SAMPLE_CONFIG = {

    "first_name": {
        "required": True,
        "type": "string",
        "start_pos": 1,
        "end_pos": 10,
        "alignment": "left",
        "padding": " "
    },

    "last_name": {
        "required": True,
        "type": "string",
        "start_pos": 11,
        "end_pos": 30,
        "alignment": "left",
        "padding": " "
    },

    "nickname": {
        "required": False,
        "type": "string",
        "start_pos": 31,
        "length": 15,
        "alignment": "left",
        "padding": " "
    },

    "age": {
        "type": "integer",
        "alignment": "right",
        "start_pos": 46,
        "padding": "0",
        "length": 3,
        "required": True
    },

    "meal": {
        "type": "string",
        "start_pos": 49,
        "default": "no preference",
        "padding": " ",
        "end_pos": 68,
        "length": 20,
        "alignment": "left",
        "required": False
    }

}


class TestFixedWidth(unittest.TestCase):
    """
    Test of the FixedWidth class.
    """

    def test_basic(self):
        """
        Test a simple, valid example.
        """

        fw_config = deepcopy(SAMPLE_CONFIG)
        fw_obj = FixedWidth(fw_config)
        fw_obj.update(
            last_name="Smith", first_name="Michael",
            age=32, meal="vegetarian"
        )

        fw_string = fw_obj.line

        good = (
            "Michael   Smith                              "
            "032vegetarian          \r\n"
        )

        self.assertEquals(fw_string, good)

    def test_update(self):
        """
        Test FixedWidth.update()
        """

        fw_config = deepcopy(SAMPLE_CONFIG)
        fw_obj = FixedWidth(fw_config)

        fw_obj.update(
            last_name="Smith", first_name="Michael",
            age=32, meal="vegetarian"
        )

        #change a value
        fw_obj.update(meal="Paleo")
        self.assertEquals(fw_obj.data["meal"], "Paleo")

        #nothing else should have changed
        self.assertEquals(fw_obj.data["first_name"], "Michael")

    def test_fw_to_dict(self):
        """
        Pass in a line and receive dictionary.
        """

        fw_config = deepcopy(SAMPLE_CONFIG)

        fw_obj = FixedWidth(fw_config)
        fw_obj.line = (
            "Michael   Smith                              "
            "032vegetarian          "
        )

        values = fw_obj.data
        self.assertEquals(values["first_name"], "Michael")
        self.assertEquals(values["last_name"], "Smith")
        self.assertEquals(values["age"], 32)
        self.assertEquals(values["meal"], "vegetarian")

    def test_datetime_formatting_to_string(self):
        # Given a default date spec,
        fw_config = deepcopy(SAMPLE_CONFIG)
        fw_config['dob'] = {
            'required': True,
            'type': "datetime",
            'start_pos': 69,
            'length': 27,
            'alignment': 'right',
            'padding': ' '
        }

        # and some sample data,
        test_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 42,
            'meal': 'omnivore',
            'dob': datetime(year=1985, month=12, day=1, hour=7, minute=55,
                            second=23, microsecond=123456),
        }

        # when we generate a line based on the spec,
        fw_obj = FixedWidth(fw_config, **test_data)
        result = fw_obj.line

        # then the line includes the default formatted date.
        expected = 'John      Doe                                042omnivore' \
                   '             1985-12-01T07:55:23.123456\r\n'
        self.assertEqual(result, expected)

# TODO formatting to dict
# TODO formatting with timezone offset
# TODO formatting with default or required/value
