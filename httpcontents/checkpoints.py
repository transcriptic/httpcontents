"""
An IPython FileContentsManager that uses Postgres for checkpoints.
"""
from __future__ import unicode_literals
from notebook.services.contents.checkpoints import GenericCheckpointsMixin
from notebook.services.contents.manager import Checkpoints
from .manager import HttpManagerMixin
from .api_utils import (
    _decode_unknown_from_base64,
    prefix_dirs,
    reads_base64,
    to_b64,
    writes_base64
)
import requests

class HttpCheckpoints(HttpManagerMixin, GenericCheckpointsMixin, Checkpoints):
    """
    A Checkpoints implementation that saves checkpoints to a remote database.
    """

    def create_file_checkpoint(self, content, format, path):
        """Create a checkpoint of the current state of a file

        Returns a checkpoint_id for the new checkpoint.
        """
        try:
            b64_content = to_b64(content, format)
        except ValueError as e:
            raise HTTPError(404, str(e))
        # with self.engine.begin() as db:
        #     return save_remote_checkpoint(db, self.user_id, path, b64_content)


    def create_notebook_checkpoint(self, nb, path):
        """Create a checkpoint of the current state of a notebook

        Returns a checkpoint_id for the new checkpoint.
        """
        # b64_content = writes_base64(nb)
        # with self.engine.begin() as db:
        #     return save_remote_checkpoint(db, self.user_id, path, b64_content)
        return {
          'id': "foo.ipynb"
        }

    def get_file_checkpoint(self, checkpoint_id, path):
        return
        # b64_content = self._get_checkpoint(checkpoint_id, path)
        # content, format = _decode_unknown_from_base64(path, b64_content)
        # return {
        #     'type': 'file',
        #     'content': content,
        #     'format': format,
        # }

    def get_notebook_checkpoint(self, checkpoint_id, path):
        return
        # b64_content = self._get_checkpoint(checkpoint_id, path)
        # with self.engine.begin() as db:
        #     return get_remote_checkpoint(
        #         db,
        #         self.user_id,
        #         path,
        #         checkpoint_id,
        #     )['content']
        # return {
        #     'type': 'notebook',
        #     'content': reads_base64(b64_content),
        # }

    def delete_checkpoint(self, checkpoint_id, path):
        """delete a checkpoint for a file"""
        return
        # with self.engine.begin() as db:
        #     return delete_single_remote_checkpoint(
        #         db, self.user_id, path, checkpoint_id,
        #     )

    def list_checkpoints(self, path):
        return []
        # """Return a list of checkpoints for a given file"""
        # with self.engine.begin() as db:
        #     return list_remote_checkpoints(db, self.user_id, path)

    def rename_checkpoint(self, checkpoint_id, old_path, new_path):
      pass
