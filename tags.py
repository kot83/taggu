from google.cloud import firestore
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'

db = firestore.Client()

async def get_tags(guild: str):
    tags = db.collection(u'taggu').document(u'tags').collection('guilds').document(guild)
    doc = tags.get()
    return doc.to_dict()

async def edit_tag(guild: str, tag: dict):
    try:
        tags = db.collection(u'taggu').document(u'tags').collection('guilds').document(guild)
        name = tag['name']
        taglist = tags.get().to_dict()
        taglist[name] = {'content': tag['content'], 'author': tag['author'], 'timestamp': tag['timestamp']}
        tags.set(taglist)
        
    except Exception as e:
        raise Exception(e)
    
    return True

async def del_tag(guild: str, tag: str):
    tags = db.collection(u'taggu').document(u'tags').collection('guilds').document(guild)
    taglist = tags.get().to_dict()
    del taglist[tag]
    tags.set(taglist)

async def initiate_guild(guild: str, tag: dict):
    tags = db.collection(u'taggu').document(u'tags').collection('guilds').document(guild)
    taglist = {}
    taglist['help'] = {'content': 'use `t help tag` for more info', 'author': tag['author'], 'timestamp': tag['timestamp']}
    tags.set(taglist)
