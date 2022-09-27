#!user/bin/env python
# -*- coding:utf-8 -*-
'''email_sending_module.py: a module used to send e-mails,\
    providing more convenience.
@Author: Golevka2001<gol3vka@163.com>
@Version: 2.0.0
@Created Date: 2022/05/16
@Last Modified Date: 2022/09/27
'''
# TODO: make adding appendix available. (MIMEMultipart)
# TODO: now all receivers are display in the field 'TO', make them hidden.

import os
import random
import time

import smtplib
import yaml

from email.header import Header
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailSendingModule:
    '''A module used to send e-mails, providing more convenience.

    Vars:
        config (class Configuration): configuration of e-mail sending module

    Functions:
        __init__()
        send_emails()
        _send_helper
        _format_address()
    '''

    def __init__(self) -> None:
        class Configuration:
            '''Configuration of e-mail sending module.

            Vars:
                sender (dict): ['address'(str), 'password'(str), 'alias'(str)]
                receivers (dict): ['address'(str_list), 'alias'(str_list)]
                mail (dict): ['subject'(str), 'body'(str)]
                serve (dict): ['address'(str), 'port'(int)]
                resend (dict): ['enable'(bool), 'times'(int),\
                    'enable_random_interval'(bool), 'min_interval'(int),\
                        'max_interval'(int), 'fixed_interval'(int)]

            Functions:
                load_from_file()
                load_from_parameters()
            '''

            def load_from_file(self, config_path) -> None:
                '''Load configuration from a yaml file.

                Args:
                    config_path (str): path of config file
                '''
                if not os.path.exists(config_path):
                    raise Exception('No such file or directory:' + config_path)
                else:
                    # load config from 'config.yml':
                    with open(config_path, 'r',
                              encoding='utf-8') as config_file:
                        config = yaml.safe_load(config_file)
                        config_file.close()
                    # assign:
                    self.sender = config['sender_information']
                    self.receivers = config['receivers_information']
                    self.mail = config['mail']
                    self.server = config['server_information']
                    # 'resend_options' is optional, set a default value:
                    if 'resend_options' in config:
                        self.resend = config['resend_options']
                    else:
                        self.resend = {'enable': False}

            def load_from_parameters(self,
                                     sender_information,
                                     receivers_information,
                                     mail,
                                     server_information,
                                     resend_options={'enable': False}) -> None:
                '''Load configuration from these parameters.

                Args:
                    see the'Vars' part in comment of 'class Configuration '
                '''
                # assign:
                self.sender = sender_information
                self.receivers = receivers_information
                self.mail = mail
                self.server = server_information
                self.resend = resend_options

        self.config = Configuration()

    def send_emails(self):
        '''Send e-mails. Configuration must be loaded first.

        Returns:
            list: [<success_count>, <failure_count>]
        '''
        count = [0, 0]  # count[0] is success count, count[1] is failure count
        if self.config.resend['enable']:
            if self.config.resend['enable_random_interval']:
                # random interval between 'min_interval' and 'max_interval':
                interval = random.uniform(self.config.resend['min_interval'],
                                          self.config.resend['max_interval'])
            else:
                # fixed interval:
                interval = self.config.resend['fixed_interval']

            for i in range(self.config.resend['times']):
                if self._send_helper(self.config.sender, self.config.receivers,
                                     self.config.mail, self.config.server):
                    count[0] += 1
                else:
                    count[1] += 1
                time.sleep(interval)
        else:
            # send e-mail only once:
            if self._send_helper(self.config.sender, self.config.receivers,
                                 self.config.mail, self.config.server):
                count[0] += 1
            else:
                count[1] += 1
        return count  # count = [<success_count>, <failure_count>]

    def _send_helper(self, sender, receivers, mail, server) -> bool:
        '''Send e-mails to receivers in the list separately.

        Args:
            sender (dict): ['address'(str), 'password'(str), 'alias'(str)]
            receivers (dict): ['address'(str_list), 'alias'(str_list)]
            mail (dict): ['subject'(str), 'body'(str)]
            serve (dict): ['address'(str), 'port'(int)]

        Returns:
            bool: True - successful, False - failed
        '''
        from_user = self._format_address(sender['address'], sender['alias'])
        to_users_list = list()
        if not len(receivers['address']) == len(receivers['alias']):
            raise Exception('Address list and alias name list do not match!')
        else:
            for address_, alias_ in zip(receivers['address'], receivers['alias']):
                to_users_list.append(self._format_address(address_, alias_))

        message = MIMEText(mail['body'], 'plain', 'utf-8')
        message['Subject'] = Header(mail['subject'], 'utf-8').encode()
        message['From'] = from_user
        message['To'] = ','.join(to_users_list)

        try:
            # send e-mails:
            smtp = smtplib.SMTP_SSL(server['address'])
            smtp.connect(server['address'], server['port'])
            smtp.login(sender['address'], sender['password'])
            smtp.sendmail(from_user, to_users_list, message.as_string())
            smtp.close()
            return True
        except Exception as e:
            # print exception when failed:
            print(str(e))
            return False

    def _format_address(self, address, alias) -> str:
        '''Format address like 'Alice<123@abc.xyz>'

        Args:
            address (str): user's address
            alias (str): user's alias name

        Returns:
            str: formatted address
        '''
        if isinstance(alias, str):  # in Python3: unicode is replaced by str
            return formataddr((Header(alias, 'utf-8').encode(),
                              address))  # EXAMPLE: Alice<123@abc.xyz>
        else:
            return address  # EXAMPLE: 123@abc.xyz
