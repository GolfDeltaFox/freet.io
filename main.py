import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from model.dweet import Dweet


from tornado.options import define, options

define("port", default=80, type=int)

dweets = {}

def get_last_dweet(thing):
    return json.dumps(dweets[thing][-1])

def get_last_dweets(thing, size=100):
    size = min(size, len(dweets[thing]))
    print(size)
    return dweets[thing][-size:]

def save_dweet(thing, content):
    dweet = Dweet(thing, content)
    if thing in dweets:
        dweets[thing].append(dweet)
    else:
        dweets[thing] = [dweet]
    return dweet


class PostDweet(tornado.web.RequestHandler):
    def post(self, thing):
        try:
            content = tornado.escape.json_decode(self.request.body)
            dweet = save_dweet(thing, content)
            response = {
              "this": "succeeded",
              "by": "dweeting",
              "the": "dweet",
              "with": [dweet.__dict__()]
            }

            self.write(response)
        except json.decoder.JSONDecodeError:
            self.set_status(400)
            self.finish("Bad JSON.")

class GetDweet(tornado.web.RequestHandler):
    def get(self, thing):
        try:
            dweet = get_last_dweet(thing)
            response = {
              "this": "succeeded",
              "by": "getting",
              "the": "dweets",
              "with": [dweet.__dict__()]
            }
            self.write(response)
        except:
            self.set_status(404)
            self.finish("No dweet found.")

class GetDweets(tornado.web.RequestHandler):
    def get(self, thing):
        try:
            print("tab")
            dweets = get_last_dweets(thing)
            response = {
              "this": "succeeded",
              "by": "getting",
              "the": "dweets",
              "with": [dweet.__dict__() for dweet in dweets]
            }
            self.write(response)
        except:
            self.set_status(404)
            self.finish("No dweet found.")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/dweet/for/([^/]+)", PostDweet),
        (r"/get/latest/dweet/for/([^/]+)", GetDweet),
        (r"/get/dweets/for/([^/]+)", GetDweets),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
