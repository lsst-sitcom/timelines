import csv
from datetime import datetime, timedelta
import re
import sys
import textwrap

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

__all__ = ["get_data_dir", "show_activities", "read_activities", "write_activities",
           "Activity", "Functionality", "Milestone",
           "AdvanceRow", "Color", "LengthArrow", "MarkerWidth"]


class Activity:
    border = None
    color = None
    markerWidth = 0
    fontsize = 8
    height = 0.3
    row = 0

    def __init__(self, descrip, t0, duration, color=None, border=None, markerWidth=0, drow=0):
        """An activity to be carried out
        descrip: string description; will be wrapped based on a guess on available width
        t0: starting date as string (e.g. 1958-02-05)
        duration: duration in days, or ending date in same format as t0
        color: color to use, or None to use current default
        border: border color to use, or None to use current default
        drow: offset Activity by drow when drawing
          (see also AdvanceRow in show_activities())
        """
        self.descrip = descrip

        self.t0 = datetime.fromisoformat(t0)
        try:
            self.duration = timedelta(duration)
        except TypeError:
            self.duration = datetime.fromisoformat(duration) - self.t0

        self.drow = drow
        self._color = color if color else None
        self._border = border if border else None
        self._markerWidth = markerWidth if markerWidth else None

    def __str__(self):
        return "Activity"

    def getData(self):
        return [self.descrip, self.t0.strftime('%Y-%m-%d'), (self.t0 + self.duration).strftime('%Y-%m-%d'),
                self._color, self._border, self._markerWidth, self.drow,
               ]

    def draw(self, totalDuration=0, startDate="1958-02-05", endDate="2099-12-31", **kwargs):
        kwargs = kwargs.copy()
        if "color" not in kwargs:
            kwargs["color"] = self.color if self._color is None else self._color

        if isinstance(endDate, str):
            endDate = datetime.fromisoformat(endDate)

        t0 = self.t0
        t1 = t0 + self.duration

        if t1 < startDate:
            return 0
        elif t0 < startDate:
            t0 = startDate

        if t0 > endDate:
            return 0
        elif t1 > endDate:
            t1 = endDate

        y0 = self.height*(1.1*(self.row - self.drow))
        x = t0 + (t1 - t0)*np.array([0, 1, 1, 0, 0])
        y = y0 + self.height*np.array([0, 0, 1, 1, 0])
        plt.fill(x, y, '-', alpha=0.5, **kwargs)

        if not (self.border is None and self._border is None):
            kwargs["color"] = self.border if self._border is None else self._border

        plt.plot(x, y, '-', **kwargs)

        textwidth = 0
        if self.fontsize:
            if totalDuration == 0:
                fiddleFactor = 3
            else:
                width_pts = plt.gcf().get_size_inches()[0]*72
                fiddleFactor = width_pts/totalDuration.days

            textwidth = int(fiddleFactor*self.duration.days/self.fontsize) + 1

        if textwidth <= 0:
            textwidth = 10
        plt.text(t0 + 0.5*(t1 - t0), y0 + 0.5*self.height,
                 textwrap.fill(self.descrip, width=textwidth, break_long_words=False),
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=self.fontsize)

        return 1


class Milestone(Activity):
    markerWidth = 2

    def __init__(self, descrip, t0, color=None, border=None, align="right", valign="top", markerWidth=None, drow=0):
        super().__init__(descrip, t0, 0.0, color=color, border=border, drow=drow, markerWidth=markerWidth)
        self.align = align
        self.valign = valign

    def __str__(self):
        return "Milestone"

    def getData(self):
        return [self.descrip, self.t0.strftime('%Y-%m-%d'),
                self._color, self._border, self.align, self.valign, self._markerWidth, self.drow]

    def draw(self, totalDuration=0, startDate="1958-02-05", endDate="2099-12-31", **kwargs):
        kwargs = kwargs.copy()
        if "color" not in kwargs:
            kwargs["color"] = self.color if self._color is None else self._color

        if isinstance(startDate, str):
            startDate = datetime.fromisoformat(startDate)
        if isinstance(endDate, str):
            endDate = datetime.fromisoformat(endDate)

        t0 = self.t0
        if t0 + self.duration < startDate:
            return 0
        elif t0 < startDate:
            t0 = startDate

        if t0 > endDate:
            return 0

        y0 = self.height*(1.1*(self.row - self.drow))

        markerWidth = timedelta(self.markerWidth if self._markerWidth is None else self._markerWidth)
        x = t0 + markerWidth*np.array([0, 1, 0, -1, 0])
        y = y0 + self.height*np.array([0, 0.5, 1, 0.5, 0])
        plt.fill(x, y, '-', alpha=1, **kwargs)

        horizontalalignment = "left" if self.align == "right" else "right"  # matplotlib is confusing
        plt.text(t0 + markerWidth/2*(1 if self.align == "right" else -1),
                 y0 + (0.9 if self.valign == "top" else 0.1)*self.height, self.descrip,
                 horizontalalignment=horizontalalignment, verticalalignment='center',
                 fontsize=self.fontsize, zorder=10)

        return 1


class Functionality(Milestone):
    """A delivered piece of functionality"""

    lengthArrow = 10

    def __init__(self, *args, dy=0, lengthArrow=None, **kwargs):
        kwargs["markerWidth"] = 0
        super().__init__(*args, **kwargs)
        self._lengthArrow = lengthArrow
        self.dy = dy
        self._color = kwargs.get("color")

    def __str__(self):
        return "Functionality"

    def getData(self):
        return [self.descrip, self.t0.strftime('%Y-%m-%d'), self.dy, self.lengthArrow,
                self._color, self._border, self.drow]

    def draw(self, dy=0, *args, **kwargs):
        if super().draw(*args, **kwargs) == 0:
            return 0

        y0 = self.height*(1.1*(self.row - self.drow))

        x0 = mdates.date2num(self.t0)
        dx = self.lengthArrow if self._lengthArrow is None else self._lengthArrow

        plt.arrow(x0, y0 + (0.5 + self.dy)*self.height, dx, 0, length_includes_head=True,
                  head_length=0.15*dx, head_width=0.2*self.height,
                  color=kwargs.get("color",
                                   self.color if self._color is None else self._color))

        return 1

class Manipulation:
    """Modify the state of the system, rather than describing an activity or milestone"""
    pass

class AdvanceRow(Manipulation):
    """A class used to advance the row counter"""

    def __init__(self, drow):
        self.drow = drow

    def __str__(self):
        return "AdvanceRow"

    def getData(self):
        return [self.drow]

class Color(Manipulation):
    """A class used to set the default Activity colour"""
    def __init__(self, color, border=None):
        self.color = color if color else None
        self.border = border if border else None

    def __str__(self):
        return "Color"

    def getData(self):
        return [self.color, self.border if self.border else '']

    def set_default_color(self):
        Activity.color = self.color
        Activity.border = self.border

class MarkerWidth(Manipulation):
    """A class used to set Milestone's markerWidth"""

    def __init__(self, markerWidth):
        self.markerWidth = markerWidth

    def __str__(self):
        return "MarkerWidth"

    def getData(self):
        return [self.markerWidth]

    def set_default_markerWidth(self):
        Milestone.markerWidth = self.markerWidth

class LengthArrow(Manipulation):
    """A class used to set Functionality's lengthArrow"""

    def __init__(self, lengthArrow):
        self.lengthArrow = lengthArrow

    def __str__(self):
        return "LengthArrow"

    def getData(self):
        return [self.lengthArrow]

    def set_default_lengthArrow(self):
        Functionality.lengthArrow = self.lengthArrow


def get_data_dir():
    return re.sub(r"/python/.*$", "", __file__)

def show_activities(activities, height=0.1, fontsize=7, show_today=True,
                    startDate="1958-02-05", endDate="2099-12-31"):
    """Plot a set of activities

    activities: list of list of Activities
    height:  height of each activity bar
    fontsize: fontsize for labels (passed to plt.text)
    show_today: indicate today by a dashed vertical line

    In general each inner list of activities is drawn on its own row but you can
    modify this by using pseudo-activity `AdvanceRow`.  Also
    available is `Color` to set the default colour (and optionally border)
    N.b. `Color(c)` resets the border, `Activity(..., color=c)` does not

    E.g.
        activities = [
            [
                Color("white", border='red'),
                Activity("A", "2021-02-28", 35),
                Activity("B", "2021-04-10", "2021-05-10")
            ], [
                Color("blue"),
                Activity("C", "2021-01-01", 30),
                Activity("D", "2021-01-20", "2021-04-01", drow=1),
                AdvanceRow(1),
            ], [
                Activity("E", "2021-01-05", "2021-01-31", color="green"),
            ],
        ]
"""
    Activity.height = height
    Activity.fontsize = fontsize

    if isinstance(startDate, str):
        startDate = datetime.fromisoformat(startDate)
    if isinstance(endDate, str):
        endDate = datetime.fromisoformat(endDate)

    dateMin = None
    dateMax = None
    for aa in activities:
        for a in aa:
            if isinstance(a, Manipulation):
                continue

            t0 = a.t0
            t1 = a.t0 + a.duration

            if t1 < startDate:
                continue
            if t0 < startDate:
                t0 = startDate

            if t0 > endDate:
                continue
            if t1 > endDate:
                t1 = endDate

            if dateMin is None or t0 < dateMin:
                dateMin = t0
            if dateMax is None or t1 > dateMax:
                dateMax = t1

    totalDuration = dateMax - dateMin  # used in line-wrapping the labels

    Activity.row = 0
    for aa in activities:
        nActivity = 0
        for a in aa:
            if isinstance(a, Manipulation):
                if isinstance(a, Color):
                    a.set_default_color()
                elif isinstance(a, AdvanceRow):
                    Activity.row -= a.drow
                elif isinstance(a, MarkerWidth):
                    a.set_default_markerWidth()
                elif isinstance(a, LengthArrow):
                    a.set_default_lengthArrow()
                else:
                    raise NotImplemented(a)

                continue

            nActivity += a.draw(totalDuration=totalDuration, startDate=startDate, endDate=endDate)

        if nActivity > 0:
            Activity.row -= 1

    if show_today and datetime.now() > startDate:
        plt.axvline(datetime.now(), ls='--', color='black', alpha=0.5, zorder=-1)
    plt.grid(axis='x')

    plt.yticks(ticks=[], labels=[])
    plt.gcf().autofmt_xdate()
    plt.gca().fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S.02 ');

    plt.tight_layout()


def read_activities(fileName):
    activities = []
    with open(fileName) as fd:
        csvin = csv.reader(fd)

        activitySet = []
        activities.append(activitySet)

        for args in csvin:
            if len(args) == 0:
                activitySet = []
                activities.append(activitySet)
                continue

            what = args.pop(0)

            if what == "Activity":
                descrip, t0, duration, color, border, markerWidth, drow = args
                drow = int(drow)
                a = Activity(descrip, t0, duration, color, border, markerWidth=markerWidth, drow=drow)
            elif what == "AdvanceRow":
                drow = int(args[0])
                a = AdvanceRow(drow)
            elif what == "Color":
                color, border = args
                a = Color(color, border)
            elif what == "Functionality":
                descrip, t0, dy, lengthArrow, color, border, drow = args
                drow = int(drow)
                a = Functionality(descrip, t0, dy, lengthArrow, color, border, drow=drow)
            elif what == "LengthArrow":
                lengthArrow = int(args[0])
                a = LengthArrow(lengthArrow)
            elif what == "MarkerWidth":
                markerWidth = int(args[0])
                a = MarkerWidth(markerWidth)
            elif what == "Milestone":
                descrip, t0, color, border, align, valign, markerWidth, drow = args
                drow = int(drow)
                a = Milestone(descrip, t0, color, border, drow=drow,
                              align=align, valign=valign, markerWidth=markerWidth)
            else:
                raise RuntimeError(what)

            activitySet.append(a)

    return activities


def write_activities(activities, fileName=None):
    if fileName is None:
        fileName = "/dev/null"

    with open(fileName, "w") as fd:
        if fileName == "/dev/null":
            fd = sys.stdout

        csvout = csv.writer(fd) # delimiter=',',  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for aa in activities:
            for a in aa:
                csvout.writerow([str(a)] + a.getData())

            csvout.writerow([])

