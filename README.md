# gerrit-config-web
gerrit的加库通过replication.conf添加gitlab源对于不懂linux的管理人员实在太容易出错。

  1 [remote "..."]
  2 projects = ...
  3 url = ...
  4 push = +refs/heads/*:refs/heads/*
  5 push = +refs/tags/*:refs/tags/*
  6 push = +refs/changes/*:refs/changes/*
  7 threads = 3

类似于这样的格式

只是想实现个网页
通过gitlab地址自动添加到replication.config，同时到gerrit的git文件夹下载，减少运维的工作。

至于gerrit replication重启，为什么不能配置项目权限，百思不得其解....
