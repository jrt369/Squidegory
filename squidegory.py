'''Currently this simply gives me a list of all unknown websites'''

from collections import Counter, deque
from ConfigParser import SafeConfigParser
import re

def get_category_counter(list, category):
    request_counter = Counter(list)
    test_counter = Counter(open(category[1], 'r').readlines())

    for domain in request_counter.keys()[:]:
        domain_parts = deque(domain.split('.'))
        domain_construction = domain_parts.pop()
        while len(domain_parts) > 0:
            domain_construction = '.'.join((domain_parts.pop(), domain_construction))
            if not test_counter.has_key(domain_construction + '\n'):
                del request_counter[domain]
                break
    return request_counter

def get_unknown_counter(list, categories):
    request_counter = Counter(list)
    for key, value in categories:
        test_counter = Counter(open(value, 'r').readlines())

        for domain in request_counter.keys()[:]:
            domain_parts = deque(domain.split('.'))
            domain_construction = domain_parts.pop()
            while len(domain_parts) > 0:
                domain_construction = '.'.join((domain_parts.pop(), domain_construction))
                if test_counter.has_key(domain_construction + '\n'):
                    del request_counter[domain]
                    break
    return request_counter

def get_categories():
    config = SafeConfigParser()
    config.read(['squidegory.cfg'])
    return config.items('category')

def get_request_list():
    new_request_list = []
    domain_regex = re.compile('^.*http://(.*?)/')
    for line in open('/tmp/access.log', 'r'):
        domain_match = domain_regex.match(line)
        try:
            if len(domain_match.group(1).split('.')) > 1:
                new_request_list.append(domain_match.group(1).strip())
        except AttributeError:
            pass
    return new_request_list

if __name__ == "__main__":
    categories = get_categories()
    request_list = get_request_list()
    print ("total relevant requests: %s" %(len(request_list)))

    unknown_counter = get_unknown_counter(request_list, categories)
    for domain in unknown_counter.most_common():
        print (domain)
    print ("total unique/unknown domains: %s\n\n" %len(unknown_counter))

    for category in categories:
        category_counter = get_category_counter(request_list, category)
        if len(category_counter) > 0:
            print category[0], len(category_counter), category_counter
        else:
            print category[0], len(category_counter)
