
<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=AlexChrzanowski&project=makintikz&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

# makintikz
The artist formerly known as <em>tikzplotlib & matplot2tikz</em>.

![PyPI - Version](https://img.shields.io/pypi/v/makintikz)
![GitHub License](https://img.shields.io/github/license/AlexChrzanowski/makintikz)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/makintikz)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![codecov](https://codecov.io/gh/AlexChrzanowski/makintikz/graph/badge.svg?token=YE2VNWL9HI)](https://codecov.io/gh/AlexChrzanowski/makintikz)
[![PyPI Downloads](https://static.pepy.tech/badge/makintikz/month)](https://pepy.tech/projects/makintikz)

This is makintikz, a Python tool for converting matplotlib figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots) ([PGF/TikZ](https://www.ctan.org/pkg/pgf))
figures like

![](https://raw.githubusercontent.com/AlexChrzanowski/makintikz/refs/heads/main/example.png)

for native inclusion into LaTeX or ConTeXt documents.

The output of makintikz is in [PGFPlots](https://github.com/pgf-tikz/pgfplots/), a TeX
library that sits on top of [PGF/TikZ](https://en.wikipedia.org/wiki/PGF/TikZ) and
describes graphs in terms of axes, data etc. Consequently, the output of makintikz

-   retains more information,
-   can be more easily understood, and
-   is more easily editable

than [raw TikZ output](https://matplotlib.org/users/whats_new.html#pgf-tikz-backend).
For example, the matplotlib figure

```python
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")

t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2 * np.pi * t)
s2 = np.cos(2 * np.pi * t)
plt.plot(t, s, "o-", lw=4.1)
plt.plot(t, s2, "o-", lw=4.1)
plt.xlabel("time (s)")
plt.ylabel("Voltage (mV)")
plt.title("Simple plot $\\frac{\\alpha}{2}$")
plt.grid(True)

import makintikz

makintikz.save("test.tex")
```

-->
(see above) gives

```latex
\begin{tikzpicture}

\definecolor{chocolate2267451}{RGB}{226,74,51}
\definecolor{dimgray85}{RGB}{85,85,85}
\definecolor{gainsboro229}{RGB}{229,229,229}
\definecolor{steelblue52138189}{RGB}{52,138,189}
\begin{axis}[
axis background/.style={fill=gainsboro229},
axis line style={white},
tick align=outside,
tick pos=left,
title={Simple plot \(\displaystyle \frac{\alpha}{2}\)},
x grid style={white},
xlabel=\textcolor{dimgray85}{time (s)},
xmajorgrids,
xmin=-0.095, xmax=1.995,
xtick style={color=dimgray85},
y grid style={white},
ylabel=\textcolor{dimgray85}{Voltage (mV)},
ymajorgrids,
ymin=-1.1, ymax=1.1,
ytick style={color=dimgray85}
]
\addplot [line width=1.64pt, chocolate2267451, mark=*, mark size=3, mark options={solid}]
table {%
0 0
% [...]
1.9 -0.587785252292473
};
\addplot [line width=1.64pt, steelblue52138189, mark=*, mark size=3, mark options={solid}]
table {%
0 1
% [...]
1.9 0.809016994374947
};
\end{axis}

\end{tikzpicture}
```

(Use `get_tikz_code()` instead of `save()` if you want the code as a string.)

Tweaking the plot is straightforward and can be done as part of your TeX work flow.
[The fantastic PGFPlots manual](http://pgfplots.sourceforge.net/pgfplots.pdf) contains
great examples of how to make your plot look even better.

Of course, not all figures produced by matplotlib can be converted without error.
Notably, [3D plots don't work](https://github.com/matplotlib/matplotlib/issues/7243).


## Installation

makintikz is [available from the Python Package
Index](https://pypi.org/project/makintikz/), so simply do

```
pip install makintikz
```

to install.


## Usage

1. Generate your matplotlib plot as usual.

2. Instead of `pyplot.show()`, invoke makintikz by

    ```python
    import makintikz

    makintikz.save("mytikz.tex")
    # or
    makintikz.save("mytikz.tex", flavor="context")
    ```

    to store the TikZ file as `mytikz.tex`.

3. Add the contents of `mytikz.tex` into your TeX source code. A convenient way of doing
   so is via

    ```latex
    \input{/path/to/mytikz}
    ```
    
    Also make sure that the packages for PGFPlots and proper Unicode support and are
    included in the header of your document:

    ```latex
    \usepackage[utf8]{inputenc}
    \usepackage{pgfplots}
    \DeclareUnicodeCharacter{2212}{−}
    \usepgfplotslibrary{groupplots,dateplot}
    \usetikzlibrary{patterns,shapes.arrows}
    \pgfplotsset{compat=newest}
    ```

    or:

    ```latex
    \setupcolors[state=start]
    \usemodule[tikz]
    \usemodule[pgfplots]
    \usepgfplotslibrary[groupplots,dateplot]
    \usetikzlibrary[patterns,shapes.arrows]
    \pgfplotsset{compat=newest}
    \unexpanded\def\startgroupplot{\groupplot}
    \unexpanded\def\stopgroupplot{\endgroupplot}
    ```

    You can also get the code via:

    ```python
    import makintikz

    makintikz.Flavors.latex.preamble()
    # or
    makintikz.Flavors.context.preamble()
    ```

4. [Optional] Clean up the figure before exporting to tikz using the `clean_figure`
   command.

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    # ... do your plotting

    import makintikz

    makintikz.clean_figure()
    makintikz.save("test.tex")
    ```

    The command will remove points that are outside the axes limits, simplify curves and
    reduce point density for the specified target resolution.


## .Save() Parameters and Documentation

```makintikz.save()``` can be called with varying parameters:

* ##### ```filepath``` : <em>string or path, required</em>
     >Indicates where the new makintikz file should be stored and what the file name will be.
   
* ##### ```figure``` : <em>figure object or ```"gcf"```, optional</em>
  
* ##### ```axis_width``` : <em>string, optional</em>
     >Specifies figure width in output. Will preserve original diagram ratio if axis_height is not provided.
     
* ##### ```axis_height``` : <em>string, optional</em>
     >Specifies figure height in output. Will preserve original diagram ratio if axis_width is not provided.

* ##### ```textsize``` : <em>float, optional</em>
     >The text size (in pt) used by the latex document. Default is 10.0 pt.

* ##### ```tex_relative_path_to_data``` : <em>string, optional</em>
     >By default, when the TikZ file must refer to another file (e.g. a PNG for image plots) the additional file is looked for in a folder relative to the LaTeX file, not the TikZ file.  This argument optionally sets the relative path from the LaTeX file to the data.

* ##### ```externalize_tables``` : <em>boolean, optional</em>
     >When ``True``, externalizes plot data tables into DAT files. Default is ``False``.

* ##### ```override_externals``` : <em>boolean, optional</em>
     >When ``True``, overrides existing external files (e.g. DAT or PNG files) with conflicting names. When 'False', chooses other names. Default is ``False``.

* ##### ```strict``` : <em>boolean, optional</em>
     >When ``True``, creates TikZ file to strictly stick to MatPlotLib's appearance (influences tick mark appearance, etc.). Default is ``False``.

* ##### ```wrap``` : <em>boolean, optional</em>
     >When ``True``, writes ``'\\begin{tikzpicture}'``/``'\\starttikzpicture'`` and ``'\\end{tikzpicture}'``/``'\\stoptikzpicture'`` to the TikZ file. One might need to provide custom arguments to the environment (eg. scale). Default is ``True``.

* ##### ```add_axis_environment``` : <em>boolean, optional</em>
    > When ``True``, writes ``'\\begin{axis}[...]'``/`'\\startaxis[...]'` and ``'\\end{axis}'``/``'\\stopaxis'`` to the TikZ file. One may need to set the environment in the document. If ``False``, additionally sets ``wrap=False``. Default is ``True``.

* ##### ```extra_axis_parameters``` : <em>list of strings or set of strings for the pgfplots axes, optional</em>
     >Extra axis options to be passed to pgfplots.

* ##### ```extra_tikzpicture_parameters``` : <em>set of strings for the pgfplots tikzpicture, optional</em>
     >Extra tikzpicture options to be passed to pgfplots.

* ##### ```dpi``` : <em>integer, optional</em>
     >The resolution in dots per inch of the rendered image, to be used in the case of QuadMesh plots. Default is the value in ``savefig.dpi`` from matplotlib.rcParams.

* ##### ```show_info``` : <em>boolean, optional</em>
     >When ``True``, shows extra info on the command line. Default is ``False``.

* ##### ```include_disclaimer``` : <em>boolean, optional</em>
     >When ``True``, includes MakinTikZ disclaimer in the output. Set to ``False`` to make tests reproducible. Default is ``True``.

* ##### ```standalone``` : <em>boolean, optional</em>
     >When ``True``, includes wrapper code for a standalone LaTeX file. Default is ``False``.

* ##### ```float_format``` : <em>string, optional</em>
     >Indicates the format for float entities. Default is ```".15g"```.

* ##### ```table_row_sep``` : <em>string, optional</em>
     >Sets the row separator for table data. Default is ```"\\n"```.

* ##### ```flavor``` : <em>string, optional</em>
     >Indicates the TeX flavor of the output code. Supports ```"latex"``` and ```"context"```. Default is ```"latex"```.


## makintikz vs. matplot2tikz vs. tikzplotlib

The matplot2tikz library and makintikz originated from the [tikzplotlib](https://github.com/nschloe/tikzplotlib)
project.
The reason a new library has been created is because tikzplotlib is no longer maintained and 
maintainance could only be done by the single owner of the tikzplotlib library.
If you need to use third-party code that already depends on tikzplotlib, it is suggested to change
the tikzplotlib dependency to makintikz. 
If this is not possible, a workaround is to put the following code *before* importing the 
third-party code:

   ```
   import sys
   import makintikz
   sys.modules["tikzplotlib"] = makintikz
   # Do other imports, e.g., using `import my_third_party_library`
   # If tikzplotlib is used in this library, it will automatically use makintikz instead.
   ```

If you are updating your own scripts from tikzplotlib, you can simply use an import alias:

   ```python
   import makintikz as tikzplotlib
   ```


## Contributing

If you experience bugs, would like to contribute, have nice examples of what makintikz
can do, or if you are just looking for more information, then please visit
[makintikz's GitHub page](https://github.com/AlexChrzanowski/makintikz).

For contributing, follow these steps:

1. Download the git repository, e.g., using
   `git clone git@github.com:AlexChrzanowski/makintikz.git`.
2. Create a virtual environment, e.g., using `python -m venv venv`.
3. Activate the virtual environment (e.g., on Windows, `venv\Scripts\activate`).
4. Install `uv` using `pip install uv` and then `tox-uv` using `uv pip install tox-uv`.
5. The main branch is protected, meaning that you cannot directly push changes to this branch. 
   Therefore, if you want to make changes, do so in a seperate branch. For example, you can create 
   a new branch using `git checkout -b feature/my_awesome_new_feature`.
6. Before pushing changes, ensure that the code adheres to the linting rules and that the tests are 
   successful. Run `tox`. This does a linting check and runs all test scripts. To manually perform 
   these steps, use the following commands:
   1. Run `tox -e lint`. You can do the linting commands manually using:
      1. (One time) `uv pip install -r requirements-lint.txt`
      2. `ruff format . --check` (remove the `--check` flag to let `ruff` do the formatting)
      3. `ruff check .`
      4. `mypy .`
   2. Run `tox -e py310`.
   3. Run `tox -e py311`.
   4. Run `tox -e py312`.
   5. Run `tox -e py313`.
   6. Run `tox -e py314`.
   7. Run `tox -e combine-test-reports`
7. Check if the tests covered everything using the coverage report in 
   `/reports/coverage_html/index.html`.

   NOTE: Currently, now all code is covered. Ideally, all code is covered, but for now, ensure that 
   all *new* code is covered by the testing.
8. Push changes to GitHub. If everything is OK and you want to merge your changes to the `main`
   branch, create a pull request.
   Ideally, there is at least one reviewer who reviews the pull request before the merge.

Note that currently only "Code owners" can merge pull requests onto the `main` branch. This is to
ensure that not everyone can break the main code (even unintentially). If you want to be a "Code
owner", let us know!


## License

makintikz is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
