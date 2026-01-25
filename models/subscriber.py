class subscriber:
    def __init__(self, subname, enabled, publications, conninfo, slot_name=None, sync_state=None):
        self.name = subname
        self.enabled = enabled
        self.publications = publications
        self.conninfo = conninfo
        self.slot_name = slot_name
        self.sync_state = sync_state

    def to_dict(self):
        return {
            "name" : self.name,
            "enabled" : self.enabled,
            "publications" : self.publications,
            "conninfo" : self.conninfo,
            "slot_name" : self.slot_name,
            "sync_name" : self.sync_state
        }