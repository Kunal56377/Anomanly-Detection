class paremeter:
    def __init__(self,Accountid,Transction):
        self.Accountid = Accountid
        self.Transction = Transction
    
    def get(self):
        return self.Accountid,self.Transction 