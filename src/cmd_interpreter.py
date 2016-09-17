import cmd


class CmdInterpreter(cmd.Cmd):
    """
    Simple command processor example
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">>>"

    def do_set_name(self, name):
        self.name = name
        print(self.name)

    def do_say(self, message):
        print(message)

    def do_greet(self, theName):
        """
        Greet the named person
        :param theName: a string representing a person name
        :return: None
        """
        if theName:
            print("Hello " + theName)
        else:
            print("Hello " + self.myName)

    def do_quit(self, message):
        """
        Quit from my CMD
        :return: True
        """
        print("Quitting ......")
        return True

    # def help_quit(self):
    #     print('\n'.join(['Quit from my CMD', ':return: True']))

    do_q = do_quit