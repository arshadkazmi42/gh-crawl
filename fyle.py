from arguments import Arguments


class Fyle:


    def __init__(self):

        self.arguments = Arguments()

        self.filename = self.arguments.get_organization()


    def write(self, content):

        file = open(f'{self.filename}.txt', 'a')
        file.write(f'{content}\n')  # python will convert \n to os.linesep
        file.close()