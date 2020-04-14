import dns.resolver
import ipaddress
from ipwhois import IPWhois

domains = ['netflix.com','google.com', 'microsoft.com','facebook.com', 'doubleclick.net']

resolver = dns.resolver.Resolver()

asn_list = []

for domain in domains:
    answer = resolver.query(domain , "A")
    for ans in answer:
        obj = IPWhois(ans)
        res= obj.lookup_whois()
        if res['asn'] not in asn_list:
            asn_list.append(res['asn'])

print(asn_list)



