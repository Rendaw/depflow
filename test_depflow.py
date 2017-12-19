import unittest
import time
import logging
import depflow
from plumbum.cmd import cp, cat, touch, rm, echo


logging.basicConfig(level=logging.DEBUG)


@depflow.check
def const():
    return 'a', 'b'


class TestDepflow(unittest.TestCase):
    def setUp(self):
        self.df = depflow.Depflow('depflow-test')

    def tearDown(self):
        rm('a.txt', retcode=None)
        rm('a', retcode=None)
        rm('b', retcode=None)
        rm('c.txt', retcode=None)
        rm('c', retcode=None)
        rm('done', retcode=None)
        rm('.depflow-test.sqlite3', retcode=None)

    def flow(self):
        run = [False, False, False]

        @self.df.depends(depflow.file_hash('a.txt'))
        def process_a():
            cp('a.txt', 'a')
            run[0] = True

        @self.df.depends(depflow.nofile('b'))
        def process_b():
            touch('b')
            run[1] = True

        @self.df.depends(process_a, process_b, depflow.file_hash('c.txt'))
        def process_c():
            cp('c.txt', 'c')
            (cat['a', 'b', 'c'] > 'done')()
            run[2] = True

        return run[0], run[1], run[2]

    def test_missing_all(self):
        try:
            a, b, c = self.flow()
        except:  # noqa
            pass

    def test_missing_some(self):
        touch('a.txt')

        try:
            a, b, c = self.flow()
        except:  # noqa
            pass

    def test_complete(self):
        touch('a.txt')

        try:
            a, b, c = self.flow()
        except:  # noqa
            pass

        touch('c.txt')
        a, b, c = self.flow()
        self.assertFalse(a)
        self.assertFalse(b)
        self.assertTrue(c)

    def test_okay(self):
        touch('a.txt')
        touch('c.txt')

        a, b, c = self.flow()
        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)

    def test_no_work(self):
        touch('a.txt')
        touch('c.txt')

        self.flow()

        a, b, c = self.flow()
        self.assertFalse(a)
        self.assertFalse(b)
        self.assertFalse(c)

    def test_rebuild_a(self):
        touch('a.txt')
        touch('c.txt')

        self.flow()

        (echo['junk'] > 'a.txt')()
        a, b, c = self.flow()
        self.assertTrue(a)
        self.assertFalse(b)
        self.assertTrue(c)

    def test_no_rebuild_b(self):
        touch('a.txt')
        touch('c.txt')

        self.flow()

        touch('b')
        a, b, c = self.flow()
        self.assertFalse(a)
        self.assertFalse(b)
        self.assertFalse(c)

    def test_rebuild_b(self):
        touch('a.txt')
        touch('c.txt')

        self.flow()

        rm('b')
        a, b, c = self.flow()
        self.assertFalse(a)
        self.assertTrue(b)
        self.assertTrue(c)

    def test_timestamp_no_rebuild(self):
        touch('a.txt')

        run = [False]

        @self.df.depends(depflow.file('a.txt'))
        def update():
            run[0] = True
        self.assertTrue(run[0])

        run = [False]

        @self.df.depends(depflow.file('a.txt'))  # noqa
        def update():
            run[0] = True
        self.assertFalse(run[0])

    def test_timestamp_rebuild(self):
        touch('a.txt')

        @self.df.depends(depflow.file('a.txt'))
        def update():
            pass
        self.assertTrue(update)

        time.sleep(1)
        touch('a.txt')

        run = [False]

        @self.df.depends(depflow.file('a.txt'))
        def update():
            run[0] = True
        self.assertTrue(run[0])

    def test_unqualified_fail(self):
        dep = const()

        run = [False, False]
        for i in range(2):
            @self.df.depends(dep)
            def update():
                run[i] = True

        self.assertTrue(run[0])
        self.assertFalse(run[1])

    def test_scope(self):
        dep = const()

        run = [False, False]
        for i in range(2):
            scope = self.df.scope(i)

            @scope.depends(dep)
            def update():
                run[i] = True

        self.assertTrue(run[1])

    def test_qualify(self):
        dep = const()

        run = [False, False]
        for i in range(2):
            @self.df.depends(dep, qualification=(i,))
            def update():
                run[i] = True

        self.assertTrue(run[1])
