"""Модуль классов infoish"""
import os
from shutil import rmtree
from markdownTable import markdownTable
from git import Repo


class ZabbixReader:
    """ Класс для получения данных с Zabbix"""
    def get_data(self):
        """ должна возвращать массив данных"""
        return []

class GitLabWikiWriter:
    """Класс для записи данных в GitlabWiki"""
    def __init__(self, repo_url, user, password, filename='infra_info.md', tmp_dir_path="tmp_git"):
        self._tmp_dir_path = tmp_dir_path
        self._user = user
        self._password = password
        self._repo_url = repo_url
        self._filename = filename
        self.filename = os.path.join(self._tmp_dir_path, self._filename)
        self.set_environments()
        self.mk_tmp_dir()
        self._repo = Repo.clone_from(url=self.full_url_path, to_path=self._tmp_dir_path)

    def __del__(self):
        if os.path.exists(self._tmp_dir_path):
            rmtree(self._tmp_dir_path)

    def mk_tmp_dir(self):
        if not os.path.exists(self._tmp_dir_path):
            os.makedirs(self._tmp_dir_path)
        else:
            rmtree(self._tmp_dir_path)
            os.makedirs(self._tmp_dir_path)

    def set_environments(self):
        os.environ["GIT_AUTHOR_NAME"] = 'a.prusakov'
        os.environ["GIT_AUTHOR_EMAIL"] = 'devops.76.pf@gmail.com'
        os.environ["GIT_COMMITTER_NAME"] = 'infoish_bot'

    @property
    def full_url_path(self):
        return self._repo_url.replace("//", f"//{self._user}:{self._password}@")

    def make_md_file(self, data):
        md_table = markdownTable(data).getMarkdown()
        with open(self.filename, "w", encoding='utf-8') as file:
            print(md_table, file=file)

    def push_to_git(self):
        self._repo.git.add([os.path.abspath(self.filename)])
        self._repo.index.commit('Add infrainfo from infoish script')
        self._repo.remotes.origin.push()

    def write_data(self, data):
        self.make_md_file(data)
        self.push_to_git()


class MockReader:
    """Просто mock класс для проверки"""
    @staticmethod
    def get_data():
        server1 = {"name": "server1", "ip": "10.215.20.56", "services": ["app1", "app2", "app3"]}
        server2 = {"name": "server2", "ip": "10.215.20.52", "services": ["app4", "app5", "app6"]}
        server3 = {"name": "server3", "ip": "10.215.20.50", "services": ["app7", "app8", "app9"]}
        return [server1, server2, server3]


class MockWriter:
    """Просто mock класс для проверки"""
    def __init__(self, path):
        self._path = path
        self._filename = 'test.md'

    def mkdir(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def write_data(self, data):
        self.mkdir()
        filename = os.path.join(self._path, self._filename)
        md_table = markdownTable(data)
        md_table.row_sep = None
        table = md_table.getMarkdown()
        with open(filename, "w", encoding='utf-8') as file:
            print(table, file=file)


class Infoish:
    """ класс для чтения/записи данных"""
    def __init__(self):
        self._readers = []
        self._writers = []
        self._data = []

    def add_reader(self, reader):
        self._readers.append(reader)

    def add_writer(self, writer):
        self._writers.append(writer)

    def parse_data(self):
        """Читаем данные из ридеров"""
        for reader in self._readers:
            self._data += reader.get_data()

    def write_data(self):
        """Пишем данные"""
        for writer in self._writers:
            writer.write_data(self._data)
