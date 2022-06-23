import socket
import unittest
from unittest.mock import patch, MagicMock
import writer


class TestWriter(unittest.TestCase):

    @patch('writer.socket')
    def test_konektuj_sa_load_balancerom_ok(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        test_writer.writer_soket = mock_socket
        self.assertEqual(True, writer.Writer.konektuj_sa_load_balancerom(test_writer))

    @patch('writer.socket')
    def test_konektuj_sa_load_balancerom_error(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        mock_socket.side_effect = Exception
        test_writer.writer_soket = mock_socket.side_effect
        self.assertEqual(False, writer.Writer.konektuj_sa_load_balancerom(test_writer))

    @patch('writer.socket')
    def test_inicijalizacija_paljenja_ok(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        test_writer.writer_soket = mock_socket
        self.assertEqual(None, writer.Writer.inicijalizacija_paljenja(test_writer))

    @patch('writer.socket')
    def test_inicijalizacija_gasenja_ok(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        test_writer.writer_soket = mock_socket
        self.assertEqual(None, writer.Writer.inicijalizacija_gasenja(test_writer))

    @patch('writer.socket')
    def test_main_ok(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        test_writer.konektuj_sa_load_balancerom = mock_socket
        self.assertEqual(None, writer.Writer.main(test_writer))

    @patch('writer.socket')
    def test_posalji_podatke(self, mock_socket_s):
        test_writer = writer.Writer()
        mock_socket = MagicMock(socket.socket)
        mock_socket_s.return_value = mock_socket
        test_writer.writer_soket = mock_socket

        self.assertEqual(None, writer.Writer.posalji_podatke(test_writer))



if __name__ == '__main__':
    unittest.main()
