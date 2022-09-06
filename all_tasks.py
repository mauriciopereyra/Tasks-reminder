import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from datetime import date

class main(Gtk.Box):

    def __init__(self,window,tasks_list,tags_list,widget=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.window = window
        # WRAPPER
        self.set_margin_top(25)
        self.set_margin_right(25)
        self.set_margin_bottom(25)
        self.set_margin_left(25)

        # BOXES
        # Top box
        self.box_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.box_top.set_vexpand(True)
        self.box_top.set_valign(Gtk.Align.START)
        self.add(self.box_top)

        # List header
        self.frame = Gtk.Frame()
        self.box_top.pack_start(self.frame, True, True, 0)

        # Create list
        self.list_box = Gtk.ListBox(visible=True)
        self.frame.add(self.list_box)

        self.list_box.connect("row-activated",self.open_task)


    def toggle_done(self,widget):
            # current_page = self.window.tasks_notebook.get_current_page() # if setting as done
            widget.task.done = widget.get_active()
            if widget.task.done:
                widget.task.last_done = date.today()
            self.window.export_tasks()
            self.window.add_pages(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
            self.window.add_tasks_lists(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)            

    def open_task(self,widget,row):
        if row:
            self.window.toggle_view()
            self.window.tasks_notebook.set_current_page(row.get_index())