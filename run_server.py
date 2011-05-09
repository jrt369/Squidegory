'''Serve Squidegory content: current state of this code really isn't intended to be used.'''

from squidegory import Squidegory

import tornado.ioloop
import tornado.web

class Root(tornado.web.RequestHandler):
    report = Squidegory()

    def get(self):
        self.write("total relevant requests: %s<br><br>" %(len(self.report.request_list)))
        # This is irredeemably long for http -- should pre-generate with ioloop.PeriodicCallback
        unknown_counter = self.report.get_unknown_counter()
        for domain in unknown_counter.most_common():
            self.write(' '.join([domain[0], str(domain[1]), "<br>"]))
        self.write("<br>total unique/unknown domains: %s\n\n" %len(unknown_counter))


application = tornado.web.Application([
    (r"/", Root),
])




if __name__ == "__main__":

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()