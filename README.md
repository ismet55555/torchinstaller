<p align="center"><div align="center" style="display": none;>
  
# `torchinstaller`

<h3 align="center">Installing PyTorch has never been this easy!</h3>

</div></p>

<p align="center">

<a href="https://pypi.org/project/torchinstaller/">
  <img alt="PYPI Version" src="https://img.shields.io/pypi/v/torchinstaller?color=blue">
</a>

<a href="https://github.com/dk0d/torchinstaller/blob/main/LICENSE">
  <img alt="Licence" src="https://img.shields.io/pypi/l/torchinstaller">
</a>

</p>

`torchinstaller` is a super simple helper to install PyTorch stuff without having to check cuda versions and go to websites for the installer URLs.
It installs PyTorch components based on requested or detected CUDA version, and doesn't check python versions.

> **_Only Linux and macOS supported_**

It detects what cuda version is available and runs the pip command to install latest PyTorch and compatible cuda version

## Installation

```bash
pip install torchinstaller
```

## Usage

```bash
$ torchinstall -h
usage: torchinstall [-h] [--pytorch [PYTORCH]] [--pyg] [--pyg-lib-source]
                    [--compute-platform {+,cu102,cu111,cu113,cu116,cu117,cu118,cu121,rocm4.0.1,rocm4.1,rocm4.2,rocm4.5.2,rocm5.1.1,rocm5.2,rocm5.4.2,rocm5.6,rocm5.7}]
                    [--lightning] [--use {pip,conda,mamba}] [-install] [--sync]

options:
  -h, --help            show this help message and exit
  --pytorch [PYTORCH], -pt [PYTORCH]
                        Flag to install pytorch, can optionally specify a desired version. Must be full
                        semantic version, e.g. 1.13.1, not 1.13, defaults to `latest`
  --pyg, -pyg           Flag to install pytorch-geometric
  --pyg-lib-source, -pyg-src
                        Flag to install PyG from source. i.e. PyG doesn't support wheels for M1/M2 macs.
                        They recommend installing from source
  --compute-platform {+,cu102,cu111,cu113,cu116,cu117,cu118,cu121,rocm4.0.1,rocm4.1,rocm4.2,rocm4.5.2,rocm5.1.1,rocm5.2,rocm5.4.2,rocm5.6,rocm5.7}, -c {+,cu102,cu111,cu113,cu116,cu117,cu118,cu121,rocm4.0.1,rocm4.1,rocm4.2,rocm4.5.2,rocm5.1.1,rocm5.2,rocm5.4.2,rocm5.6,rocm5.7}
                        Manually specify platform version (cuda or rocm) instead ofauto-detect (useful
                        for cluster installations).
  --lightning, -l       Flag to install lightning (lightning.ai)
  --use {pip,conda,mamba}, -u {pip,conda,mamba}
                        set command to install with.
  -install, -i          Run installation (default is to dry run commands)
  --sync, -s            update installation commands by parsing the pytorch website
```

> Note: `pytorch-geometric` can be problematic to install. Installing from source has been added to facilitate installation, but referring to their documentation may be necessary to address errors if they occur.

