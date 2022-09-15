import os

import infoish


if __name__ == '__main__':
    zabbix_url = os.getenv('ZABBIX_URL', '')
    zabbix_user = os.getenv('ZABBIX_USER', '')
    zabbix_password = os.getenv('ZABBIX_PASSWORD', '')
    gitlab_url_repo = os.getenv('GITLAB_URL_REPO', '')
    gitlab_user = os.getenv('GITLAB_USER', '')
    gitlab_password = os.getenv('GITLAB_PASSWORD', '')
    reader = infoish.ZabbixReader(url=zabbix_url,
                                  user=zabbix_user,
                                  password=zabbix_password)
    writer = infoish.GitLabWikiWriter(repo_url=gitlab_url_repo,
                                      user=gitlab_user,
                                      password=gitlab_password)
    # writer = infoish.MockWriter('tmp')
    worker = infoish.Infoish()
    worker.add_reader(reader)
    worker.add_writer(writer)
    worker.parse_data()
    worker.write_data()
