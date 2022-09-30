#!user/bin/env python
# -*- coding:utf-8 -*-
'''demo.py: a demonstrate of the e-mail sending module.
@Author: Gol3vka<gol3vka@163.com>
@Created Date: 2022/05/16
@Last Modified Date: 2022/09/30
'''

from email_sending_module import EmailSendingModule

import os

''' Load configuration '''
# Method 1: using an yaml format config file
# create your own config file by referring to 'config_demo.yml':
config_file_name = 'config.yml'  # change this str to your config file name
config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           config_file_name)
email_1 = EmailSendingModule()
email_1.config.load_from_file(config_file_path)

# Method 2: using parameters
sender_information = {
    'address': '123@abc.xyz',
    'password': '******',
    #'alias': 'Alice'  # 'alias 'can be deleted from this dict
}
receivers_information = {
    'address': ['456@def.xyz', '789@ghi.xyz'],
    'alias': ['Bob', '']  # match the 2 lists
}
mail = {'subject': '[NOTIFICATION]', 'body': 'Hello!'}
server_information = {'address': 'smtp.abc.xyz', 'port': 25}
# 'resend_options' is optional
email_2 = EmailSendingModule()
email_2.config.load_from_parameters(sender_information, receivers_information,
                                    mail, server_information)
''' Send e-mails '''
result_1 = email_1.send_emails()
print('Success:', result_1[0], '\nFailure:', result_1[1])

result_2 = email_2.send_emails()
print('Success:', result_2[0], '\nFailure:', result_2[1])
