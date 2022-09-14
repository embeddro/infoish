import infoish


if __name__ == '__main__':
    reader = infoish.MockReader()
    # writer = infoish.GitLabWikiWriter(repo_url='https://gitlab.devpizzasoft.ru:8000/pzsoft-cluster/wiki.wiki.git',
    #                                   user='user', password='password')
    writer = infoish.MockWriter('tmp')
    worker = infoish.Infoish()
    worker.add_reader(reader)
    worker.add_writer(writer)
    worker.parse_data()
    worker.write_data()
