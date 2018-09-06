#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/9/6 11:11
# @File    : dst
# @Author  : x84106389
# @Site    : 
# @Version : 0.0.1

__author__ = 'Xu'

import os
import click
import pathlib
import re
from configparser import ConfigParser


class Message:
    docker_compose = """version: '2'
services:
    {name}:
        image: thoxvi/dont-starve-together-docker-cluster:latest
        ports:
          - "10999/udp"
          - "10998/udp"
        volumes:
          - "{save}:/root/.klei/DoNotStarveTogether/Cluster_1"
          - "{mod}:/root/DST/mods/dedicated_server_mods_setup.lua"
        container_name: {name}
    """
    mods_pattern = re.compile(r'workshop-(\d+)')


class Mods(object):
    def __init__(self, path: pathlib.Path):
        self.path = path

    def setup(self, ids: list):
        with self.path.open(mode='w') as f:
            for id in ids:
                f.write('ServerModSetup("{}")\n'.format(id))


class DSTSaves(object):
    def __init__(self, dirname: str):
        self.path = pathlib.Path(dirname)
        self.mods = Mods(self.path / 'dedicated_server_mods_setup.lua')
        self.config = ConfigParser()

    def load(self):
        self.config.read(str(self.path / 'cluster.ini'))
        print("""Don't Starve Server Config
Name: {name}
Mode: {mode}
Password: {password}
Max Players: {max}
Description: {des}""".format(name=self.config.get('NETWORK', 'cluster_name'),
                             mode=self.config.get('GAMEPLAY', 'game_mode'),
                             password=self.config.get('NETWORK', 'cluster_password'),
                             max=self.config.get('GAMEPLAY', 'max_players'),
                             des=self.config.get('NETWORK', 'cluster_description')))

    @property
    def parse(self):
        """
        :return: list
        """
        modoverrides = self.path / 'Master/modoverrides.lua'
        with modoverrides.open('r') as f:
            return Message.mods_pattern.findall(f.read())

    def start(self, detach: bool):
        self.load()
        print('Find Mods: {}'.format(self.parse))
        self.mods.setup(self.parse)
        docker = self.path / 'docker-compose.yml'
        with docker.open('w') as f:
            f.write(Message.docker_compose.format(
                    name=self.config.get('NETWORK', 'cluster_name'),
                    save=self.path.absolute(),
                    mod=self.mods.path.absolute()
            ))
        options = '-d' if detach else ''
        os.chdir(str(self.path))
        os.system('docker-compose up {}'.format(options))



pass_save = click.make_pass_decorator(DSTSaves)


class App(object):
    @click.group()
    @click.pass_context
    @click.argument('dir', type=click.Path(exists=True))
    def cli(ctx, dir):
        ctx.obj = DSTSaves(dir)

    @cli.command()
    @pass_save
    def load(save):
        save.load()

    @cli.command()
    @pass_save
    def mods(save):
        for id in save.parse:
            print('Mod: {}'.format(id))

    @cli.command()
    @click.option('--detach', '-d', default=False, is_flag=True, help='Run containers in the background')
    @pass_save
    def start(save, detach):
        save.start(detach)


if __name__ == '__main__':
    app = App()
    app.cli()
