import json
import os
import configparser
import subprocess
from utils import log
from config import gerrit_repliction_config


from collections import OrderedDict
from utils import log
import time


class multidict(OrderedDict):
    _unique = 0   # class variable

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += str(self._unique)
        OrderedDict.__setitem__(self, key, val)


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """

    with open(path, 'a+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write("\n")
        f.write(data["remote"]+"\n")
        f.write(data["projects"]+"\n")
        f.write(data["url"]+"\n")
        f.write("push = +refs/heads/*:refs/heads/*\n")
        f.write("push = +refs/tags/*:refs/tags/*\n")
        f.write("push = +refs/changes/*:refs/changes/*\n")
        f.write("threads = 3\n")
    #generate_dir(data["projects"],data["url"])

def generate_dir(projects,url):
    base = '/data/samba/gerrit-data/gerrit_samba/formal/git'
    last_url = url.split("=")[1]
    path = projects.split("=")[1]
    if not os.path.exists(base+os.sep+path):
        os.chdir(base)
        os.mkdirs(path)
    os.chdir(base+os.sep+path)
    cmd = 'git clone --bare {}'.format(last_url)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() == 0:
        log('git command success')


def load(path):
    replication_config = {}
    git_list_url = []
    config = configparser.ConfigParser(defaults=None, dict_type=multidict, strict=False)
    read = config.read(path,encoding='UTF-8-sig')
    section = config.sections()[::-1][:5]
    replication_list  = []
    for i in section:
        replication_list.append(
            {
                "remote":i,
                "projects":config.items(i)[0][1],
                "url": config.items(i)[1][1],

            }
        )
    return replication_list










# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = gerrit_repliction_config +'/{}.config'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()

        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)


    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log(self,'77776')
        log(self.url,'888886')
        t_path = self.url.split(":", 1)[-1].split("/")[:-1]
        path = "/".join(t_path).lstrip("/")

        self.remote = '''[remote "{}"]'''.format(path)
        self.project = "projects = " + path
        self.url = "url = " + self.url
        models = {
            "remote":self.remote,
            "projects":self.project,
            "url":self.url
        }

        path = self.db_path()
        log(models,'77777')
        save(models, path)

class Replication(Model):
    def __init__(self,form):
        self.remote = form.get('remote',"")
        self.project = form.get('project',"")
        self.url = form.get('url',"")
    def validate_login(self,form):
        result = False
        self.url = form.get('url',None)
        if self.url is not None:
            import commands
            status, output = commands.getstatusoutput("git ls-remote "  + self.url)
            if status == 0:
                result = True
        return result



    @classmethod
    def new(cls, form):
        t = cls(form)
        t.save()
        return t


    def nova_url (self):
        return self.url


    #     #self.remote = '''[remote "{}"]'''.format(self.nova_key())
    #     self.url = form.get('path','')
    #     self.remote = None
    #     #self.url = None
    #     self.project = None
        #self.project = self.nova_key()
