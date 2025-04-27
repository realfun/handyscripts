#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# 一个来回切换代理服务器的小脚本
#   用Chrome，切换代理不方便，--proxy-server好像也不顶用
# 
# 使用方法:
#   proxytoggle 127.0.0.1:8118
#   执行一次开启，再执行就关闭，再执行又开启，循环往复
#
# 有自己主机的，可以用Tohr Proxy:
#   http://blog.solrex.cn/articles/tohr-the-onion-http-router.html
#
import struct
import _winreg
import sys

#proxy = sys.argv[1]
proxy = "127.0.0.1:8118"
root = _winreg.HKEY_CURRENT_USER
proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
kv_Enable = [
  (proxy_path, "ProxyEnable", 1, _winreg.REG_DWORD),
  (proxy_path, "ProxyServer", proxy, _winreg.REG_SZ),
]

kv_Disable = [
  (proxy_path, "ProxyEnable", 0, _winreg.REG_DWORD),
  (proxy_path, "ProxyServer", proxy, _winreg.REG_SZ),
]

hKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, proxy_path)
value, type = _winreg.QueryValueEx(hKey, "ProxyEnable")
kv = kv_Enable
result = "Enabled"
if value:
    result = "Disabled"
    kv = kv_Disable

for keypath, value_name, value, value_type in kv:
    hKey = _winreg.CreateKey (root, keypath)
    _winreg.SetValueEx (hKey, value_name, 0, value_type, value)

print result

