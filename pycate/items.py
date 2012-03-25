from scrapy.item import Item, Field

class Identity(Item):
    first_name  = Field()
    last_name   = Field()
    course      = Field()
    cid         = Field()
    tutor_name  = Field() 
    tutor_login = Field()

class Course(Item):
    name       = Field()
    code       = Field()

class Note(Item):
    title      = Field()
    url        = Field()
    note_type  = Field()
