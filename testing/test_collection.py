import pytest, py

from _pytest.main import Session

class Test_collection:
    def test_check_collect_foo(self, testdir):
        p = testdir.makepyfile("""
            import pytest
            
            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass
            
            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", "-f", "foo", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 2
        acceptable = ['test_baz', 'test_bar']
        for passd in passed:
            assert passd.nodeid.split('::')[1] in acceptable

    def test_check_collect_bar(self, testdir):
        p = testdir.makepyfile("""
            import pytest

            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass

            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", "-f", "bar", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 2
        acceptable = ['test_baz', 'test_foo']
        for passd in passed:
            assert passd.nodeid.split('::')[1] in acceptable
            
    def test_check_collect_foo_and_bar(self, testdir):
        p = testdir.makepyfile("""
            import pytest

            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass

            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", '-f', "foo bar", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1
        assert passed[0].nodeid.split('::')[1] == 'test_baz'
        
    def test_check_collect_foo_or_bar(self, testdir):
        p = testdir.makepyfile("""
            import pytest

            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass

            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", '-f', "foo", "-f", "bar", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 3
        acceptable = ['test_baz', 'test_foo', 'test_bar']
        for passd in passed:
            assert passd.nodeid.split('::')[1] in acceptable

    def test_check_collect_foo_but_not_bar(self, testdir):
        p = testdir.makepyfile("""
            import pytest

            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass

            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", '-f', "foo -bar", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1
        assert passed[0].nodeid.split('::')[1] == 'test_bar'
        
    def test_check_collect_foo_but_not_bar_as_or(self, testdir):
        p = testdir.makepyfile("""
            import pytest

            @pytest.mark.bar
            def test_foo():
                pass

            @pytest.mark.foo
            def test_bar():
                pass

            @pytest.mark.foo
            @pytest.mark.bar
            def test_baz():
                pass
        """)
        reprec = testdir.inline_run("-s", '-f', "foo", "-f", "-bar", p)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1
        assert passed[0].nodeid.split('::')[1] == 'test_bar'