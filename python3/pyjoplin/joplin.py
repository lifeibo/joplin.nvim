#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests

from .node import FolderNode, NoteNode, ResourceNode, TagNode, factory_node


class Joplin(object):
    """Joplin operation"""
    def __init__(self, token, url):
        self.token = token
        self.base_url = url

    def ping(self):
        """Testing if the service is available
        :returns: bool

        """
        url = self.base_url + '/ping'
        succ = False
        try:
            r = requests.get(url)
            succ = r.status_code == 200 and r.text == 'JoplinClipperServer'
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
        except Exception:
            print('Joplin: joplin.app error')
        return succ

    def search(self, query, typ=None):
        """search data

        :query: the keyword to search
        :typ: search special type
        :returns: search nodes

        """
        path = '/search'
        kwargs = {'query': query}
        if typ is not None:
            kwargs['type'] = typ

        nodes = self._get_by_path(factory_node, path, **kwargs)
        nodes = list(filter(lambda node: node is not None, nodes))
        return nodes

    def _get_by_path_page(self, cls, path, page, **kwargs):
        url = '%s%s?token=%s&page=%d' % (self.base_url, path, self.token, page)
        for k, v in kwargs.items():
            url += '&%s=%s' % (k, str(v))

        # fetch all data with body
        # the body is to large and useless
        if cls != factory_node:
            fields = list(filter(lambda field: field != 'body',
                                 cls().fields()))
            fields_str = ','.join(fields)
            url += '&fields=' + fields_str
        json = {}
        try:
            r = requests.get(url)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None, False
            json = r.json()
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return None, False
        except Exception:
            print('Joplin: joplin.app error')
            return None, False
        items = json['items']
        has_more = json['has_more']
        objects = list([cls(**item) for item in items])
        return objects, has_more

    def _get_by_path(self, cls, path, **kwargs):
        page = 1
        has_more = True
        objects = []
        while has_more:
            cur, has_more = self._get_by_path_page(cls, path, page, **kwargs)
            if cur is None:
                break
            page += 1
            objects += cur
        return objects

    def get_all(self, cls, order_by='updated_time', order_dir='DESC'):
        """Gets all cls' objects

        :cls: the object type
        :returns: ojbects and has_more if success else None

        """
        return self._get_by_path(cls,
                                 '/' + cls.path(),
                                 order_by=order_by,
                                 order_dir=order_dir)

    def get(self, cls, id, except_fields=[]):
        """Get cls' object

        :cls: the object type
        :id: the id to get
        :returns: object if success else None

        """
        fields = cls().fields()
        fields = list(filter(lambda field: field not in except_fields, fields))
        fields_str = ','.join(fields)
        url = '%s/%s/%s?token=%s&fields=%s' % (self.base_url, cls.path(), id,
                                               self.token, fields_str)
        json = {}
        try:
            r = requests.get(url)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None
            json = r.json()
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return None
        except Exception:
            print('Joplin: joplin.app error')
            return None
        return cls(**json)

    def post(self, o):
        """Create a new object

        :o: the object to create
        :returns: the created object

        """
        url = '%s/%s?token=%s' % (self.base_url, o.path(), self.token)
        json = {}
        try:
            r = requests.post(url, json=o.dict())
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None
            json = r.json()
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return None
        except Exception:
            print('Joplin: joplin.app error')
            return None
        return o.new(**json)

    def put(self, o):
        """Sets the properties of the object

        :o: the object to update
        :returns: new object
        """
        url = '%s/%s/%s?token=%s' % (self.base_url, o.path(), o.id, self.token)
        json = {}
        try:
            r = requests.put(url, json=o.dict())
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None
            json = r.json()
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return None
        except Exception:
            print('Joplin: joplin.app error')
            return None
        return o.new(**json)

    def delete(self, cls, id):
        """delete object with id

        :cls: the object type
        :arg1: the id to delete
        :returns:

        """
        url = '%s/%s/%s?token=%s' % (self.base_url, cls.path(), id, self.token)
        try:
            r = requests.delete(url)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
        except Exception:
            print('Joplin: joplin.app error')

    def get_note_tags(self, id):
        """Gets all the tags attached to this note

        :id: note's id
        :returns: TagNodes, has_more

        """
        path = '/notes/%s/tags' % id
        return self._get_by_path(TagNode, path)

    def get_note_resources(self,
                           id,
                           order_by='updated_time',
                           order_dir='DESC'):
        """Gets all the resources attached to this note

        :id: note's id
        :returns: ResourceNodes

        """
        path = '/notes/%s/resources' % id
        return self._get_by_path(ResourceNode,
                                 path,
                                 order_by=order_by,
                                 order_dir=order_dir)

    def get_folder_notes(self, id, order_by='updated_time', order_dir='DESC'):
        """Gets all notes inside this folder

        :id: folder's id
        :returns: NoteNode

        """
        path = '/folders/%s/notes' % id
        return self._get_by_path(NoteNode,
                                 path,
                                 order_by=order_by,
                                 order_dir=order_dir)

    def get_resource_file(self, id):
        """Gets the actual file associated with this resource

        :id: resource's id
        :returns: file text

        """
        url = '%s/resources/%s/file?token=%s' % (self.base_url, id, self.token)
        text = ''
        try:
            r = requests.get(url)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None
            text = r.text
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return ''
        except Exception:
            print('Joplin: joplin.app error')
            return ''
        return text

    def get_resource_notes(self,
                           id,
                           order_by='updated_time',
                           order_dir='DESC'):
        """Gets the notes associated with the resource with id

        :id: resource's id
        :returns: notes' id

        """
        path = '/resources/%s/notes' % id
        return self._get_by_path(NoteNode,
                                 path,
                                 order_by=order_by,
                                 order_dir=order_dir)

    def post_resource(self, filename, resource):
        """Creates a new resource

        :resource: the resource to create
        :returns: resource

        """
        url = '%s/resources?token=%s' % (self.base_url, self.token)
        payload = {
            'props': json.dumps(resource.dict()),
        }
        j = {}
        try:
            r = requests.post(url,
                              files={'data': open(filename, 'rb')},
                              data=payload)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
                return None
            j = r.json()
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
            return None
        except Exception as e:
            print('Joplin: joplin.app error', e)
            return None
        return ResourceNode(**j)

    def get_tag_notes(self, id, order_by='updated_time', order_dir='DESC'):
        """Gets all the notes with this tag

        :id: tag's id
        :returns: None

        """
        path = '/tags/%s/notes' % id
        return self._get_by_path(NoteNode,
                                 path,
                                 order_by=order_by,
                                 order_dir=order_dir)

    def post_tag_note(self, id, note_id):
        """Post a note to this endpoint to add the tag to the note.

        :id: tag id
        :note_id: note id
        :returns: None

        """
        url = '%s/tags/%s/notes?token=%s' % (self.base_url, id, self.token)
        payload = {'id': note_id}
        try:
            r = requests.post(url, json=payload)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
        except Exception:
            print('Joplin: joplin.app error')

    def delete_tag_note(self, id, note_id):
        """Remove the tag from the note

        :id: tag id
        :note_id: note_id
        :returns: None

        """
        url = '%s/tags/%s/notes/%s?token=%s' % (self.base_url, id, note_id,
                                                self.token)
        try:
            r = requests.delete(url)
            if r.status_code != 200:
                print('Joplin:', url, r.status_code, r.text)
        except requests.ConnectionError:
            print('Joplin: joplin.app not available')
        except Exception:
            print('Joplin: joplin.app error')

    def node_path(self, node):
        if node is None or node.type_ not in [1, 2]:
            return ''

        path = [node.title]
        cur = node
        while cur.parent_id != '':
            cur = self.get(FolderNode, cur.parent_id)
            if cur is not None:
                path.append(cur.title)

        path = reversed(path)
        return '/'.join(path)
