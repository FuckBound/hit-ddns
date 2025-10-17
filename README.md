# hit-ddns
哈工大校园网内网ddns 基于cloudflare
更新会发送电子邮件

获取校园网内网ip的关键
```
hit_ip =  requests.get('https://wp.hit.edu.cn/cgi-bin/rad_user_info').text.split(',')[8]
```
