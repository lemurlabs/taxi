import datetime
from settings import settings

class Entry:
    def __init__(self, date, project_name, hours, description):
        self.project_name = project_name
        self.duration = hours
        self.description = description
        self.date = date
        self.pushed = False

        if project_name in settings.projects:
            self.project_id = settings.projects[project_name][0]
            self.activity_id = settings.projects[project_name][1]
        else:
            self.project_id = None
            self.activity_id = None

    def __str__(self):
        if self.is_ignored():
            project_name = '%s (ignored)' % (self.project_name)
        else:
            project_name = '%s (%s/%s)' % (self.project_name, self.project_id, self.activity_id)

        return '%-30s %-5.2f %s' % (project_name, self.get_duration() or 0, self.description)

    def is_ignored(self):
        return self.project_name[-1] == '?' or self.get_duration() == 0

    def get_duration(self):
        if isinstance(self.duration, tuple):
            if None in self.duration:
                return 0

            now = datetime.datetime.now()
            time_start = now.replace(hour=self.duration[0].hour,\
                    minute=self.duration[0].minute, second=0)
            time_end = now.replace(hour=self.duration[1].hour,\
                    minute=self.duration[1].minute, second=0)
            total_time = time_end - time_start
            total_hours = total_time.seconds / 3600.0

            return total_hours

        return self.duration

class Project:
    STATUS_NOT_STARTED = 0;
    STATUS_ACTIVE = 1;
    STATUS_FINISHED = 2;
    STATUS_CANCELLED = 3;

    STATUSES = {
            STATUS_NOT_STARTED: 'Not started',
            STATUS_ACTIVE: 'Active',
            STATUS_FINISHED: 'Finished',
            STATUS_CANCELLED: 'Cancelled',
    }

    SHORT_STATUSES = {
            STATUS_NOT_STARTED: 'N',
            STATUS_ACTIVE: 'A',
            STATUS_FINISHED: 'F',
            STATUS_CANCELLED: 'C',
    }

    def __init__(self, id, name, status = None, description = None, budget = None):
        self.id = int(id)
        self.name = name
        self.activities = []
        self.status = int(status)
        self.description = description
        self.budget = budget

    def __unicode__(self):
        if self.status in self.STATUSES:
            status = self.STATUSES[self.status]
        else:
            status = 'Unknown'

        return """Id: %s
Name: %s
Status: %s
Start date: %s
End date: %s
Budget: %s
Description: %s""" % (
        self.id, self.name,
        status,
        self.start_date.strftime('%d.%m.%Y'),
        self.end_date.strftime('%d.%m.%Y'),
        self.budget,
        self.description
    )

    def __str__(self):
        return unicode(self).encode('utf-8')

    def add_activity(self, activity):
        self.activities.append(activity)

    def is_active(self):
        return (self.status == self.STATUS_ACTIVE and
                self.start_date <= datetime.datetime.now() and
                self.end_date > datetime.datetime.now())

    def get_short_status(self):
        if self.status not in self.SHORT_STATUSES:
            return '?'

        return self.SHORT_STATUSES[self.status]

class Activity:
    def __init__(self, id, name, price):
        self.id = int(id)
        self.name = name
        self.price = float(price)
