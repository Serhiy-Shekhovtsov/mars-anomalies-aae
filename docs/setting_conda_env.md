# Setting Conda Environment

Download and install anaconda [link](https://www.anaconda.com/distribution/).

## Install environment with all required packages:

```bash
$ conda env create -f environment.yml
```

## Activate conda environment, named `mars-aae`:

```bash
$ conda activate mars-aae
```

## To install packages:

```bash
$ conda install <package>
```

Or:

```bash
$ pip install <package>
```

## To uninstall run:

```bash
$ conda deactivate
$ conda env remove -n mars-aae
```
