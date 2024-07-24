from service import views

urls = [
    # 获取流水线列表-首页
    ('/get_flow_list', views.get_flow_list),
    # 登录
    ('/login', views.login),
    # 注册
    ('/register', views.register),
    # 流水线详情
    (r'/get_flow_detail', views.get_flow_detail),
    # 流水线设置
    (r'/flow_setting', views.flow_setting),
    # 添加流水线
    (r'/add_flow', views.add_flow),
]
