FROM pypy:3.7

# pyenvとpython3.9のインストール 参考→https://codeaid.jp/pyenv-linux/
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    . ~/.bashrc  && \
    pyenv install 3.6.4

WORKDIR /src

# python3仮想環境構築とモジュールのインストール
COPY Pipfile* ./
RUN pip install pipenv && \
    pipenv install

# pypy環境へのモジュールのインストール
COPY requirements-for-pypy.txt .
RUN pip install -r requirements-for-pypy.txt
