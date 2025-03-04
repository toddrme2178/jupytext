# -*- coding: utf-8 -*-

from nbformat.v4.nbbase import new_markdown_cell, new_code_cell, new_notebook
from jupytext.compare import compare
import jupytext
from jupytext.compare import compare_notebooks


def test_read_simple_file(pynb="""# ---
# title: Simple file
# ---

# Here we have some text
# And below we have some python code

def f(x):
    return x+1


def h(y):
    return y-1
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 4
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == '---\ntitle: Simple file\n---'
    assert nb.cells[1].cell_type == 'markdown'
    assert nb.cells[1].source == 'Here we have some text\n' \
                                 'And below we have some python code'
    assert nb.cells[2].cell_type == 'code'
    compare(nb.cells[2].source, '''def f(x):
    return x+1''')
    assert nb.cells[3].cell_type == 'code'
    compare(nb.cells[3].source, '''def h(y):
    return y-1''')

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_less_simple_file(pynb="""# ---
# title: Less simple file
# ---

# Here we have some text
# And below we have some python code

# This is a comment about function f
def f(x):
    return x+1


# And a comment on h
def h(y):
    return y-1
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 4
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == '---\ntitle: Less simple file\n---'
    assert nb.cells[1].cell_type == 'markdown'
    assert nb.cells[1].source == 'Here we have some text\n' \
                                 'And below we have some python code'
    assert nb.cells[2].cell_type == 'code'
    compare(nb.cells[2].source,
            '# This is a comment about function f\n'
            'def f(x):\n'
            '    return x+1')
    assert nb.cells[3].cell_type == 'code'
    compare(nb.cells[3].source,
            '''# And a comment on h\ndef h(y):\n    return y-1''')

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_non_pep8_file(pynb="""# ---
# title: Non-pep8 file
# ---

# This file is non-pep8 as the function below has
# two consecutive blank lines in its body

def f(x):


    return x+1
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 3
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == '---\ntitle: Non-pep8 file\n---'
    assert nb.cells[1].cell_type == 'markdown'
    assert nb.cells[1].source == 'This file is non-pep8 as ' \
                                 'the function below has\n' \
                                 'two consecutive blank lines ' \
                                 'in its body'
    assert nb.cells[2].cell_type == 'code'
    compare(nb.cells[2].source,
            'def f(x):\n\n\n'
            '    return x+1')

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_cell_two_blank_lines(pynb="""# ---
# title: cell with two consecutive blank lines
# ---

# +
a = 1


a + 2
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == '---\ntitle: cell with two ' \
                                 'consecutive blank lines\n---'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[1].source == 'a = 1\n\n\na + 2'

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_cell_explicit_start(pynb='''
import pandas as pd
# + {}
def data():
    return pd.DataFrame({'A': [0, 1]})


data()
'''):
    nb = jupytext.reads(pynb, 'py')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_complex_cells(pynb='''import pandas as pd

# +
def data():
    return pd.DataFrame({'A': [0, 1]})


data()

# +
def data2():
    return pd.DataFrame({'B': [0, 1]})


data2()

# +
# Finally we have a cell with only comments
# This cell should remain a code cell and not get converted
# to markdown

# + {"endofcell": "--"}
# This cell has an enumeration in it that should not
# match the endofcell marker!
# - item 1
# - item 2
# -
# --
'''):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 5
    assert nb.cells[0].cell_type == 'code'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[2].cell_type == 'code'
    assert nb.cells[3].cell_type == 'code'
    assert nb.cells[4].cell_type == 'code'
    assert (nb.cells[3].source ==
            '''# Finally we have a cell with only comments
# This cell should remain a code cell and not get converted
# to markdown''')
    assert (nb.cells[4].source ==
            '''# This cell has an enumeration in it that should not
# match the endofcell marker!
# - item 1
# - item 2
# -''')

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_prev_function(
        pynb="""def test_read_cell_explicit_start_end(pynb='''
import pandas as pd
# +
def data():
    return pd.DataFrame({'A': [0, 1]})


data()
'''):
    nb = jupytext.reads(pynb, 'py')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)
"""):
    nb = jupytext.reads(pynb, 'py')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_cell_with_one_blank_line_end(pynb="""import pandas

"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 1
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_code_cell_fully_commented(pynb="""# +
# This is a code cell that
# only contains comments
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'code'
    assert nb.cells[0].source == """# This is a code cell that
# only contains comments"""
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_file_with_two_blank_line_end(pynb="""import pandas


"""):
    nb = jupytext.reads(pynb, 'py')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_one_blank_lines_after_endofcell(pynb="""# +
# This is a code cell with explicit end of cell
1 + 1

2 + 2
# -

# This cell is a cell with implicit start
1 + 1
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'code'
    assert (nb.cells[0].source ==
            '''# This is a code cell with explicit end of cell
1 + 1

2 + 2''')
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[1].source == '''# This cell is a cell with implicit start
1 + 1'''
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_two_cells_with_explicit_start(pynb="""# +
# Cell one
1 + 1

1 + 1

# +
# Cell two
2 + 2

2 + 2
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'code'
    assert nb.cells[0].source == '''# Cell one
1 + 1

1 + 1'''
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[1].source == '''# Cell two
2 + 2

2 + 2'''
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_escape_start_pattern(pynb="""# The code start pattern '# +' can
# appear in code and markdown cells.

# In markdown cells it is escaped like here:
# # + {"sample_metadata": "value"}

# In code cells like this one, it is also escaped
# # + {"sample_metadata": "value"}
1 + 1
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 3
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[1].cell_type == 'markdown'
    assert nb.cells[2].cell_type == 'code'
    assert nb.cells[1].source == '''In markdown cells it is escaped like here:
# + {"sample_metadata": "value"}'''
    assert (nb.cells[2].source ==
            '''# In code cells like this one, it is also escaped
# + {"sample_metadata": "value"}
1 + 1''')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_dictionary_with_blank_lines_not_broken(
        pynb="""# This is a markdown cell, and below
# we have a long dictionary with blank lines
# inside it

dictionary = {
    'a': 'A',
    'b': 'B',

    # and the end
    'z': 'Z'}
"""):
    nb = jupytext.reads(pynb, 'py')
    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[0].source == '''This is a markdown cell, and below
we have a long dictionary with blank lines
inside it'''
    assert nb.cells[1].source == '''dictionary = {
    'a': 'A',
    'b': 'B',

    # and the end
    'z': 'Z'}'''
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_isolated_cell_with_magic(pynb="""# ---
# title: cell with isolated jupyter magic
# ---

# A magic command included in a markdown
# paragraph is code
#
# %matplotlib inline

# a code block may start with
# a magic command, like this one:

# %matplotlib inline

# or that one

# %matplotlib inline
1 + 1
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 6
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == '---\ntitle: cell with isolated jupyter ' \
                                 'magic\n---'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[2].cell_type == 'markdown'
    assert nb.cells[3].cell_type == 'code'
    assert nb.cells[3].source == '%matplotlib inline'
    assert nb.cells[4].cell_type == 'markdown'
    assert nb.cells[5].cell_type == 'code'
    assert nb.cells[5].source == '%matplotlib inline\n1 + 1'

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_multiline_comment(pynb="""'''This is a multiline
comment with "quotes", 'single quotes'
# and comments
and line breaks


and it ends here'''


1 + 1
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 2
    assert nb.cells[0].cell_type == 'code'
    assert nb.cells[0].source == """'''This is a multiline
comment with "quotes", 'single quotes'
# and comments
and line breaks


and it ends here'''"""
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[1].source == '1 + 1'

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_no_space_after_code(pynb=u"""# -*- coding: utf-8 -*-
# Markdown cell

def f(x):
    return x+1

# And a new cell, and non ascii contênt
"""):
    nb = jupytext.reads(pynb, 'py')

    assert len(nb.cells) == 3
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[0].source == 'Markdown cell'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[1].source == 'def f(x):\n    return x+1'
    assert nb.cells[2].cell_type == 'markdown'
    assert nb.cells[2].source == u'And a new cell, and non ascii contênt'

    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_write_script(pynb="""#!/usr/bin/env python
# coding=utf-8
print('Hello world')
"""):
    nb = jupytext.reads(pynb, 'py')
    pynb2 = jupytext.writes(nb, 'py')
    compare(pynb, pynb2)


def test_read_write_script_with_metadata_241(pynb="""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

a = 2

a + 1
"""):
    nb = jupytext.reads(pynb, 'py')
    assert 'executable' in nb.metadata['jupytext']
    assert 'encoding' in nb.metadata['jupytext']
    pynb2 = jupytext.writes(nb, 'py')

    # remove version information
    def remove_version_info(text):
        return '\n'.join([line for line in text.splitlines() if 'version' not in line])

    compare(remove_version_info(pynb), remove_version_info(pynb2))


def test_notebook_blank_lines(script="""# +
# This is a comment
# followed by two variables
a = 3

b = 4
# -

# New cell is a variable
c = 5


# +
# Now we have two functions
def f(x):
    return x + x


def g(x):
    return x + x + x


# -


# A commented block that is two lines away
# from previous cell

# A function again
def h(x):
    return x + 1


# variable
d = 6
"""):
    notebook = jupytext.reads(script, 'py')
    assert len(notebook.cells) >= 6
    for cell in notebook.cells:
        lines = cell.source.splitlines()
        if len(lines) != 1:
            assert lines[0], cell.source
            assert lines[-1], cell.source

    script2 = jupytext.writes(notebook, 'py')

    compare(script, script2)


def test_notebook_two_blank_lines_before_next_cell(script="""# +
# This is cell with a function

def f(x):
    return 4


# +
# Another cell
c = 5


def g(x):
    return 6


# +
# Final cell

1 + 1
"""):
    notebook = jupytext.reads(script, 'py')
    assert len(notebook.cells) == 3
    for cell in notebook.cells:
        lines = cell.source.splitlines()
        if len(lines) != 1:
            assert lines[0]
            assert lines[-1]

    script2 = jupytext.writes(notebook, 'py')

    compare(script, script2)


def test_notebook_one_blank_line_between_cells(script="""# +
1 + 1

2 + 2

# +
3 + 3

4 + 4

# +
5 + 5


def g(x):
    return 6


# +
7 + 7


def h(x):
    return 8


# +
def i(x):
    return 9


10 + 10


# +
def j(x):
    return 11


12 + 12
"""):
    notebook = jupytext.reads(script, 'py')
    for cell in notebook.cells:
        lines = cell.source.splitlines()
        assert lines[0]
        assert lines[-1]
        assert not cell.metadata, cell.source

    script2 = jupytext.writes(notebook, 'py')

    compare(script, script2)


def test_notebook_with_magic_and_bash_cells(script="""# This is a test for issue #181

# %load_ext line_profiler

# !head -4 data/president_heights.csv
"""):
    notebook = jupytext.reads(script, 'py')
    for cell in notebook.cells:
        lines = cell.source.splitlines()
        assert lines[0]
        assert lines[-1]
        assert not cell.metadata, cell.source

    script2 = jupytext.writes(notebook, 'py')

    compare(script, script2)


def test_notebook_no_line_to_next_cell(nb=new_notebook(
    cells=[new_markdown_cell('Markdown cell #1'),
           new_code_cell('%load_ext line_profiler'),
           new_markdown_cell('Markdown cell #2'),
           new_code_cell('%lprun -f ...'),
           new_markdown_cell('Markdown cell #3'),
           new_code_cell('# And a function!\n'
                         'def f(x):\n'
                         '    return 5')])):
    script = jupytext.writes(nb, 'py')
    nb2 = jupytext.reads(script, 'py')
    nb2.metadata.pop('jupytext')

    compare(nb, nb2)


def test_notebook_one_blank_line_before_first_markdown_cell(script="""
# This is a markdown cell

1 + 1
"""):
    notebook = jupytext.reads(script, 'py')
    script2 = jupytext.writes(notebook, 'py')
    compare(script, script2)

    assert len(notebook.cells) == 3
    for cell in notebook.cells:
        lines = cell.source.splitlines()
        if len(lines):
            assert lines[0]
            assert lines[-1]


def test_round_trip_markdown_cell_with_magic():
    notebook = new_notebook(cells=[new_markdown_cell('IPython has magic commands like\n%quickref')],
                            metadata={'jupytext': {'main_language': 'python'}})
    text = jupytext.writes(notebook, 'py')
    notebook2 = jupytext.reads(text, 'py')
    compare_notebooks(notebook, notebook2)


def test_round_trip_python_with_js_cell():
    notebook = new_notebook(cells=[new_code_cell('''import notebook.nbextensions
notebook.nbextensions.install_nbextension('jupytext.js', user=True)'''),
                                   new_code_cell('''%%javascript
Jupyter.utils.load_extensions('jupytext')''')])
    text = jupytext.writes(notebook, 'py')
    notebook2 = jupytext.reads(text, 'py')
    compare_notebooks(notebook, notebook2)


def test_round_trip_python_with_js_cell_no_cell_metadata():
    notebook = new_notebook(cells=[new_code_cell('''import notebook.nbextensions
notebook.nbextensions.install_nbextension('jupytext.js', user=True)'''),
                                   new_code_cell('''%%javascript
Jupyter.utils.load_extensions('jupytext')''')],
                            metadata={'jupytext': {'notebook_metadata_filter': '-all',
                                                   'cell_metadata_filter': '-all'}})
    text = jupytext.writes(notebook, 'py')
    notebook2 = jupytext.reads(text, 'py')
    compare_notebooks(notebook, notebook2)
