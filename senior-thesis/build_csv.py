import csv
from crawl_cogent_2 import get_cogent_dict
from crawl_firstlight_2 import get_firstlight_dict
from crawl_hurricane_2 import get_hurricane_dict
from crawl_internet2_2 import get_internet2_dict
from crawl_NYSER_2 import get_NYSER_dict
from crawl_Zayo_2 import get_Zayo_dict

with open('train_test_data.csv', mode='w') as csv_file:
    #fieldnames = ['net(work) neutral', 'support net(work) neutrality', 'practice net(work) neutrality', 'is/are net(work) neutral']
    fieldnames = ["network neutral", "net neutral", "support net neutral", "practice net neutral", "support network neutral", "practice network neutral", "be net neutral", "be network neutral"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    
    cogent = get_cogent_dict()
    firstlight = get_firstlight_dict()
    hurricane = get_hurricane_dict()
    internet2 = get_internet2_dict()
    nyser = get_NYSER_dict()
    zayo = get_Zayo_dict()

    writer.writerow(cogent)
    writer.writerow(firstlight)
    writer.writerow(hurricane)
    writer.writerow(internet2)
    writer.writerow(nyser)
    writer.writerow(zayo)