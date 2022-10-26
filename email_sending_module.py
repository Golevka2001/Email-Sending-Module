#!user/bin/env python
# -*- coding:utf-8 -*-
'''email_sending_module.py: a module used to send e-mails,\
    providing more convenience.
@Author: Gol3vka<gol3vka@163.com>
@Version: 2.1.2
@Created Date: 2022/05/16
@Last Modified Date: 2022/10/26
'''
# TODO: make adding appendix available. (MIMEMultipart)
# TODO: now all recipients are display in the field 'TO', make them hidden.

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
        _send_helper()
        _format_address()
    '''

    def __init__(self) -> None:

        class Configuration:
            '''Configuration of e-mail sending module.

            Vars:
                sender (dict): {'address'(str), 'password'(str),\
                    [OPTIONAL]'alias'(str)}
                recipients (dict): {'address'(str or list),\
                    [OPTIONAL]'alias'(str or list)}
                mail (dict): {'subject'(str), 'body'(str)}
                server (dict): {'address'(str), 'port'(int)}
                [OPTIONAL]resend (dict): {'enable'(bool), 'times'(int),\
                    'enable_random_interval'(bool), 'min_interval'(int),\
                    'max_interval'(int), 'fixed_interval'(int)}

            Functions:
                load_from_file()
                load_from_parameters()
            '''

            def load_from_file(self, config_path: str) -> None:
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
                    self.recipients = config['recipients_information']
                    self.mail = config['mail']
                    self.server = config['server_information']
                    # 'resend_options' is optional, set a default value:
                    if 'resend_options' in config:
                        self.resend = config['resend_options']
                    else:
                        self.resend = {'enable': False}

            def load_from_parameters(
                    self,
                    sender_information: dict,
                    recipients_information: dict,
                    mail: dict,
                    server_information: dict,
                    resend_options: dict = {'enable': False}) -> None:
                '''Load configuration from these parameters.

                Args:
                    sender_information (dict): {'address'(str),\
                        'password'(str), [OPTIONAL]'alias'(str)}
                    recipients_information (dict): {'address'(str or list),\
                        [OPTIONAL]'alias'(str or list)}
                    mail (dict): {'subject'(str), 'body'(str)}
                    server_information (dict): {'address'(str), 'port'(int)}
                    [OPTIONAL]resend_options (dict): {'enable'(bool),\
                        'times'(int), 'enable_random_interval'(bool),\
                        'min_interval'(int), 'max_interval'(int),\
                        'fixed_interval'(int)}
                '''
                # assign:
                self.sender = sender_information
                self.recipients = recipients_information
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
            times_ = self.config.resend['times']
        else:
            times_ = 1

        for i in range(times_):
            if self._send_helper(self.config.sender, self.config.recipients,
                                 self.config.mail, self.config.server):
                if isinstance(self.config.recipients['address'], list):
                    count[0] += len(self.config.recipients['address'])
                else:
                    count[0] += 1
                print('['+str(count[0]+count[1])+'] Successful')
            else:
                if isinstance(self.config.recipients['address'], list):
                    count[1] += len(self.config.recipients['address'])
                else:
                    count[1] += 1
                print('['+str(count[0]+count[1])+'] Failed')
            if times_ > 1:
                time.sleep(interval)
        return count  # count = [<success_count>, <failure_count>]

    def _send_helper(self, sender: dict, recipients: dict, mail: dict,
                     server: dict) -> bool:
        '''Send e-mails to recipients in the list separately.

        Args:
            sender (dict): ['address'(str), 'password'(str),\
                [OPTIONAL]'alias'(str)]
            recipients (dict): ['address'(str_list),\
                [OPTIONAL]'alias'(str_list)]
            mail (dict): ['subject'(str), 'body'(str)]
            serve (dict): ['address'(str), 'port'(int)]

        Returns:
            bool: True - successful, False - failed
        '''
        # format address of sender
        if 'alias' in sender:
            from_user = self._format_address(sender['address'],
                                             sender['alias'])
        else:
            from_user = self._format_address(sender['address'])

        # format addresses of recipients
        to_users_list = list()
        if isinstance(recipients['address'], str):
            # only one recipient:
            if 'alias' in recipients:
                to_users_list.append(
                    self._format_address(recipients['address'],
                                         recipients['alias']))
            else:
                to_users_list.append(
                    self._format_address(recipients['address']))
        elif isinstance(recipients['address'], list):
            # only one or more than one recipient:
            if 'alias' in recipients:
                if not len(recipients['address']) == len(recipients['alias']):
                    raise Exception(
                        'Address list and alias name list do not match!')
                else:
                    for address_, alias_ in zip(recipients['address'],
                                                recipients['alias']):
                        to_users_list.append(
                            self._format_address(address_, alias_))
            else:
                for address_ in recipients['address']:
                    to_users_list.append(self._format_address(address_))

        # compose e-mail:
        message = MIMEText(mail['body'], 'plain', 'utf-8')
        message['Subject'] = Header(mail['subject'], 'utf-8').encode()
        message['From'] = from_user
        message['To'] = ','.join(to_users_list)

        try:
            # send e-mails:
            smtp = smtplib.SMTP_SSL(
                server['address'])  # if SSL is not supported, delete '_SSL'
            smtp.connect(server['address'], server['port'])
            smtp.login(sender['address'], sender['password'])
            smtp.sendmail(from_user, to_users_list, message.as_string())
            smtp.close()
            return True
        except Exception as e:
            # print exception when failed:
            print(str(e))
            return False

    def _format_address(self, address: str, alias: str = None) -> str:
        '''Format address like 'Alice<123@abc.xyz>'

        Args:
            address (str): user's address
            [OPTIONAL]alias (str): user's alias name

        Returns:
            str: formatted address
        '''
        if isinstance(alias, str):
            return formataddr((Header(alias, 'utf-8').encode(),
                               address))  # EXAMPLE: Alice<123@abc.xyz>
        else:
            return address  # EXAMPLE: 123@abc.xyz
