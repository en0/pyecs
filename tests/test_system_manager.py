from unittest import TestCase
from unittest.mock import Mock
from pyecs import SystemManager
from pyecs.typing import ISystem


class SystemManagerTests(TestCase):

    def setUp(self):
        self.manager = SystemManager()

    def test_update_called(self):
        m_spec = Mock(spec=ISystem)
        m1 = m_spec()
        self.manager.install(m1)
        self.manager.update()
        m1.update.assert_called_once()

    def test_update_not_called_if_disabled(self):
        m_spec = Mock(spec=ISystem)
        m1 = m_spec()
        self.manager.install(m1, False)
        self.manager.update()
        m1.update.assert_not_called()

    def test_update_not_called_if_disabled(self):
        m_spec = Mock(spec=ISystem)
        m1 = m_spec()
        self.manager.install(m1, False)
        self.manager.update()
        m1.update.assert_not_called()

    def test_update_not_called_if_disabled_from_enabled(self):
        m_spec = Mock(spec=ISystem)
        m1 = m_spec()
        self.manager.install(m1)
        self.manager.update()
        m1.update.assert_called_once()
        m1.reset_mock()
        self.manager.disable(type(m1))
        self.manager.update()
        m1.update.assert_not_called()

    def test_update_called_if_enabled_from_disabled(self):
        m_spec = Mock(spec=ISystem)
        m1 = m_spec()
        self.manager.install(m1, False)
        self.manager.update()
        m1.update.assert_not_called()
        m1.reset_mock()
        self.manager.enable(type(m1))
        self.manager.update()
        m1.update.assert_called_once()

