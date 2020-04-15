#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom QLCDNumber that shows date and time, optional background image."""


import os
from datetime import datetime

from PyQt5.QtCore import QTimer

from PyQt5.QtGui import QPalette, QBrush, QImage

from PyQt5.QtWidgets import QLCDNumber


##############################################################################


class QLCDDateTime(QLCDNumber):

    """Custom QLCDNumber with datetime."""

    def __init__(self, parent=None, background_image=None, *args, **kwargs):
        """Init class custom tab bar."""
        super(QLCDDateTime, self).__init__(parent=None, *args, **kwargs)
        self.parent, self.timer, self.palete = parent, QTimer(self), QPalette()
        if background_image and os.path.isfile(background_image):
            self.palete.setBrush(QPalette.Background,
                                 QBrush(QImage(background_image)))
            self.setPalette(self.palete)
        self.setNumDigits(22)
        self.timer.timeout.connect(lambda: self.display(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")))
        self.timer.start(1000)


class QLCDCountDown(QLCDNumber):

    """Custom QLCDNumber with a CountDown based on argument datetime."""

    def __init__(self, parent=None, background_image=None, until=None, *args):
        """Init class custom tab bar."""
        super(QLCDCountDown, self).__init__(parent=None, *args)
        self.parent, self.timer, self.palete = parent, QTimer(self), QPalette()
        self.setNumDigits(14)
        if background_image and os.path.isfile(background_image):
            self.palete.setBrush(QPalette.Background,
                                 QBrush(QImage(background_image)))
            self.setPalette(self.palete)
        if until and isinstance(until, datetime) and until > datetime.now():
            self.timer.timeout.connect(lambda: self.display(
               self.seconds_time_to_human_string(
                   (until - datetime.now()).total_seconds())))
            self.timer.start(1000)
        else:
            self.display("0" * 24)

    def seconds_time_to_human_string(self, time_on_seconds=0):
        """Calculate time, with precision from seconds to days."""
        minutes, seconds = divmod(int(time_on_seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        human_time_string = ""
        if days:
            human_time_string += "%02dD " % days
        if hours:
            human_time_string += "%02d" % hours
        else:
            human_time_string += "00"
        if minutes:
            human_time_string += ":%02d" % minutes
        else:
            human_time_string += ":00"
        human_time_string += ":%02d" % seconds
        return human_time_string


##############################################################################


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    gui1 = QLCDDateTime(None)
    gui2 = QLCDCountDown(None, None, datetime.strptime('Jun 2020', '%b %Y'))
    gui1.show()  # date and time
    gui2.show()  # count down
    exit(app.exec_())
