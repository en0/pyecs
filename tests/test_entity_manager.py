from unittest import TestCase
from pyecs import EntityManager


class EntityManagerTests(TestCase):

    def setUp(self):
        self.manager = EntityManager({0b0111, 0b1100, 0b1001}, {"a", "b"})
        self.manager.activate_world("a")

    def test_worlds_are_different(self):
        e1 = {0b1000: "value_1000_e1"}
        e2 = {0b1000: "value_1000_e2"}

        self.manager.activate_world("a")
        e1_id = self.manager.spawn(e1)
        self.manager.activate_world("b")
        e2_id = self.manager.spawn(e2)

        with self.assertRaises(KeyError):
            self.manager.get_entity(e1_id)
        self.assertEqual(self.manager.get_entity(e2_id), e2)

        self.manager.activate_world("a")
        with self.assertRaises(KeyError):
            self.manager.get_entity(e2_id)
        self.assertEqual(self.manager.get_entity(e1_id), e1)

        self.manager.activate_world("a")
        self.manager.kill(e1_id)

        self.manager.activate_world("b")
        self.manager.kill(e2_id)

    def test_delete_entity(self):
        _id = self.manager.spawn({0b1000: "value"})
        self.manager.kill(_id)
        with self.assertRaises(KeyError):
            self.manager.get_entity(_id)

    def test_group_query(self):
        e1 = {0b1000: {"e1"}, 0b0100: {"e1"}, 0b0010: {"e1"}, 0b0001: {"e1"}}
        e2 = {0b1000: {"e2"}, 0b0100: {"e2"}}
        e3 = {0b0100: {"e3"}, 0b0010: {"e3"}, 0b0001: {"e3"}}
        e1_id = self.manager.spawn(e1)
        e2_id = self.manager.spawn(e2)
        e3_id = self.manager.spawn(e3)
        for a, e in zip(self.manager.get_entities(0b0111), [e1, e3]):
            self.assertEqual(a, e)

    def test_add_component(self):
        e = {0b0100: None, 0b0010: None}
        e_id = self.manager.spawn(e)
        self.assertListEqual(list(self.manager.get_entities(0b0111)), [])
        self.manager.add_component(e_id, 0b0001, None)
        self.assertListEqual(list(self.manager.get_entities(0b0111)), [e])

    def test_remove_component(self):
        e = {0b0100: None, 0b0010: None, 0b0001: None}
        e_id = self.manager.spawn(e)
        self.assertListEqual(list(self.manager.get_entities(0b0111)), [e])
        self.manager.remove_component(e_id, 0b0001)
        self.assertListEqual(list(self.manager.get_entities(0b0111)), [])

