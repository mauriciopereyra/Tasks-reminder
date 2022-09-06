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
import csv
from distutils.util import strtobool
from datetime import date
import pickle
import os
from recurring import check_recurring

cwd = os.getcwd()

# Load css
screen = Gdk.Screen.get_default()
# Picle file location
pickle_file = cwd+"/pickle_file.p"


class MyWindow(Gtk.Window):
    def __init__(self,position):
        # Import tasks and tags
        self.tags_list = [Tag("Work"),Tag("Family"),Tag("Personal")]
        self.tasks_list = []
        self.import_tasks()
        
        # Update recurring tasks
        check_recurring(self.tasks_list)

        # Import filters
        try:
            filters_imported = pickle.load(open(pickle_file, "rb"))
        except (OSError, IOError) as e:
            print(e)
            filters_imported = {
                    'filter_active': "All",
                    'tag_active': "All",
                    'date_filter_active': "All",
            }
            pickle.dump(filters_imported, open(pickle_file, "wb"))

        
        self.filter_active = filters_imported['filter_active']
        self.tag_active = filters_imported['tag_active']
        self.date_filter_active = filters_imported['date_filter_active']

        self.filters = ["All","Pending","Done"]
        self.tags = ["All"] + [tag.name for tag in self.tags_list]
        self.date_filters = ["All","7 days","15 days","1 month"]

        # Create window
        self.window = self.init_window()
        # Create single task view
        self.tasks_notebook = Gtk.Notebook()
        self.tasks_notebook.set_scrollable(True)
        self.tasks_notebook.popup_enable()
        # Create all tasks view
        self.all_tasks_wrapper = all_tasks.main(window=self,tasks_list=self.tasks_list,tags_list=self.tags_list)
        self.stack.add_named(self.tasks_notebook,"single_task")
        self.stack.add_named(self.all_tasks_wrapper,"all_tasks")
        self.add_pages(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
        self.add_tasks_lists(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)


    def clear_notebook(self):
        if hasattr(self, 'tasks_notebook'):
            for child in self.tasks_notebook.get_children():
                self.tasks_notebook.remove(child)

    def clear_all_tasks_wrapper(self):
        if hasattr(self, 'all_tasks_wrapper'):
            if hasattr(self.all_tasks_wrapper, 'list_box'):
                for child in self.all_tasks_wrapper.list_box.get_children():
                    self.all_tasks_wrapper.list_box.remove(child)


    def add_pages(self,filter_by="All",tag="All",date_filter="All"):
        tasks = self.tasks_list
        if filter_by == "All":
            tasks = tasks
        elif filter_by == "Pending":
            tasks = [task for task in self.tasks_list if not task.done]
        elif filter_by == "Done":
            tasks = [task for task in self.tasks_list if task.done]

        # Filter by tags here!!!
        if not tag == "All":
            tasks = [task for task in tasks if task.tags.name == tag]
        # Filter by dates here!!!
        if date_filter == "All":
            tasks = tasks
        elif date_filter == "7 days":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 7]
        elif date_filter == "15 days":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 15]
        elif date_filter == "1 month":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 30]

        tasks = sorted(tasks, key=lambda task: (task.done,-task.star,task.date_to_do))
        
        self.clear_notebook()

        if hasattr(self, 'tasks_notebook'):
            for task in tasks:
                single_task_wrapper = main_page.Create(window=self,current_task=task,tags_list=self.tags_list,widget=None)
                self.tasks_notebook.append_page(child=single_task_wrapper,tab_label=Gtk.Label(label=task.name))
                single_task_wrapper.show()

        self.export_tasks()




    def add_tasks_lists(self,filter_by="All",tag="All",date_filter="All"):
        tasks = self.tasks_list

        if filter_by == "All":
            tasks = tasks
        elif filter_by == "Pending":
            tasks = [task for task in self.tasks_list if not task.done]
        elif filter_by == "Done":
            tasks = [task for task in self.tasks_list if task.done]

        # Filter by tags here!!!
        if not tag == "All":
            tasks = [task for task in tasks if task.tags.name == tag]
        # Filter by dates here!!!
        if date_filter == "All":
            tasks = tasks
        elif date_filter == "7 days":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 7]
        elif date_filter == "15 days":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 15]
        elif date_filter == "1 month":
            tasks = [task for task in tasks if (task.date_to_do - date.today()).days <= 30]

        tasks = sorted(tasks, key=lambda task: (task.done,-task.star,task.date_to_do))

        self.clear_all_tasks_wrapper()

        if hasattr(self, 'all_tasks_wrapper'):
            self.all_tasks_wrapper.frame.set_label(tag)

            for task in tasks:
                row = Gtk.ListBoxRow()
                row.task = task
                box = Gtk.Box()
                field = Gtk.Label(label=task.name)
                field2 = Gtk.CheckButton()#task.done
                field2.set_active(task.done)
                field2.connect("released",self.all_tasks_wrapper.toggle_done)
                field2.task = task
                field3 = Gtk.Label(label=task.date_to_do)
                box.pack_start(field,True,False,10)
                box.pack_start(field2,False,False,10)
                box.pack_start(field3,False,False,10)
                row.add(box)
                self.all_tasks_wrapper.list_box.insert(row,-1)
                field.show()
                field2.show()
                field3.show()
                box.show()
                row.show()





    # SETTING UP THE WINDOW
    def init_window(self,widget=None):
        Gtk.Window.__init__(self, title="Tasks")
        Gtk.Window.set_default_size(self, 400, 480)
        Gtk.Window.move(self,1640,300)
        Gtk.Window.set_keep_above(self,True)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(self.main_box)
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.main_box.pack_start(self.stack, True, True, 0)
        self.create_toolbar()
        Notify.init("Tasks")


    def open_task(self,tasks_list,tags_list,position):
        self.current_task = tasks_list[position]
        self.task.set_text(self.current_task.name)
        self.done.set_active(self.current_task.done)
        self.notes.set_text(self.current_task.notes)
        self.recurring.set_active(self.current_task.recurring)
        self.date.set_text(self.current_task.date_to_do)
        self.star.set_active(self.current_task.star)
        # tags = ', '.join([str(tag) for tag in self.current_task.tags])
        self.tags.set_active(tags_list.index(self.current_task.tags))



    def toggle_view(self,widget=None):
        current_view = self.stack.get_visible_child_name()
        if current_view == "single_task":
            self.stack.set_visible_child_name("all_tasks")
            self.add_tasks_lists(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
            self.all_tasks_wrapper.list_box.select_row(self.all_tasks_wrapper.list_box.get_row_at_index(self.tasks_notebook.get_current_page()))
        else:
            self.add_pages(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
            self.stack.set_visible_child_name("single_task")
            self.tasks_notebook.set_current_page(self.all_tasks_wrapper.list_box.get_selected_row().get_index())
            # self.all_tasks_wrapper.list_box.select_row(self.all_tasks_wrapper.list_box.get_row_at_index(self.tasks_notebook.get_current_page()))


    def create_toolbar(self):
        toolbar = Gtk.Box(spacing=6)
        toolbar.set_valign(Gtk.Align.END)
        self.main_box.pack_end(toolbar, True, True, 0)

        # View
        view = Gtk.Button(label="View")
        view.connect("clicked",self.toggle_view)
        toolbar.pack_start(view, True, True, 0)

        # Tags
        self.tags_in_dropdown = Gtk.ListStore(str)
        for index, tag in enumerate(self.tags):
                self.tags_in_dropdown.append([tag])
        tags = Gtk.ComboBox.new_with_model(self.tags_in_dropdown)
        renderer_text = Gtk.CellRendererText()
        tags.pack_start(renderer_text, True)
        tags.add_attribute(renderer_text, "text", 0)
        tags.connect('changed',self.save_tag)
        toolbar.pack_start(tags, True, True, 0)
        tags.set_active(self.tags.index(self.tag_active))

        # Filter
        filters_in_dropdown = Gtk.ListStore(str)
        for index, filter in enumerate(self.filters):
                filters_in_dropdown.append([filter])
        filters = Gtk.ComboBox.new_with_model(filters_in_dropdown)
        renderer_text1 = Gtk.CellRendererText()
        filters.pack_start(renderer_text1, True)
        filters.add_attribute(renderer_text1, "text", 0)
        filters.connect('changed',self.save_filter)
        toolbar.pack_start(filters, True, True, 0)
        filters.set_active(self.filters.index(self.filter_active))
        self.filters_elem = filters

        # Date filter
        date_filters_in_dropdown = Gtk.ListStore(str)
        for index, filter in enumerate(self.date_filters):
                date_filters_in_dropdown.append([filter])
        date_filters = Gtk.ComboBox.new_with_model(date_filters_in_dropdown)
        renderer_text1 = Gtk.CellRendererText()
        date_filters.pack_start(renderer_text1, True)
        date_filters.add_attribute(renderer_text1, "text", 0)
        date_filters.connect('changed',self.save_date_filter)
        toolbar.pack_start(date_filters, True, True, 0)
        date_filters.set_active(self.date_filters.index(self.date_filter_active))

        lights_off_btn = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_INFO))
        lights_off_btn.connect("clicked",self.lights_off)
        toolbar.pack_start(lights_off_btn, True, True, 0)

    def lights_off(self,widget):
        if self.get_opacity() == 1:
            self.set_opacity(0.5)
        else:
            self.set_opacity(1)

    def save_filter(self,widget=None):
            self.filter_active = self.filters[widget.get_active()]
            self.add_pages(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
            self.add_tasks_lists(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)

    def save_date_filter(self,widget=None):
            self.date_filter_active = self.date_filters[widget.get_active()]
            self.add_pages(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
            self.add_tasks_lists(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)

    def save_tag(self,widget=None):
            self.tag_active = self.tags[widget.get_active()]
            self.add_pages(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)
            self.add_tasks_lists(filter_by=self.filter_active,tag=self.tag_active,date_filter=self.date_filter_active)

    def export_tasks(self):
         with open(cwd+'/database.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.tasks_list[0].__dict__.keys())
            writer.writeheader()
            for task in self.tasks_list:
                writer.writerow(task.__dict__)

    def import_tasks(self):
        with open(cwd+'/database.csv', mode='r') as infile:
            DictReader_obj = csv.DictReader(infile)
            for item in DictReader_obj:
                self.tasks_list.append(Task(name=item["name"],done=strtobool(item["done"]), notes=item["notes"], 
                recurring=strtobool(item["recurring"]), date_started=item["date_started"], date_to_do=item["date_to_do"],
                star=strtobool(item["star"]),tags=next((tag for tag in self.tags_list if tag.name == item['tags']), None),last_done=item["last_done"],
                recurring_type=item["recurring_type"],recurring_value=item["recurring_value"]))



win = MyWindow(0)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

# Save filters
filters_exported = {
        'filter_active': win.filter_active,
        'tag_active': win.tag_active,
        'date_filter_active': win.date_filter_active,
}
pickle.dump(filters_exported, open(pickle_file, "wb"))
