import cmd
import os


class CmdView(cmd.Cmd):
    def __init__(self, controller):
        cmd.Cmd.__init__(self, controller)
        self.controller = controller
        self.prompt = ">>>"
        self.intro = "Thank you for using WebScraper. \n" \
                     "Type: 'help' to find available commands. \n" \
                     "Type: 'help <command name>' for more information about" \
                     " the command. \n" \
                     "Type: 'q' or 'quit' to exit WebScraper."

    def do_set_url(self, new_url):
        """
        Replaces the existing URL with the newly assigned URL
        Usage:
            s <new_url>
            set_url <new_url>
        :param new_url: new URL value
        :return: None
        """
        self.controller.set_to_input(new_url)
        print("URL is now set to: " + new_url)

    def do_show_url(self, args):
        """
        Prints out the existing URL in the interpreter
        Usage:
            sh
            show_url
        :param args: there are no arguments for this method
        :return: None
        """
        print(self.controller.get_url())

    def do_load(self, args):
        """
        Starts the web scrapping process to retrieve fresh data
        Usage:
            l
            load
        :param args: there are no arguments for this method
        :return: None
        """
        print("This may take a while. Please wait a moment...")
        self.controller.get_data()
        print("All done.")

    def do_display(self, index, ):
        """
        Prints out records by their assigned index number
        Usage:
            d index
            display index
        :param index: index number of record contained in the dictionary
        of lists
        :return: None
        """
        try:
            for record in (self.controller.get_container(index)):
                if type(record) == list:
                    record = [str(n) for n in record]
                    print(''.join(record))
                else:
                    print(record)
        except TypeError:
                print("Error: Failed to read data.")
        except ValueError:  # as e:
                print("Error: Missing index value or conversion error.")
                # print(e)
        except IndexError:
                print("Error: Missing or corrupted data.")
                print("Maybe try loading data first?")
        print("Finished processing.")

    def do_quit(self, args):
        """
        Save data to local drive, which is to be loaded on next startup
        and then exits out of my CMD successfully
        Usage:
            q
            quit
        :param args: there are no arguments for this method
        :return: True
        """
        self.controller.save_pickle_data()
        os._exit(0)

    do_l = do_load
    do_s = do_set_url
    do_sh = do_show_url
    do_q = do_quit
    do_d = do_display
