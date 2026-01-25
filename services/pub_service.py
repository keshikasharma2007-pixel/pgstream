from repositories.pub_repository import PubRepository

class PubService:
    def __init__(self):
        self.repository = PubRepository()

    def get_all_pubs(self):
        return self.repository.get_all_pubs()

    def get_pub(self, pubname):
        return self.repository.get_pub_name(pubname)

    def delete_pub_by_name(self, pubname):
        return self.repository.delete_pub_name(pubname)

    def create_pub(self, pubname, table):
        return self.repository.create_new_pub(pubname, table)

    def update_pub(self, pubname, publish_ops):
        return self.repository.update_one_pub(pubname, publish_ops)

