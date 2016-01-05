from __future__ import unicode_literals
from itertools import chain
import requests, base64, json

from nbformat import (
  from_dict,
)
from traitlets import (
  Bool,
  Integer,
  Instance,
  HasTraits,
  Unicode
)
from notebook.services.contents.manager import ContentsManager
from tornado import web
from tornado.web import HTTPError

from .api_utils import (
  base_model,
  base_directory_model,
  from_b64,
  reads_base64,
  to_api_path,
  to_b64,
  writes_base64,
)

class HttpManagerMixin(HasTraits):
  base_url = Unicode(
      default_value="http://localhost:3000",
      allow_none=True,
      config=True,
      help="Base connection url",
  )

  user_email = Unicode(
      allow_none=False,
      config=True,
      help="User email address to connect with",
  )

  user_token = Unicode(
      allow_none=False,
      config=True,
      help="User token to connect with",
  )

  def __init__(self, *args, **kwargs):
    super(HttpManagerMixin, self).__init__(*args, **kwargs)
    self.default_headers = {
      "X-User-Email": self.user_email,
      "X-User-Token": self.user_token,
      "Content-Type": "application/json",
      "Accept": "application/json"
    }

class HttpContentsManager(HttpManagerMixin, ContentsManager):

  def __init__(self, *args, **kwargs):
    super(HttpContentsManager, self).__init__(*args, **kwargs)

  def get(self, path, content=True, type=None, format=None):
    "HTTP GET"
    self.log.info("get GET %s %s" % (self.base_url, path))
    b64_path = base64.b64encode(path.encode('utf-8')).decode()
    req = requests.get("%s/%s.jupyter" % (self.base_url, b64_path), headers = self.default_headers)
    if req.status_code == 200:
      data = req.json()
      if not content:
        data['content'] = None
        data['format'] = None
      return data
    else:
      raise HTTPError(404, "No object found at '%s'" % path)
  
  def save(self, model, path):
    "Save a file or directory model to path. HTTP POST/PUT"
    try:
      if self.get(path):
        return self._update(model, path)
    except HTTPError:
      return self._create(model, path)

  def _create(self, model, path):
    self.log.info("create POST %s headers=%s" % (self.base_url, json.dumps(self.default_headers)))
    model['path'] = path
    req = requests.post("%s" % self.base_url, json = {
      'notebook': model
    }, headers = self.default_headers)
    if req.status_code == 200:
      data = req.json()
      data['content'] = None
      data['format'] = None
      return data
    else:
      raise HTTPError(404, "Could not create object at path '%s'" % path)

  def _update(self, model, path):
    b64_path = base64.b64encode(path.encode('utf-8')).decode()
    req = requests.put("%s/%s" % (self.base_url, b64_path), json = {
      'notebook': model
    }, headers = self.default_headers)
    if req.status_code == 200:
      data = req.json()
      data['content'] = None
      data['format'] = None
      return data
    else:
      raise HTTPError(404, "Could not update object at path '%s'" % path)

  def delete_file(self, path):
    "Delete the file or directory at path. HTTP DELETE"
    b64_path = base64.b64encode(path.encode('utf-8')).decode()
    req = requests.delete("%s/%s" % (self.base_url, b64_path), headers = self.default_headers)
    if req.status_code == 200:
      return True
    else:
      return False

  def rename_file(self, old_path, new_path):
    "Rename a file or directory. HTTP PUT"
    b64_path = base64.b64encode(old_path.encode('utf-8')).decode()
    req = requests.put("%s/%s" % (self.base_url, b64_path), data = {
      path: new_path
    }, headers = self.default_headers)
    if req.status_code == 200:
      return True
    else:
      return False

  def file_exists(self, path):
    "Does a file exist at the given path? HTTP GET"
    b64_path = base64.b64encode(path.encode('utf-8')).decode()
    self.log.info("file_exists GET %s %s" % (self.base_url, path))
    req = requests.get("%s/%s" % (self.base_url, b64_path), headers = self.default_headers)
    if req.status_code == 200 and (req.json()['type'] == 'file' or req.json()['type'] == 'notebook'):
      return True
    else:
      return False

  def dir_exists(self, path):
    "Does a directory exist at the given path? HTTP GET"
    b64_path = base64.b64encode(path.encode('utf-8')).decode()
    self.log.info("dir_exists GET %s %s" % (self.base_url, path))
    req = requests.get("%s/%s" % (self.base_url, b64_path), headers = self.default_headers)
    if req.status_code == 200 and req.json()['type'] == 'directory':
      return True
    else:
      return False

  def is_hidden(self, path):
    "??? HTTP GET"
    pass
