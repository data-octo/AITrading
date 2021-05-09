# AITrading
Reinforcement Learning for trading cryptocurrencies, stocks and forex 


## Python Virtual Environment
### Using Conda
https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/02-working-with-environments/index.html

Install virtual environment in current project folder
- conda create --prefix ./env python=3.8
- conda activate ./env
- conda activate /Users/yuan/Projects/github/ai-trading/env
- conda remove --prefix /path/to/conda-env/ --all
  
Install virutal environmenbt in default home folder
- conda create --name env_tensortrade python=3.8
- conda remove --name my-first-conda-env --all
- conda list --name basic-scipy-env

### Using Python venv
- python3 -m venv <name_of_virtualenv>
- virtualenv venv
- source ./venv/bin/activate

## Documentation

This directory contains the sources (`.md` and `.rst` files) for the
documentation. The main index page is defined in `source/index.rst`.
The Sphinx options and plugins are found in the `source/conf.py` file.
The documentation is generated in full by calling `make html` which
also automatically generates the Python API documentation from
docstrings.


Sphinx and ReadtheDocs

- [Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)

- [Read the Docs theme](https://github.com/readthedocs/sphinx_rtd_theme)

- [Sphinx Markdown support](https://www.sphinx-doc.org/en/master/usage/markdown.html)

- [Sample Doc](https://matplotlib.org/sampledoc/getting_started.html)

```
pip install sphinx

pip install sphinx_rtd_theme

pip install --upgrade myst-parser
```

Create folder for documentation

```
mkdir docs

cd docs

sphinx-quickstart

make html
```

Update conf.py 


### Building documentation locally

Dependencies must be installed using `make sync` from the project root.
Run `make docs-build` from project root, or `make html` from the `docs/` subfolder (this one).

Note this can take some time as some of the notebooks may be executed
during the build process. The resulting documentation is located in the
`build` directory with `build/html/index.html` marking the homepage.

### Sphinx extensions and plugins

We use various Sphinx extensions and plugins to build the documentation:

- [recommonmark](https://recommonmark.readthedocs.io) - to handle both `.rst` and `.md`
- [sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) - support extracting Numpy style doctrings for API doc generation
- [sphinx_autodoc_typehints](https://github.com/agronholm/sphinx-autodoc-typehints) - support parsing of typehints for API doc generation
- [sphinxcontrib.apidoc](https://github.com/sphinx-contrib/apidoc) - automatic running of [sphinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html) during the build to document API
- [nbsphinx](https://nbsphinx.readthedocs.io) - parsing Jupyter notebooks to generate static documentation
- [nbsphinx_link](https://nbsphinx-link.readthedocs.io) - support linking to notebooks outside of Sphinx source directory via `.nblink` files

The full list of plugins and their options can be found in `source/conf.py`.


## Reference



TensorTrade Source Code
https://github.com/tensortrade-org/tensortrade


TensorTrade Doc - HTML
https://www.tensortrade.org/en/latest/index.html

TensorTrade Doc - PDF
https://readthedocs.org/projects/tensortrade/downloads/pdf/latest/


(Guide - English) Trade and Invest Smarter — The Reinforcement Learning Way
https://towardsdatascience.com/trade-smarter-w-reinforcement-learning-a5e91163f315

Using TensorTrade for Making a Simple Trading Algorithm
https://levelup.gitconnected.com/using-tensortrade-for-making-a-simple-trading-algorithm-6fad4d9bc79c

(Guide - CN Translated) TensorTrade：基于深度强化学习的Python交易框架
https://cloud.tencent.com/developer/article/1525771?tt_from=copy_link&utm_source=copy_link&utm_medium=toutiao_ios&utm_campaign=client_share

(Guide - RL) Reinforcement Q-Learning from Scratch in Python with OpenAI Gym
https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/

(Guide - PPO) PPO Hyperparameters and Ranges
https://medium.com/aureliantactics/ppo-hyperparameters-and-ranges-6fc2d29bccbe


Train a Deep Q Network with TF-Agents
https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial