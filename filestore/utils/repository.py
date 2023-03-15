from datetime import datetime
from filestore.models.dbmodels import User, SavedFile


class BaseRepository():
    __model__ = None

    def __init__(self, session):
        self.session = session

    def get(self, id) -> list:
        """Returns a content with a certain id"""
        return self.query.get(id)

    def get_list(self):
        """
        Returns a list of all non-removed items
        """
        return self.query.filter_by(removed_at=None).all()

    def save(self, model):
        """
        """
        self.session.add(model)
        self.session.commit()
        return model

    def delete(self, id):
        model = self.get(id)
        if not model:
            raise Exception('Model not found')
        self.session.query(self.__model__).filter_by(id=id).update(
            {'removed_at': datetime.now()}
        )
        return model

    @property
    def query(self):
        """
        The decorator sets the query function as a class attribute.
        The function returns it so I don't have to pass the __model__
        every time one needs to query. 
        """
        return self.session.query(self.__model__)


class UserRepository(BaseRepository):

    ...


class FileRepository(BaseRepository):
    def get_file(self, id):
        """
        gets certain file
        """
        self.get(id)

    def get_file_list(self, userid):
        """
        gets a list of certain files
        based on filters.
        Currently only user
        """
        return self.query.filtery_by(user_id=userid)

    def save_file(self, model):
        """
        saves file
        later will put a filter logic here
        """
        self.save(model)
