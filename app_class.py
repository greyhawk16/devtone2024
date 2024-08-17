from models import SessionDB


class Session():
    def __init__(self, SessionDB):
        self.token = SessionDB.token
        self.problem_number = int(SessionDB.problem_num)
        self.life = int(SessionDB.life)
        self.description = SessionDB.description
        self.option = [SessionDB.option1, SessionDB.option2, SessionDB.option3, SessionDB.option4]
        self.result = [int(SessionDB.result1), int(SessionDB.result2), int(SessionDB.result3), int(SessionDB.result4)]
        self.result_text = SessionDB.result_desc


class Problem():
    def __init__(self, Session):
        self.problem_number = 0
        self.life = 0
        self.image_url = ""
        self.description = ""
        self.option = []
        self.token = Session.token

class Check():
    def __init__(self, Session):
        self.problem_number = 0
        self.life = 0
        self.result_all = False
        self.result_text = ""
        self.option = []
        self.token = Session.token
        # Generate attributes from result_1 to result_4
        for i in range(1, 5):
            setattr(self, f"result_{i}", 0)

class Start():
    def __init__(self, Session):
        self.token = Session.token

class Gameover():
    def __init__(self, Session):
        self.token = Session.token
        self.result_text = ""