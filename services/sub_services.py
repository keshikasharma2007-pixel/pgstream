from repositories.sub_repository import SubRepository

class SubService:
    def __init__(self):
        self.repository = SubRepository()

    def get_subs(self):
        return self.repository.get_all_subs()

