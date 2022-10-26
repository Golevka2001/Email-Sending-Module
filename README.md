# Email Sending Module :e-mail:

English | [简体中文](README.zh-CN.md)

## Table of Contents

- [Email Sending Module :e-mail:](#email-sending-module-e-mail)
  - [Table of Contents](#table-of-contents)
  - [Security](#security)
  - [Background](#background)
  - [Usage](#usage)
    - [Import the module](#import-the-module)
    - [Create object](#create-object)
    - [Load configuration](#load-configuration)
      - [Method 1：load from a configuration file](#method-1load-from-a-configuration-file)
      - [Method 2: load from parameters](#method-2-load-from-parameters)
    - [Send e-mails](#send-e-mails)
  - [Sample Programs](#sample-programs)
  - [Change Log](#change-log)
  - [License](#license)

## Security

This program will not collect or upload any personal information used when running, including e-mail addresses, passwords, etc. The personal information is only written into a local configuration file by users, or passed in through parameters.

:warning:**Remember**：Please do not send the configuration files with private information to anyone.

## Background

A few months ago, I participated in a contest. Our program would need to warn users when an intrusion on the smart home system was detected. I intended to use e-mails and wrote a simple version using ```smtplib```. \
Then I extracted this part as a separate module and improved functions, planning to complement an e-mail sending module can be called more conveniently in other programs.

## Usage

### Import the module

```python
from email_sending_module import EmailSendingModule
```

### Create object

```python
email = EmailSendingModule()
```

### Load configuration

#### Method 1：load from a configuration file

Create a configuration file named `config.yml`
(or other path/name) in the directory where the program is located, and call `config.load_from_file()` to load configuration:

```python
# if other path/name is adopted, please change this(absolute path is unnecessary):
config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yml')

# load configuration:
email.config.load_from_file(config_file_path)
```

A sample configuration file:

```yaml
# sender's information:
sender_information:
  address: '123@abc.xyz'  # e-mail address of sender
  password: '******'  # e-mail password of sender
  alias: 'Alice'  # alias of sender(optional, you can delete it)

# recipients' information:
recipients_information:
  # if only one recipient: use 'str' or 'list'
  # if more than one: use 'list', remember to match the addresses and alias names:
  address:  # e-mail address of recipients
    - '456@def.xyz'
    - '789@ghi.xyz'
  alias:  # alias of recipient(optional, you can delete it)
    - 'Bob'
    -  # you can leave it blank

# content of e-mails:
mail:
  subject: '[NOTIFICATION]'  # subject of e-mails
  body: 'Hello!'  # body of e-mails

# SMTP server's information:
server_information:
  address: 'smtp.abc.xyz'  # address of the SMTP server
  port: 25  # port number of the SMTP server

# options for sending e-mails repeatedly(optional, you can delete it):
resend_options:
  enable: False  # True - enable, False - disable
  # the following settings only have an effect when 'enable' is True
  times: 5  # number of times to send
  enable_random_interval: True  # True - enable, False - disable
  min_interval: 10  # minimum interval(seconds), this setting only has an effect when 'enable_random_interval' is True
  max_interval: 15  # maximum interval(seconds), this setting only has an effect when 'enable_random_interval' is True
  fixed_interval: 3  # assign a fixed interval(seconds), this setting only has an effect when 'enable_random_interval' is False

```

#### Method 2: load from parameters

Organize the parameters required by the module according to the required format in the program in advance, and call `config.load_from_parameters()` , pass in corresponding parameters to load configuration:

```python
# parameters:
# sender's information:
sender_information = {
    'address': '123@abc.xyz',  # e-mail address of sender
    'password': '******',  # e-mail password of sender
    'alias': 'Alice'  # alias of sender(optional, you can delete it)
}
# recipients' information:
recipients_information = {
    # if only one recipient: use 'str' or 'list'
    # if more than one: use 'list', remember to match the addresses and alias names:
    'address': ['456@def.xyz', '789@ghi.xyz'],  # e-mail address of recipients
    'alias': ['Bob', '']  # alias of recipient(optional, you can delete it)
}
# content of e-mails:
mail = {
    'subject': '[NOTIFICATION]',  # subject of e-mails
    'body': 'Hello!'  # body of e-mails
}
# SMTP server's information:
server_information = {
    'address': 'smtp.abc.xyz',  # address of the SMTP server
    'port': 25  # port number of the SMTP server
}
# options for sending e-mails repeatedly(optional, you can delete it):
resend_options = {
    'enable': True,  # True - enable, False - disable
    # the following settings only have an effect when 'enable' is True
    'times': 5,  # number of times to send
    'enable_random_interval': True,  # True - enable, False - disable
    'min_interval': 10,  # minimum interval(seconds), this setting only has an effect when 'enable_random_interval' is True
    'max_interval':15,  # maximum interval(seconds), this setting only has an effect when 'enable_random_interval' is True
    'fixed_interval':3  # assign a fixed interval(seconds), this setting only has an effect when 'enable_random_interval' is False
}

# load configuration：
email.config.load_from_parameters(sender_information, recipients_information, mail, server_information, resend_options)
```

### Send e-mails

```python
# send e-mails:
result = email.send_emails()
# print the result of sending:
print('Success:', result[0], '\nFailure:', result[1])
```

## Sample Programs

[demo.py](./demo.py)
[config_demo.yml](./config_demo.yml)

## Change Log

**2022-10-26:**

1. Fix "count".

**2022-09-27:**

1. In the recipients' information part, 'str' and 'list' both can be used;
2. Modify the alias field of the sender and recipients to be deletable。

**2022-09-26:**

1. Encapsulate as class;
2. Add a new configure loading method that load from parameters;
3. Modify the protocol used by the SMTP server to SSL.

**2022-09-17:**

1. Add a display of the aliases of senders and recipient, and formatting of e-mail addresses;
2. Add more functions for the resending past;
3. Modify the return method of mail sending results: ret[0] is number of successes, ret[1] is number of failures.

**2022-08-03:**

1. Add a function of repeated sending;
2. Add a display of e-mail recipients.

## License

[MIT © Gol3vka.](./LICENSE)
