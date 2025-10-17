import requests
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import datetime


Error = 0
update_flag = 0


ZONE_ID = '***'
DOMAIN_NAME = '***'
API_TOKEN = '***'
SUBDOMAIN = '***'
RECORD_ID = '***'


sender_email = '***'
sender_password = '***'
recipient_email = '***'

WORKPATH = '***'


def update_dns_record(ip_address):
    """更新 Cloudflare DNS 记录"""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": f"{SUBDOMAIN}.{DOMAIN_NAME}",
        "content": ip_address,
        "ttl": 1,  # 自动 TTL
        "proxied": False  # 如果需要通过 Cloudflare 的代理，请设置为 True
    }

    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        if response.json().get("success"):
            print(f"DNS 记录更新成功: {ip_address}")
        else:
            print(f"DNS 记录更新失败: {response.json()}")
    except requests.RequestException as e:
        print(f"更新 DNS 记录失败: {e}")

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # 创建邮件对象
        message = MIMEMultipart()
        message['From'] = Header(sender_email)
        message['To'] = Header(recipient_email)
        message['Subject'] = Header(subject, 'utf-8')

        # 添加邮件正文
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # 使用 SMTP 协议发送邮件
        with smtplib.SMTP_SSL('smtp.126.com', 587) as server:  # 替换为实际的 SMTP 服务器地址
            server.login(sender_email, sender_password)  # 登录邮箱
            server.sendmail(sender_email, recipient_email, message.as_string())  # 发送邮件

        print("邮件发送成功！")

    except Exception as e:
        print(f"邮件发送失败：{e}")

try:
    hit_ip =  requests.get('https://wp.hit.edu.cn/cgi-bin/rad_user_info').text.split(',')[8]

except Exception as e:
    Error = 1

with open(f'{WORKPATH}hitip', 'r') as f:
    oldip = ''
    try:
        oldip = f.readlines()[-1].split(' ')[-1].replace('\n', '')
        print(oldip)
    except Exception as e:
        pass
    if oldip != hit_ip:
        try:
            update_dns_record(hit_ip)
            update_flag = 1
        except Exception as e:
            Error = 2
    f.close()

with open(f'{WORKPATH}hitip', 'a') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')+hit_ip+'\n')

message = ''
if Error == 1:
    message += '未能获取到哈工大ip\n'
if Error == 2:
    message += 'cloudflare更新dns记录失败'

if update_flag == 1:
    message += f'cloudflare记录更新成功\n{hit_ip}'

if update_flag == 1 or (Error ==1 or Error == 2):
    send_email(sender_email,sender_password,recipient_email,'ddns脚本通知',message)
