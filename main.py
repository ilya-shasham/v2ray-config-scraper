from bs4 import BeautifulSoup
from requests import get
from threading import Thread
from time import sleep

print("Gathering proxy list...")

proxies = BeautifulSoup(get("https://vpn.fail/free-proxy").text).find_all("article")
v2ray_proxies = []

for proxy in proxies:
    proxy_type = str(proxy.find_all("div")[1].text)
    
    if proxy_type.lower().replace("\n", "").replace(" ", "").replace("\r", "") == "v2ray":
        v2ray_proxies.append(proxy)

print("Done.")

for i in v2ray_proxies:
    print(i.find_all("a"))

proxy_info_links = [proxy.find_all("a")[0].attrs["href"] for proxy in v2ray_proxies]
connection_links = [None for i in range(len(proxy_info_links))]

def get_connection_link(proxy_info_link: str, index: int):
    connection_links[index] = BeautifulSoup(get(proxy_info_link).text).find_all("input")[0].attrs["value"]

print("Gathering connection links...")

thread_pool = [Thread(target=get_connection_link, args=(proxy_info_links[i], i)) for i in range(len(proxy_info_links))]

for thread in thread_pool:
    thread.start()
    sleep(0.5)
    
for thread in thread_pool:
    thread.join()

print("Done.")

open("results.txt", "w").write("\n".join(connection_links))