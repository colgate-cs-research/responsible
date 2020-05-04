import dns.resolver
import ipaddress
from ipwhois import IPWhois


# these are the destinations of interest
domains = ['netflix.com','google.com', 'microsoft.com','facebook.com', 'doubleclick.net']

resolver = dns.resolver.Resolver()

asn_dict = dict()
string = '-p'

# get paths; format string to pass into bgpscanner as specific in man page
for domain in domains:
    answer = resolver.query(domain , "A")
    for ans in answer:
        obj = IPWhois(ans)
        res= obj.lookup_whois()
        net_name = res['nets'][0]['description']
        if res['asn'] not in asn_dict.keys():
            asn_dict[res['asn']] = net_name
            string += ' \"' + str(res['asn']) + '$\" -p'

string = string[:-2]
print(asn_dict)
print(string) # this gets copied and pasted into terminal with bgpscanner command and filename



