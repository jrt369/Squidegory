from collections import Counter, deque
from ConfigParser import SafeConfigParser
import re

class PrettyPrinter:
    def __init__(self):
        pass

    def index(self, counter):
        pass

    def ip_detail(self, counter):
        pass

    def category_detail(self, counter):
        pass

    def category_overview(self, counter):
        pass

    def unknown_overview(self, counter):
        pass

    def ip_overview(self, counter):
        pass

class Squidegory:
    def __init__(self):
        self.reload()

    def reload(self):
        self.categories = self.get_categories()
        self.request_list = self.get_request_list()

    def get_category_counter(self, category):
        request_counter = Counter(self.request_list)
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

    def get_unknown_counter(self):
        request_counter = Counter(self.request_list)
        for key, value in self.categories:
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

    def get_categories(self):
        config = SafeConfigParser()
        config.read(['squidegory.cfg'])
        return config.items('category')

    def get_request_list(self):
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
    analyze = Squidegory()
    print("total relevant requests: %s" %(len(analyze.request_list)))

    unknown_counter = analyze.get_unknown_counter()
    for domain in unknown_counter.most_common():
        print(domain)
    print("total unique/unknown domains: %s\n\n" %len(unknown_counter))

    for category in analyze.categories:
        category_counter = analyze.get_category_counter(category)
        if len(category_counter) > 0:
            print(category[0], len(category_counter), category_counter)
        else:
            print(category[0], len(category_counter))
