class publication:
    def __init__(self, pubname, pubowner, puballtables, pubinsert, pubupdate,
                 pubdelete, pubtruncate, pubviaroot, pubgencols):
        self.pubname = pubname
        self.pubowner = pubowner
        self.puballtables = puballtables
        self.pubinsert = pubinsert
        self.pubupdate = pubupdate
        self.pubdelete = pubdelete
        self.pubtruncate = pubtruncate
        self.pubviaroot = pubviaroot
        self.pubgencols = pubgencols

    def to_dict(self):
        return {
            "name" : self.pubname,
            "pubowner" : self.pubowner,
            "puballtables" : self.puballtables,
            "pubinsert" : self.pubinsert,
            "pubupdate" : self.pubupdate,
            "pubdelete" : self.pubdelete,
            "pubtruncate" : self.pubtruncate,
            "pubviaroot" : self.pubviaroot,
            "pubgencols" : self.pubgencols
        }