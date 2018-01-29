from time import gmtime, strftime

class Dweet:
    def __init__(self, thing, content):
        date = strftime("%y-%d-%mT%H:%M:%SZ", gmtime())
        self.thing = thing
        self.created = date
        self.content = content

    def __dict__(self):
        return dict(
            thing=self.thing,
            created=self.created,
            content=self.content
        )
