from utils import log
from utils import template
from utils import redirect
from utils import http_response

from models import Replication


def index(request):
    replication_list = Replication.all()
    log(replication_list,'99999999')
    body = template('gerrit_index.html', replications=replication_list)
    return http_response(body)





def add(request):
    if request.method == 'POST':
        form = request.form()
        # 创建一个 todo
        Replication.new(form)
        # 让浏览器刷新页面到主页去
        return redirect('/')






route_dict = {
    '/': index,
    '/add': add,

}
