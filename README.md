<h1 align="center">Don't Starve Together Server of Docker</h1>

Run your DST Server from local save.
> 从本地存档快速搭建DST服务器

## Usage

1. Find your saves in `sdf`(Windows) or `sdf`(Unix),upload into your vps.

   > 在用户根目录下的`somewhere`找到存档文件,上传到你的服务器上

2. `git clone https://github.com/XuCcc/Dont_Starve_Together_of_Docker.git`

3. Install python packages `pip install -r requirements.txt` or `pipenv install --dev`

   > 安装依赖包 `pip install -r requirements.txt` 或者使用 `pipenv install --dev`

4. Run service `python dst.py path_to_save start`

   > 启动服务

```bash
[?] Your Token [pds-g^KU_SIyU7xC8^BefMQjkrZ8l/3SMeS3pIZPnh/R9qujwAt1cqXjuZoaQ=] is right? [Y/n]:
[!] Don't Starve Server Config
Name: Xu
Mode: survival
Password: Xuuuuuuu
Max Players: 8
Description: 
[+] Find Mods: ['1253432', '123123', '96678']
Pulling Test (thoxvi/dont-starve-together-docker-cluster:latest)...
```

**Other Command**

```bash

Usage: dst.py [OPTIONS] DIR COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  load   Load Config file
  mods   Load mods id			
  start  startup service
  token  Confirm token
```

## Require

**os** `Ubuntu 14.04.5 LTS \n \l`

- python3
- docker
- docker compose

You can use [InitUbuntu](https://github.com/XuCcc/InitUbuntu) to install these, ez(｡･ω･｡)ﾉ♡

> [InitUbuntu](https://github.com/XuCcc/InitUbuntu) 可以帮你迅速配置好环境依赖