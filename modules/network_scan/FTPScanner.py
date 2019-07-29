#!/usr/bin/env python
# -*- coding:utf-8 -*-

from core.prototypes.AbstractScanner import AbstractScanner
import ftplib
from ftplib import FTP

MAX_ERRORS = 3


class FTPScanner(AbstractScanner):
    def __init__(self, timeout):
        self.__timeout__ = timeout

    def scan_address(self, host: 'ipv4_str or hostname', port: 'port', credentials: 'tuples with login and password') -> {'scan_result'}:
        result = self.ftp_anonymous_login(host, port, self.__timeout__)
        if result['status'] == 'error' or result['anonymous_login']:
            return result
        result['credentials'] = self.ftp_bruteforce(
            host, port, credentials, self.__timeout__)
        return result

    @staticmethod
    def ftp_anonymous_login(host, port, timeout):
        '''Get version and check if anonympous login is enabled'''
        result = {}
        ftp_connection = FTP(timeout=timeout)
        try:
            version = ftp_connection.connect(host=host, port=port)
            # Get something like "220 Twisted 16.6.0 FTP Server"
            result['ftp_version'] = version.lstrip('220 ')
            # Try to login as anonymous user
            ftp_connection.login()
            result['anonymous_login'] = True
            result['status'] = 'ok'
        except ftplib.error_perm as e:
            if str(e).startswith("530"):
                result['status'] = 'ok'
                result['anonymous_login'] = False
        except ftplib.all_errors as e:
            result['status'] = 'error'
            result['error_type'] = str(e)
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
                        return user, password
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
        return None
