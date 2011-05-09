'''Serve Squidegory content: current state of this code really isn't intended to be used.'''

from squidegory import Squidegory

import tornado.ioloop
import tornado.web

class Root(tornado.web.RequestHandler):

    def get(self):
        self.write("total relevant requests: %s<br><br>" %(len(report.request_list)))

        for domain in report.unknown_counter.most_common():
            self.write(' '.join([domain[0], str(domain[1]), "<br>"]))
        self.write("<br>total unique/unknown domains: %s\n\n" %len(report.unknown_counter))


report = Squidegory()
update = tornado.ioloop.PeriodicCallback(report.update_unknown_counter, 60000)
update.start()
application = tornado.web.Application([(r"/", Root),])

if __name__ == "__main__":

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()