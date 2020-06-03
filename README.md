# free_proxy_pool
#### 运行
- **运行环境: Python3+Redis+Mysql**
- **没有Redis可在config.yml中将is_verify设置成False,但这样不会验证IP是否可用**
- **导依赖 pip install -r reuirements.txt**  
- **python start.py**
- **提供一个flask的接口**


**/config/config.yml 配置文件**
```
# mysql
db:
  host: 127.0.0.1
  port: 3306
  user: root
  passwd: 2018
  database: ip_pool
  tablename: ip_tables

# redis
redis:
  host: 127.0.0.1
  port: 6379
  key: ip

# 是否初始化数据库
IS_INIT_DATABASE: False

# 是否开启ip验证
is_verify: True

# 验证ip url
# test_proxy_url: https://www.google.com.hk
test_proxy_url: https://cn.bing.com

user-angers:
  - {"user-agent":"Mozilla/5.0 (Linux; Android 5.1; vivo X6D Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36"}

# 日志文件配置
log_config:
  file: crawl_ip.log
  level: INFO
  pattern: '%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s'
  datefmt: '%Y-%m-%d %H:%m:%S'
```

**/spider/spider_main.py 配置爬取ip的xpath**

``` 
    xpath_dict = {
        # IP组xpath 
        "ip_group": "//tbody/tr",
        # ip xpath
        "ip": "./td[1]/text()",
        # 端口 xpath
        "port": "./td[2]/text()",
        # 协议 xpath
        "proto" :"./td[4]/text()"
    }
```

> **接口**

**请求url:http://127.0.0.1/get_free_ip?action=get_ip&count=5**  
**count获取ip数量:0 < count <= 5**

```
request url:
    get_free_ip
request method: get
request param:
    action=get_ip: 必选 String
    count:  必选 String 获取ip的数量 <= 5
返回示例:
    {
      "result_code": "200",
      "result_msg": "请求成功",
      "result": true,
      "ip_list": [
        {
          "proto": "HTTP",
          "ip": "163.204.245.76",
          "port": "9999"
        }
      ]
    }

返回参数:
    proto:  代理协议
    ip:     代理ip
    port:   代理端口
```

