#!/usr/bin/env python3
import i3ipc
import time
import threading
import subprocess

""" Time tracker, notify every 5 minutes passed in a specefic program """


class TimeTracker:
    def __init__(self):
        self.i3 = i3ipc.Connection(auto_reconnect=True)
        self.i3.on('window::focus', self.on_window_focus)

        self.pending_notification = {}
        self.focus_history = {}

        # Time in seconds to wait before a notification
        self.delay = 5

        self.lfocused = None
        self.focused = self.i3.get_tree().find_focused()

        self.lfocused_class = None
        self.focused_class = self.focused.window_class
        # time since last focus
        self.time_since_lfocus = time.perf_counter()

        self.save_to_history()
        self.notification_manager()

    def wait_for_events(self):
        self.i3.main()

    def save_to_history(self):
        current_time = time.perf_counter()

        if self.lfocused is not None and self.lfocused.type == 'con':
            if self.lfocused_class not in self.focus_history.keys():
                self.focus_history[ self.lfocused_class ] = {
                    'time_spent': current_time - self.time_since_lfocus,
                    'window': self.lfocused
                }
            else:
                self.focus_history[ self.lfocused_class ]['time_spent'] += current_time - self.time_since_lfocus

        if self.focused.type == 'con':
            if self.focused_class not in self.focus_history.keys():
                self.focus_history[ self.focused_class ] = {
                    'time_spent': 0,
                    'window': self.focused
                }
            else:
                self.focus_history[ self.focused_class ]['time_spent'] += current_time - self.time_since_lfocus

        self.time_since_lfocus = time.perf_counter()

    def on_window_focus(self, i3, e):
        self.lfocused = self.focused
        self.lfocused_class = self.lfocused.window_class

        self.focused = i3.get_tree().find_focused()
        self.focused_class = self.focused.window_class 

        self.save_to_history()
        self.notification_manager()

        print( "%s focused" % self.focused_class )


    def notificate(self):
        window_class = self.focused_class
        time_spent = self.focus_history[ self.focused_class ]['time_spent']

        notification = "You have spent %s seconds in %s" % ( int(time_spent) + self.delay, window_class )

        print( notification )
        print( "time_spent: %d" % int(time_spent) )

        subprocess.run(['notify-send', notification])

        self.pending_notification = {}
        self.save_to_history()
        self.notification_manager()


    def notification_manager(self):
        if self.focused.type != 'con':
            thr = pending_notification['thread']

            thr.cancel() if thr.is_alive() else 0

            return 0

        time_spent = int(self.focus_history[ self.focused_class ]['time_spent']) 
        sec_to_wait = int( time_spent / self.delay + 1) * self.delay - int(time_spent)
            
        print( "time_spent: %d, sec_to_wait: %d" % ( time_spent, sec_to_wait )  )
        # Create new pending notification
        if not self.pending_notification:
            self.pending_notification['name'] = self.focused_class
            self.pending_notification['thread'] = threading.Timer(
                sec_to_wait,
                self.notificate,
            )
            self.pending_notification['thread'].start()
        # Replace last pending notification with a new one
        elif self.focused_class != self.pending_notification['name']:
            # print( "focused: %s, pending: %s" % (self.focused_class, self.pending_notification['name']) )
            thr = self.pending_notification['thread']

            thr.cancel() if thr.is_alive() else 0

            self.pending_notification['name'] = self.focused_class
            self.pending_notification['thread'] = threading.Timer(
                sec_to_wait,
                self.notificate,
            )
            self.pending_notification['thread'].start()
        else:
            print( "focused: %s, pending: %s" % (self.focused_class, self.pending_notification['name']) )



if __name__ == '__main__':
    tracker = TimeTracker()
    tracker.wait_for_events()
