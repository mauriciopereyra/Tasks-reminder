from cgitb import text
from logging import NOTSET
from pyclbr import Class
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
import main_page # Main page view
import all_tasks # All tasks view
from task import Task
from tag import Tag
from datetime import date, datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

def check_recurring(tasks_list):
    today = date.today() + timedelta(days=0)

    for task in [task for task in tasks_list if task.recurring]:
        # check when it's the last start date
        start_date = task.date_started
        recurring_value = task.recurring_value

        if task.recurring_type == 'weekday':
            recurring_value = 7
            while True:
                if start_date.weekday() == time.strptime(task.recurring_value,'%A').tm_wday:
                    break
                else:
                    start_date += timedelta(days=1)
        
        elif task.recurring_type == 'month':
            recurring_value = 30
        

        if not task.recurring_type == 'month':
            while True:
                if start_date >= today:
                    start_date -= timedelta(days=int(recurring_value))
                    break
                start_date += timedelta(days=int(recurring_value))
            to_do = start_date + timedelta(days=int(recurring_value))
        else:
            while True:
                if start_date >= today:
                    start_date -= relativedelta(months=1)
                    break
                start_date += relativedelta(months=1)
            to_do = start_date + relativedelta(months=1)            



        # Check if today is in last 40%
        today_in_last_days = ((to_do - today) / (to_do - start_date) * 100) <= 40
        # Check if last done is in last 40%
        last_done_in_last_days = ((to_do - task.last_done) / (to_do - start_date) * 100) <= 40

        # If today is in last 40% and last done is NOT in last 40% then set task as not done
        if today_in_last_days:
            task.date_to_do = to_do
            if not last_done_in_last_days:
                task.done = False
            






class Recurring:
    def __init__(self,task):
        self.info = None

        self.days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]

        # Days
        days_in_dropdown = Gtk.ListStore(str)
        for index, day in enumerate(self.days):
                days_in_dropdown.append([day])
        self.weekday_dropdown = Gtk.ComboBox.new_with_model(days_in_dropdown)
        renderer_text1 = Gtk.CellRendererText()
        self.weekday_dropdown.pack_start(renderer_text1, True)
        self.weekday_dropdown.add_attribute(renderer_text1, "text", 0)
        self.weekday_dropdown.set_active(0)

        self.window = Gtk.Window(title="Recurring task")
        self.window.set_default_size( 300, 150)
        self.window.move(1140,300)
        self.window.set_keep_above(True)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.window.add(main_box)

        # Not recurring
        self.not_recurring = Gtk.RadioButton.new_with_label_from_widget(None,"Not recurring")

        # Every n days
        self.days_radiobutton = Gtk.RadioButton.new_with_label_from_widget(self.not_recurring, "Every")
        self.days_value = Gtk.Entry(text=3)
        test_label3 = Gtk.Label(label="days")

        # Every x weekday
        self.weekday_radiobutton = Gtk.RadioButton.new_with_label_from_widget(self.not_recurring,"Every")

        # Every month
        self.month_radiobutton = Gtk.RadioButton.new_with_label_from_widget(self.not_recurring,"Every")
        test_label7 = Gtk.Label(label="Month")

        test_label8 = Gtk.Label(label="Startdate")
        self.startdate_entry = Gtk.Entry(text=date.today().strftime("%d/%m/%Y"))

        # Check if recurring
        if task.recurring:
            self.startdate_entry.set_text(datetime.strftime(task.date_started,"%d/%m/%Y"))
            if task.recurring_type == 'days':
                self.days_radiobutton.set_active(1)
                self.days_value.set_text(task.recurring_value)
            elif task.recurring_type == 'weekday':
                self.weekday_radiobutton.set_active(2)
                self.weekday_dropdown.set_active((time.strptime(task.recurring_value, "%A").tm_wday+1)%7)
            elif task.recurring_type == 'month':
                self.month_radiobutton.set_active(3)


        table=Gtk.Table(n_rows=4,n_columns=4)

        table.attach(self.not_recurring,0,3,0,1)

        table.attach(self.days_radiobutton,1,2,1,2)
        table.attach(self.days_value,2,3,1,2)
        table.attach(test_label3,3,4,1,2)

        table.attach(self.weekday_radiobutton,1,2,2,3)
        table.attach(self.weekday_dropdown,2,4,2,3)

        table.attach(self.month_radiobutton,1,2,3,4)
        table.attach(test_label7,2,3,3,4)

        table.attach(test_label8,1,2,4,5)
        table.attach(self.startdate_entry,2,4,4,5)


        cancel = Gtk.Button(label="Cancel")
        cancel.connect("clicked",self.on_clicking_cancel)
        ok = Gtk.Button(label="Ok")
        ok.connect("clicked",self.on_clicking_ok)
        cancel.set_hexpand(True)
        ok.set_hexpand(True)

        bottom_box = Gtk.Box()
        bottom_box.pack_start(cancel,False,False,0)
        bottom_box.pack_start(ok,False,False,0)

        bottom_box.set_hexpand(True)

        main_box.pack_start(table,False,False,0)
        main_box.pack_end(bottom_box,False,False,0)



    def on_clicking_ok(self,widget):
        value = None
        if self.days_radiobutton.get_active():
            recurring_type = "days"
            value = self.days_value.get_text()
        elif self.weekday_radiobutton.get_active():
            recurring_type = "weekday"
            value = self.days[self.weekday_dropdown.get_active()]
        elif self.month_radiobutton.get_active():
            recurring_type = "month"
            value = "month"
        elif self.not_recurring.get_active():
            recurring_type = None
            value = None            
        self.info = {
            'recurring_type':recurring_type,
            'value': value,
            'startdate':self.startdate_entry.get_text(),
        }

        self.window.destroy()

    def on_clicking_cancel(self,widget):
        self.window.destroy()



