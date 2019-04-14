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
python tools/download_data.py -h

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

15-Apr-19 00:15:36 - [10] file(s) will be downloaded [randomly] to [data]
15-Apr-19 00:15:36 - Starting...
15-Apr-19 00:15:36 - [1/10] | Downloading ESP_011313_1900_RED1_0.IMG ...
15-Apr-19 00:15:39 - File ESP_011313_1900_RED1_0.IMG downloaded successfully!
15-Apr-19 00:15:39 - [2/10] | Downloading ESP_011317_1665_RED0_1.IMG ...
15-Apr-19 00:15:45 - File ESP_011317_1665_RED0_1.IMG downloaded successfully!
15-Apr-19 00:15:45 - [3/10] | Downloading ESP_011319_1305_RED7_0.IMG ...
```

#### Download all files from bucket to `./data` folder

Set `-n` to `0`:

```bash
$ python tools/download_data.py -b <bucketname> -d -n 0 -v

15-Apr-19 00:21:12 - [1000] file(s) will be downloaded [not randomly] to [data]
15-Apr-19 00:21:12 - Starting...
15-Apr-19 00:21:12 - ESP_011261_1960_BG12_0.IMG file exists. Skipping...
15-Apr-19 00:21:12 - [1/1000] | Downloading ESP_011261_1960_BG12_1.IMG ...
15-Apr-19 00:21:19 - File ESP_011261_1960_BG12_1.IMG downloaded successfully!
15-Apr-19 00:21:19 - [2/1000] | Downloading ESP_011261_1960_BG13_0.IMG ...
```

As you can see already downloaded files are skipped.

#### Download all files to specified location

```bash
$ python tools/download_data.py -b <bucketname> -d /home/user/data -n 0 -v
```
