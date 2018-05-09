#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import sys
import traceback
from bs4 import BeautifulSoup
from lxml import etree
import tldextract


class DiscoverBroDomain(object):
    def __init__(self):
        self.basic_api = "http://whois.chinaz.com/{}/"
        self.reverse_email_api = "http://whois.chinaz.com/reverse?host={}&ddlSearchMode=1"
        self.reverse_registrant_api = "http://whois.chinaz.com/reverse?host={}&ddlSearchMode=2"
        self.reverse_phone_api = "http://whois.chinaz.com/reverse?host={}&ddlSearchMode=3"
        self.statistics_api = "https://icp.aizhan.com/{}/"
        self.iptodomain_api = "https://dns.aizhan.com/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
        }
        self.result = set()
        self.email = set()

    def getBasicWhoisInfo(self, domain):
        registrant, email, phone = None, None, None
        try:
            r = requests.get(self.basic_api.format(domain), headers=self.headers, timeout=15)
            soup = BeautifulSoup(r.content, 'lxml')
            hand = soup.find('div', class_="WhoisWrap clearfix")
            try:
                registrant = \
                    re.findall('联系人</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>', str(hand))[
                        0]
            except:
                registrant = ''
            try:
                email = \
                    re.findall('联系邮箱</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>',
                               str(hand))[0]
            except:
                email = ''
            try:
                phone = \
                    re.findall('联系电话</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>',
                               str(soup))[0]
            except:
                phone = ''
        except:
            traceback.print_exc()
        finally:
            return registrant, email, phone

    def getDomainByEmail(self, email):
        print "[+] Get domains by email:{}".format(email)
        try:
            r = requests.get(self.reverse_email_api.format(email), headers=self.headers, timeout=15)
            self.result = self.result | {domain.text for domain in
                                         BeautifulSoup(r.text, 'lxml').find(id="ajaxInfo").find_all('a') if
                                         re.match(r'\w+\.\w+', domain.text)}
        except:
            traceback.print_exc()

    def getDomainByregistrant(self, registrant):
        print "[+] Get domains by registrant:{}".format(registrant)
        try:
            r = requests.get(self.reverse_registrant_api.format(registrant), headers=self.headers, timeout=15)
            domain = re.findall(r'<a href="/(.+?)" target', r.text)
            email = re.findall(r'[\w\-]+\@[\w\-]+\.\w+', r.text)
            for i in domain: self.result.add(i)
            for j in email: self.email.add(j)
        except:
            traceback.print_exc()

    def getDomainByPhone(self, phone):
        print "[+] Get domains by phone:{}".format(phone)
        try:
            r = requests.get(self.reverse_phone_api.format(phone), headers=self.headers, timeout=15)
            domain = re.findall(r'<a href="/(.+?)" target', r.text)
            email = re.findall(r'[\w\-]+\@[\w\-]+\.\w+', r.text)
            for i in domain: self.result.add(i.strip())
            for j in email: self.email.add(j.strip())
        except:
            traceback.print_exc()

    def getDomainByStatistics(self, domain):
        print "[+] Get domains by statistics"
        try:
            r = requests.get(self.statistics_api.format(domain), headers=self.headers, timeout=15)
            html = etree.HTML(r.content)
            result = html.xpath(""".//*[@id='company']/table/tbody/tr/td/span[@class="blue"]/text()""")
            for i in result: self.result.add(i.strip())
        except:
            traceback.print_exc()

    def IPtoDomain(self, ip):
        domains = set()
        try:
            r = requests.get(self.iptodomain_api.format(ip), headers=self.headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            hand = soup.find_all("td", class_="domain")
            for i in xrange(1, len(hand)):
                p = tldextract.extract(hand[i].find("a").get_text())
                domains.add('.'.join(p[1:]))
        except:
            traceback.print_exc()
        finally:
            return domains

    def main(self, address):
        domains = set()
        try:
            ip_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.$')
            domain_regex = re.compile(
                r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', re.IGNORECASE)
            if ip_regex.match(address):
                domains = self.IPtoDomain(ip=address)
            elif domain_regex.match(address):
                domains.add(address)
            else:
                return

            for domain in domains:
                registrant, email, phone = self.getBasicWhoisInfo(domain)
                print "[+] Init Registrant:[\033[31m{}\033[0m],Email:[\033[31m{}\033[0m],Phone:[\033[31m{}\033[0m]".format(
                    registrant, email, phone)
                if email: self.getDomainByEmail(email=email)
                if registrant: self.getDomainByregistrant(registrant=registrant)
                if phone: self.getDomainByPhone(phone=phone)
                if self.email:
                    with open('email.txt', 'w+') as fw:
                        for each in self.email:
                            self.getDomainByEmail(email=each)
                            fw.write(each.strip() + '\n')
                if self.result:
                    with open('domains.txt', 'w+') as fw:
                        for each in self.result:
                            fw.write(each.strip() + '\n')
        except:
            traceback.print_exc()
        finally:
            print "[+] Done,total [\033[36m{}\033[0m] domains and [\033[36m{}\033[0m] emails.".format(
                len(self.result), len(self.email))


if __name__ == "__main__":
    banner = """
          _____  _                             ____            _____                        _       
         |  __ \(_)                           |  _ \          |  __ \                      (_)      
         | |  | |_ ___  ___ _____   _____ _ __| |_) |_ __ ___ | |  | | ___  _ __ ___   __ _ _ _ __  
         | |  | | / __|/ __/ _ \ \ / / _ | '__|  _ <| '__/ _ \| |  | |/ _ \| '_ ` _ \ / _` | | '_ \ 
         | |__| | \__ | (_| (_) \ V |  __| |  | |_) | | | (_) | |__| | (_) | | | | | | (_| | | | | |
         |_____/|_|___/\___\___/ \_/ \___|_|  |____/|_|  \___/|_____/ \___/|_| |_| |_|\__,_|_|_| |_|
                                                                     Coded By Coco413 (v1.0 RELEASE)                                                                                                                                                                                                                                                                                              
        """
    print banner
    hand = DiscoverBroDomain()
    if not len(sys.argv) < 2:
        hand.main(sys.argv[1])
    else:
        print "[+] Please input ip or domain.."
