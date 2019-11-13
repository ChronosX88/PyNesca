#!/usr/bin/env python
# -*- coding:utf-8 -*-

from core.prototypes.AbstractScanner import AbstractScanner
import ftplib
from ftplib import FTP

MAX_ERRORS = 3


class FTPScanner(AbstractScanner):
    def __init__(self, timeout:"timeout", credentials:"credentials"):
        self.__timeout__ = timeout
        self.__credantials__ = credentials

    def scan_address(self, host: 'ipv4_str', port: 'port') -> {'ftp_version', 'ftp_status', 'login', 'password'}:
        result = self.ftp_anonymous_login(host, port, self.__timeout__)
        if result['ftp_status'] == 'ok':
            #Что-то делать с ошибками
            return result
        if not result['ftp_status'].startswith('530'):
            return result
        return self.ftp_bruteforce(
            host, port, self.__credentials__, self.__timeout__)

    @staticmethod
    def ftp_anonymous_login(host, port, timeout):
        '''Get version and check if anonympous login is enabled'''
        result = {
                key:None for key in ['ftp_version', 'ftp_status', 'login',
                'password']
                }
        ftp_connection = FTP(timeout=timeout)
        try:
            version = ftp_connection.connect(host=host, port=port)
            # Get something like "220 Twisted 16.6.0 FTP Server"
            result['ftp_version'] = version.lstrip('220 ')
            # Try to login as anonymous user
            ftp_connection.login()
            result['ftp_status'] = 'ok'
        except ftplib.error_perm as e:
            if str(e).startswith("530"):
                result['ftp_status'] = 'ok'
                result['anonymous_login'] = False
        except ftplib.all_errors as e:
            #status - error
            result['ftp_status'] = str(e)
            return result
        finally:
            ftp_connection.close()
            return result

    @staticmethod
    def ftp_bruteforce(host, port, creds, timeout):
        '''Attempt to brute force login/password pair'''
        # We want maintain connection to speed up bruteforce
        # but we also want to reconnect if necessary.
        # That is why I use cred iterator to pick up new login/pass only when
        # we need to.
        result = {
                key:None for key in ['ftp_version', 'ftp_status', 'login',
                'password']
                }
        result['ftp_status'] = "error"
        error_count = 0
        it = iter(creds)
        cred = next(it, "")
        ftp_connection = FTP(timeout=timeout)
        while error_count < MAX_ERRORS:
            try:
                # Connecting to server
                ftp_connection.connect(host=host, port=port)
                while cred and error_count < MAX_ERRORS:
                    user, password = cred
                    # Trying to log in
                    try:
                        ftp_connection.login(user, password)
                        ftp_connection.close()
                        result['ftp_status'] = 'ok'
                        result['login'] = user
                        result['password'] = password
                        return result
                    except ftplib.error_perm as e:
                        # Password was wrong, checking another
                        cred = next(it, "")
                        continue
                    except ftplib.all_errors as e:
                        error_count += 1
                        # Connection was dropped or another network error happened
                        # We must connection, error_count would help us to
                        # avoid deadlock on mumbling host
                        break
            except ftplib.all_errors as e:
                # Cannot reconnect, give up
                break
            finally:
                ftp_connection.close()
        return result
