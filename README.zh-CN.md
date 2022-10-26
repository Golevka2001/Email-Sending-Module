# Email Sending Module :e-mail:

[English](README.md) | 简体中文

## 目录

- [Email Sending Module :e-mail:](#email-sending-module-e-mail)
  - [目录](#目录)
  - [安全性](#安全性)
  - [背景](#背景)
  - [使用说明](#使用说明)
    - [导入模块](#导入模块)
    - [创建对象](#创建对象)
    - [加载配置](#加载配置)
      - [方法1：通过配置文件加载](#方法1通过配置文件加载)
      - [方法2：通过传入参数加载](#方法2通过传入参数加载)
    - [发送邮件](#发送邮件)
  - [示例程序](#示例程序)
  - [更新日志](#更新日志)
  - [使用许可](#使用许可)

## 安全性

此程序不会收集、上传在运行中所使用到的任何个人信息，包括邮箱地址、登录密码等。这些个人信息仅由用户写入本地配置文件中，或通过参数传入。

:warning:**切记**：请不要将写有隐私信息的配置文件发送给任何人。

## 背景

几个月前在做一个竞赛，我们的程序需要在检测到对智能家居系统的入侵后向用户发出警告。我当时就打算的是用e-mail来发送报警信息，并且写了一个很简陋的版本，是使用 `smtplib` 库来实现的。

后来就把这个部分单独摘出来当作一个单独的模块，又完善了一些功能，想实现一个更方便在其他程序中调用的邮件发送模块。

## 使用说明

### 导入模块

```python
from email_sending_module import EmailSendingModule
```

### 创建对象

```python
email = EmailSendingModule()
```

### 加载配置

#### 方法1：通过配置文件加载

在程序所在目录下创建 `config.yml` 文件（或其他路径、其他文件名），在程序中调用 `config.load_from_file()` 进行加载：

```python
# 若采用其他路径或文件名，请修改此项（绝对路径不是必要的）：
config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yml')

# 加载配置：
email.config.load_from_file(config_file_path)
```

配置文件示例：

```yaml
# 发件人相关信息：
sender_information:
  address: '123@abc.xyz'  # 发件人邮箱地址
  password: '******'  # 发件人邮箱密码
  alias: 'Alice'  # 发件人别名（非必要项，可删除）

# 收件人相关信息：
recipients_information:
  # 若只有一位收件人，使用字符串或列表类型均可
  # 若存在多位收件人，请使用列表类型，注意两个列表项数和顺序的匹配
  address:  # 收件人邮箱地址
    - '456@def.xyz'
    - '789@ghi.xyz'
  alias:  # 收件人别名（非必要项，可删除）
    - 'Bob'
    -  # 也可以留空

# 邮件内容：
mail:
  subject: '[NOTIFICATION]'  # 邮件主题
  body: 'Hello!'  # 邮件正文

# SMTP服务器相关信息：
server_information:
  address: 'smtp.abc.xyz'  # 发件邮箱对应的SMTP服务器地址
  port: 25  # SMTP服务器端口号

# 重复发送邮件相关设置（非必要项，可删除）：
resend_options:
  enable: False  # 是否启用重复发送
  # 以下设置仅在'enable'为True时生效：
  times: 3  # 重复发送次数
  enable_random_interval: True  # 是否启用随机时间间隔
  min_interval: 1  # 最小时间间隔（秒），此设置仅在'enable_random_interval'为True时生效
  max_interval: 10  # 最大时间间隔（秒），此设置仅在'enable_random_interval'为True时生效
  fixed_interval: 5  # 固定时间间隔（秒），此设置仅在'enable_random_interval'为False时生效

```

#### 方法2：通过传入参数加载

预先在程序中将模块所需参数按照要求格式组织好，调用 `config.load_from_parameters()` ，传入相应参数进行加载：

```python
# 参数：
# 发件人相关信息：
sender_information = {
    'address': '123@abc.xyz',  # 发件人邮箱地址
    'password': '******',  # 发件人邮箱
    'alias': 'Alice'  # 发件人别名（非必要项，可删除）
}
# 收件人相关信息：
recipients_information = {
    # 若只有一位收件人，使用字符串或列表类型均可
    # 若存在多位收件人，请使用列表类型，注意两个列表项数和顺序的匹配
    'address': ['456@def.xyz', '789@ghi.xyz'],  # 收件人邮箱地址
    'alias': ['Bob', '']  # 收件人别名（非必要项，可删除）
}
# 邮件内容：
mail = {
    'subject': '[NOTIFICATION]',  # 邮件主题
    'body': 'Hello!'  # 邮件正文
}
# SMTP服务器相关信息：
server_information = {
    'address': 'smtp.abc.xyz',  # 发件邮箱对应的SMTP服务器地址
    'port': 25  # SMTP服务器端口号
}
# 重复发送邮件相关设置（非必要项，可删除）：
resend_options = {
    'enable': True,  # 是否启用重复发送
    # 以下设置仅在'enable'为True时生效：
    'times': 5,  # 重复发送次数
    'enable_random_interval': True,  # 是否启用随机时间间隔
    'min_interval': 10,  # 最小时间间隔（秒），此设置仅在'enable_random_interval'为True时生效
    'max_interval':15,  # 最大时间间隔（秒），此设置仅在'enable_random_interval'为True时生效
    'fixed_interval':3  # 固定时间间隔（秒），此设置仅在'enable_random_interval'为False时生效
}

# 加载配置：
email.config.load_from_parameters(sender_information, recipients_information, mail, server_information, resend_options)
```

### 发送邮件

```python
# 发送邮件：
result = email.send_emails()
# 打印发送结果：
print('Success:', result[0], '\nFailure:', result[1])
```

## 示例程序

[demo.py](./demo.py)
[config_demo.yml](./config_demo.yml)

## 更新日志

**2022-10-26:**

1. 修复“count”的错误。

**2022-09-27:**

1. 收件人相关信息部分，str或list类型均可使用；
2. 修改收、发件人的别名（alias）字段为可删去。

**2022-09-26:**

1. 封装为类；
2. 新增从参数传入的配置加载方式；
3. 修改SMTP服务器使用SSL协议发送邮件。

**2022-09-17:**

1. 新增收、发件人的别名显示，以及邮箱地址格式化；
2. 重复发送部分新增更多功能；
3. 修改邮件发送结果的返回方式：ret[0]为发送成功次数，ret[1]为发送失败次数。

**2022-08-03:**

1. 新增重复发送功能；
2. 新增邮件收件人部分的显示。

## 使用许可

[MIT © Gol3vka.](./LICENSE)
