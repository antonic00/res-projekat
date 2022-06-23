import socket
import unittest
from unittest.mock import patch, MagicMock
from unittest import mock

import description
import load_balancer
import broj_workera
class TestLoadBalancer(unittest.TestCase):

    @patch('broj_workera.Broj_Workera')
    def test_posalji_podatke_ok(self, mock_broj_workera):
        test_load_balancer = load_balancer.Load_Balancer()
        mock_socket1 = MagicMock(socket.socket)
        mock_socket2 = MagicMock(socket.socket)

        test_load_balancer.writer_socket = mock_socket1
        test_load_balancer.worker_socket = mock_socket2

        mock_broj = MagicMock(broj_workera.Broj_Workera)
        test_load_balancer.broj_workera = mock_broj
        mock_broj_workera.return_value = mock_broj


        with mock.patch('load_balancer.pickle.loads', side_effect=[["CODE_ANALOG",1], ["CODE_CUSTOM",1], ["CODE_SINGLENODE",1], ["CODE_CONSUMER",1], Exception]):
            assert load_balancer.Load_Balancer.posalji_podatke(test_load_balancer) == False

    @patch('broj_workera.Broj_Workera')
    def test_posalji_podatke_exit(self, mock_broj_workera):
        test_load_balancer = load_balancer.Load_Balancer()
        mock_socket1 = MagicMock(socket.socket)
        mock_socket2 = MagicMock(socket.socket)

        test_load_balancer.writer_socket = mock_socket1
        test_load_balancer.worker_socket = mock_socket2

        mock_broj = MagicMock(broj_workera.Broj_Workera)
        test_load_balancer.broj_workera = mock_broj
        mock_broj_workera.return_value = mock_broj

        with mock.patch('load_balancer.pickle.loads', side_effect=[ValueError, "exit", Exception]):
            assert load_balancer.Load_Balancer.posalji_podatke(test_load_balancer) == False

    @patch('broj_workera.Broj_Workera')
    def test_posalji_podatke_add(self, mock_broj_workera):
        test_load_balancer = load_balancer.Load_Balancer()
        mock_socket1 = MagicMock(socket.socket)
        mock_socket2 = MagicMock(socket.socket)

        test_load_balancer.writer_socket = mock_socket1
        test_load_balancer.worker_socket = mock_socket2

        mock_broj = MagicMock(broj_workera.Broj_Workera)
        test_load_balancer.broj_workera = mock_broj
        mock_broj_workera.return_value = mock_broj

        with mock.patch('load_balancer.pickle.loads', side_effect=[ValueError, "add", Exception]):
            assert load_balancer.Load_Balancer.posalji_podatke(test_load_balancer) == False

    @patch('broj_workera.Broj_Workera')
    def test_posalji_podatke_zaustavi(self, mock_broj_workera):
        test_load_balancer = load_balancer.Load_Balancer()
        mock_socket1 = MagicMock(socket.socket)
        mock_socket2 = MagicMock(socket.socket)

        test_load_balancer.writer_socket = mock_socket1
        test_load_balancer.worker_socket = mock_socket2

        mock_broj = MagicMock(broj_workera.Broj_Workera)
        test_load_balancer.broj_workera = mock_broj
        mock_broj_workera.return_value = mock_broj

        with mock.patch('load_balancer.pickle.loads', side_effect=[ValueError, "zaustavi", Exception]), mock.patch('load_balancer.pickle.dumps', side_effect=[description.Description(1, 1)]):
                assert load_balancer.Load_Balancer.posalji_podatke(test_load_balancer) == False

if __name__ == '__main__':
    unittest.main()
