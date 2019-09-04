# plasma-cash

[![codecov](https://codecov.io/gh/omisego/plasma-cash/branch/master/graph/badge.svg)](https://codecov.io/gh/omisego/plasma-cash)

### Dependency Prerequisite

- [LevelDB](https://github.com/google/leveldb)

Mac:
```
$ brew install leveldb
```

Linux:

LevelDB should be installed along with `plyvel` once you make the project later on.

Windows:

First, install [vcpkg](https://github.com/Microsoft/vcpkg). Then,

```
> vcpkg install leveldb
```

- [Solidity 0.4.24](https://github.com/ethereum/solidity/releases/tag/v0.4.24)

Mac:
```
$ brew update
$ brew upgrade
$ brew tap ethereum/ethereum
$ brew install solidity
```

Linux:
```
$ wget https://github.com/ethereum/solidity/releases/download/v0.4.24/solc-static-linux
$ chmod +x ./solc-static-linux
$ sudo mv solc-static-linux /usr/bin/solc
```

Windows:

Follow [this guide](https://solidity.readthedocs.io/en/v0.4.21/installing-solidity.html#prerequisites-windows).

- [ganache-cli 6.1.2+](https://github.com/trufflesuite/ganache-cli)

It's also recommended to run `ganache-cli` when developing, testing, or playing around. This will allow you to receive near instant feedback.

Mac:
```
$ brew install node
$ npm install -g ganache-cli
```

Linux:

Install [Node.js](https://nodejs.org/en/download/). Then,
```
$ npm install -g ganache-cli
```

- [Python 3.5+](https://www.python.org/downloads/)

### Develop

Install requirements:
```
pip install -r requirements.txt
```

Ganache-cli command:
```
ganache-cli -m=plasma_cash
```

Deploy contract:
```
python deployment.py
```

Run child chain Server:
```
python -m plasma_cash.child_chain
```

Run operator cron jobs:
(TODO: the following commands does not support running with cron job yet)
```
python -m plasma_cash.operator_cron_job
```

User dapp:
```
python user/user_flask_application.py
```
