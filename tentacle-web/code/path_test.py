from path import Path
from db_manager import db_session
from node import Node
from level import Level
from user import User
import unittest

u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")

class TestPath(unittest.TestCase):
    def test_create_path(self):
        p = Path(db_session, u, "DESCRIPTION")
        self.assertEqual(p.user_id, u.id)
        
        p2 = db_session.query(Path).filter(Path.id == p.id).first()
        self.assertEqual(p2.id, p.id)

    def test_add_node(self):
        l = Level(db_session, u, b'')
        n = Node(db_session, l, u, "test")

        p = Path(db_session, u, "DESCRIPTION")
        p.add_node(n, db_session)

        seq = p.get_node_sequence(db_session)
        self.assertEqual(len(seq), 1)

        self.assertEqual(seq[0].node_id, n.id)

        # assert the following line raises an exception:
        with self.assertRaises(Exception):
            p.add_node(n, db_session)

    def test_add_node_to_two_diff_paths(self):
        l = Level(db_session, u, b'')
        n = Node(db_session, l, u, "test")

        p = Path(db_session, u, "DESCRIPTION")
        p.add_node(n, db_session)

        p2 = Path(db_session, u, "DESCRIPTION")
        p2.add_node(n, db_session)

        seq = p2.get_node_sequence(db_session)
        self.assertEqual(len(seq), 1)

        self.assertEqual(seq[0].node_id, n.id)

        seq = p.get_node_sequence(db_session)
        self.assertEqual(len(seq), 1)

        self.assertEqual(seq[0].node_id, n.id)

    def test_update_playcount(self):
        p = Path(db_session, u, "DESCRIPTION")
        p.update_playcount(db_session)

        self.assertEqual(p.get_playcount(), 1)

        playcount = db_session.query(Path).filter(Path.id == p.id).first().playcount
        self.assertEqual(playcount, 1)

    def test_update_rating(self):
        p = Path(db_session, u, "DESCRIPTION")
        p.update_rating(5, db_session)

        self.assertEqual(p.rating, 5)

        rating = db_session.query(Path).filter(Path.id == p.id).first().rating
        self.assertEqual(rating, 5)

        p.update_rating(10, db_session)
        self.assertEqual(p.rating, 7.5)

        rating = db_session.query(Path).filter(Path.id == p.id).first().rating
        self.assertEqual(rating, 7.5)


def main():
    unittest.main()

if __name__ == "__main__":
    main()