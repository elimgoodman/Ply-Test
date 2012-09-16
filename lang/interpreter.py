class Interpeter(object):
    
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def interpet(self):
        scope = {}

        #TODO: I think statement_list needs its own execute fn...
        for stmt in self.statement_list.statements:
            stmt.execute(scope)
        
        print scope
