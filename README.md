# django-vue-admin

### 项目介绍
1. 基于 **django-rest-framework** + **vue2** + **element ui**
2. 支持 **企业微信扫码登录**
3. 支持 **钉钉扫码登录**
4. 支持 **飞书扫码登录**
5. 前端框架 [https://github.com/PanJiaChen/vue-admin-template/tree/permission-control](https://github.com/PanJiaChen/vue-admin-template/tree/permission-control)
6. 开发环境
```
操作系统： macOS Monterey
前端环境： Node v16.15.1 (Npm v8.11.0)
后端环境： Python 3.10
数据库：   Mysql 8.0.24
开发工具： Pycharm
```

### todo
1. 三方登录时强制要求绑定主账户，没有主账户需要注册后再使用三方登录

### 加入我们

<img src="https://github.com/YuYingTechnology/django-vue-admin/blob/main/images/qq.png?raw=true" width="25%" height="25%"><img src="https://github.com/YuYingTechnology/django-vue-admin/blob/main/images/wechat.png?raw=true" width="28%" height="28%">

### 项目截图

<img src="https://github.com/YuYingTechnology/django-vue-admin/blob/main/images/login.png?raw=true" width="53%" height="53%">

### 食用方法

#### 拉取代码
```shell
git clone https://github.com/YuYingTechnology/django-vue-admin.git
```

#### openresty（nginx） 实现前后端分离
```conf
server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;


        location / {
            root   /tmp;
            proxy_pass http://127.0.0.1:9528;   # 与npm run dev 后的端口保持一致
            index  index.html index.htm;
        }


        location /api {
            root   html;
            index  index.html index.htm;
            proxy_set_header  Host  $host;
            proxy_set_header  Domain $scheme://$host;    # 必须！！！
            proxy_set_header  X-real-ip $remote_addr;
            proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://127.0.0.1:8000;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

```

#### 前端
```shell
cd django-vue-admin/web/
npm install
npm run dev
```

#### 后端
```shell
cd django-vue-admin/server/
pip install -r requirements.txt
python manager.py runserver
```

### 访问
```
浏览器打开
http://localhost
```