#import important file
from instagrambot import instagramBot
from instagrambot import smart_run
from instagrambot import set_workspace


set_workspace(path=none)

session = instagramBot()

with smart_run(session):
    #public settings
    sessions.set_dont_include(["friend1","friend2","friend3"])

    #activity bots
    session.like_by_tags(["natgeo"], amount=10)
