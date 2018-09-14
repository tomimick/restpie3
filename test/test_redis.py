#!/usr/bin/python
# -*- coding: utf-8 -*-

# test_redis.py: test red.py, the Redis storage
#
# Author: Tomi.Mickelsson@iki.fi

import unittest
import time

import red

class Tests(unittest.TestCase):

    def test_keyval(self):
        VAL = "a1"
        red.set_keyval("k1", VAL)
        val = red.get_keyval("k1")
        self.assertEqual(VAL, val)

        VAL = {"some":1, "thing":[1,2,"3"]}
        red.set_keyval("k1", VAL)
        val = red.get_keyval("k1")
        self.assertEqual(VAL, val)

        red.delete_key("k1")
        val = red.get_keyval("k1")
        self.assertEqual(None, val)

        val = red.get_keyval("qwerty")
        self.assertEqual(None, val)

        val = red.get_keyval("qwerty", "mydefault")
        self.assertEqual("mydefault", val)

    def test_keyval_expir(self):
        red.delete_key("k1")
        val = red.get_keyval("k1")
        self.assertEqual(None, val)

        red.set_keyval("k1", 99, 1)
        val = red.get_keyval("k1")
        self.assertEqual(99, val)
        time.sleep(1.1)
        val = red.get_keyval("k1")
        self.assertEqual(None, val)

    def test_list(self):
        red.delete_key("mylist")
        self.assertEqual(0, red.list_length("mylist"))

        VAL = {"foo":1, "bar":[1,2]}
        red.list_append("mylist", VAL)
        self.assertEqual(1, red.list_length("mylist"))

        red.list_append("mylist", "apple")
        self.assertEqual(2, red.list_length("mylist"))

        self.assertEqual(VAL, red.list_peek("mylist"))

        curlist = red.list_fetch("mylist")
        self.assertEqual(2, len(curlist))
        self.assertEqual("apple", curlist[1])

        self.assertEqual(VAL, red.list_pop("mylist"))
        self.assertEqual(1, red.list_length("mylist"))
        self.assertEqual("apple", red.list_pop("mylist"))
        self.assertEqual(0, red.list_length("mylist"))

    def test_list_maxsize(self):
        red.delete_key("mylist")
        self.assertEqual(0, red.list_length("mylist"))

        red.list_append("mylist", "abc", 3)
        self.assertEqual(1, red.list_length("mylist"))
        self.assertEqual("abc", red.list_peek("mylist"))
        red.list_append("mylist", "123", 3)
        self.assertEqual(2, red.list_length("mylist"))
        self.assertEqual("abc", red.list_peek("mylist"))
        red.list_append("mylist", "def", 3)
        self.assertEqual(3, red.list_length("mylist"))
        self.assertEqual("abc", red.list_peek("mylist"))
        red.list_append("mylist", "456", 3)
        self.assertEqual(3, red.list_length("mylist"))
        self.assertEqual("123", red.list_peek("mylist"))

    def test_incr(self):
        red.delete_key("counter")

        self.assertEqual(1, red.incr("counter"))
        self.assertEqual(2, red.incr("counter"))
        self.assertEqual(5, red.incr("counter", 3))

    def test_getset(self):
        red.delete_key("foo")

        self.assertEqual(None, red.get_set("foo", "orange"))
        self.assertEqual("orange", red.get_set("foo", "banana"))
        self.assertEqual("banana", red.get_set("foo", "blackberry"))


if __name__ == '__main__':
    unittest.main()

