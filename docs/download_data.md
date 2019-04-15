# How to Use `download_data` Tool

> `download_data` is python based commandline tool for file downloading from bucket.
Tool is located in `tools` folder.

## Prerequisites

```bash
$ pip install boto3
```

## Usage

### Quick Help

```bash
$ python tools/download_data.py -h

usage: download_data.py [-h] [-b BUCKET] [-p PREF] [-d PATH] [-n N] [-r] [-v]

Downloads specified number of [random] files from Amazon S3 bucket.

optional arguments:
  -h, --help                    show this help message and exit
  -b BUCKET, --bucket BUCKET    Bucket name.
  -p PREF, --pref PREF          Bucket prefix (Default: DATA/).
  -d PATH, --dir PATH           Destination path for files (Default: data).
  -n N, --nfiles N              Number of files to load (Default: 5). Set 0 to download all files.
  -r, --rand                    Download randomly (Default: False).
  -v, --verbose                 Print info (Default: False).
```

### Examples

> **NOTE:** All examples treat project root folder as working dir!

#### Download 10 random files to `./data` folder

```bash
$ python tools/download_data.py -b <bucketname> -n 10 -r
```

To print some info, simply add `-v` or `--verbose` flag:

```bash
$ python tools/download_data.py -b <bucketname> -n 10 -r -v

15-Apr-19 07:27:05 - [10] file(s) will be downloaded [randomly] to [data]
15-Apr-19 07:27:05 - Starting...
15-Apr-19 07:27:05 - [1/10] | Downloading ESP_011288_1675_BG13_1.IMG...
15-Apr-19 07:27:08 - File ESP_011288_1675_BG13_1.IMG was downloaded successfully!
15-Apr-19 07:27:08 - [2/10] | Downloading ESP_011265_1560_RED3_0.IMG...
```

#### Download all files from bucket to `./data` folder

Set `-n` to `0`:

```bash
$ python tools/download_data.py -b <bucketname> -d -n 0 -v

15-Apr-19 07:28:40 - [1000] file(s) will be downloaded [not randomly] to [data]
15-Apr-19 07:28:40 - Starting...
15-Apr-19 07:28:40 - ESP_011261_1960_BG12_0.IMG file exists. Skipping...
15-Apr-19 07:28:40 - ESP_011261_1960_BG12_1.IMG file exists. Skipping...
15-Apr-19 07:28:40 - [3/1000] | Downloading ESP_011261_1960_BG13_0.IMG...
15-Apr-19 07:28:47 - File ESP_011261_1960_BG13_0.IMG was downloaded successfully!
15-Apr-19 07:28:47 - [4/1000] | Downloading ESP_011261_1960_BG13_1.IMG...
```

As you can see already downloaded files are skipped.

#### Download all files to specified location

```bash
$ python tools/download_data.py -b <bucketname> -d /home/user/data -n 0 -v
```
