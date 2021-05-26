
class Logger(object):

    def __init__(self, edit_log=None, show_mode='both'):
        self.edit_log = edit_log
        self.show_mode = show_mode

    def log(self, text):
        if self.show_mode == 'both':
            print(text)
            if self.edit_log is not None:
                self.edit_log.append(text)

        elif self.show_mode == 'console_only':
            print(text)

        elif self.show_mode == 'edit_only':
            if self.edit_log is not None:
                self.edit_log.append(text)
