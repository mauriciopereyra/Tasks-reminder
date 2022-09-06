import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from task import Task
from tag import Tag
from datetime import datetime, date
from recurring import Recurring

class Create(Gtk.Box):

        def __init__(self,window,current_task,tags_list,widget=None):
                # self
                # self = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
                super().__init__(orientation=Gtk.Orientation.VERTICAL,spacing=6)
                self.set_margin_top(25)
                self.set_margin_right(25)
                self.set_margin_bottom(25)
                self.set_margin_left(25)
                self.current_task = current_task
                self.window = window

                # BOXES
                # Top box
                box_top = Gtk.Box(spacing=6)
                # box_top.set_vexpand(True)
                box_top.set_valign(Gtk.Align.START)
                self.add(box_top)
                
                # Tag
                tag = Gtk.Label(self.current_task.tags)
                self.pack_start(tag, True, True, 0)

                # Task
                task = Gtk.Entry()
                task.set_vexpand(False)
                # task.set_line_wrap(True)
                task.connect("key-release-event",self.save_task)
                self.pack_start(task, True, True, 0)


                # Middle box
                box_middle = Gtk.Box(spacing=6)
                box_middle.set_vexpand(True)
                # box_middle.set_valign(Gtk.Align.CENTER)
                self.add(box_middle)


                # Notes
                notes = Gtk.Entry()
                notes.set_valign(Gtk.Align.START)
                notes.connect("key-release-event",self.save_notes)
                self.pack_start(notes, True, True, 0)

                # Bottom box
                box_bottom = Gtk.Box(spacing=6)
                box_bottom.set_vexpand(True)
                box_bottom.set_valign(Gtk.Align.END)
                self.add(box_bottom)

                recurring_info = Gtk.Label(label="")
                box_bottom.pack_start(recurring_info,True,True,0)

                # Middle left box
                box_middle_left = Gtk.Box(spacing=6)
                box_middle_left.set_hexpand(True)
                box_middle.add(box_middle_left)

                # Middle center box
                box_middle_center = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
                box_middle_center.set_hexpand(True)
                box_middle.add(box_middle_center)

                # Middle right box
                box_middle_right = Gtk.Box(spacing=6)
                box_middle_right.set_hexpand(True)
                box_middle.add(box_middle_right)



                # WIDGETS
                # remove <- Add/edit tags, 
                remove = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_CLOSE))
                remove.connect("clicked", self.on_clicking_remove)
                box_top.pack_start(remove, True, True, 0)

                # Recurring
                recurring = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
                recurring.connect("clicked",self.on_clicking_recurring)
                box_top.pack_start(recurring, True, True, 0)

                # Date
                date = Gtk.Entry()
                date.connect("changed",self.save_date)
                box_top.pack_start(date, True, True, 0)

                # Star
                star = Gtk.CheckButton(image=Gtk.Image(stock=Gtk.STOCK_ABOUT))
                star.connect("clicked",self.save_star)
                box_top.pack_start(star, True, True, 0)

                # New
                new = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_ADD))
                new.connect("clicked",self.on_clicking_new)
                box_top.pack_start(new, True, True, 0)

                # Done
                done = Gtk.CheckButton(image=Gtk.Image(stock=Gtk.STOCK_APPLY))
                done.set_halign(Gtk.Align.CENTER)
                done.set_hexpand(True)
                done.connect("released",self.toggle_done)
                box_middle_center.pack_start(done, True, True, 0)

                # Back
                back = Gtk.Button(label="<-")
                back.connect("clicked",self.previous_task)
                box_middle_left.pack_start(back, True, True, 0)

                # Forward
                forward = Gtk.Button(label="->")
                forward.connect("clicked",self.next_task)
                box_middle_right.pack_start(forward, True, True, 0)

                task.set_text(current_task.name)
                done.set_active(current_task.done)
                notes.set_text(current_task.notes)
                date.set_text(current_task.date_to_do.strftime("%Y-%m-%d"))
                star.set_active(current_task.star)

                if current_task.recurring:
                        if current_task.recurring_type == 'days':
                                recurring_info.set_text("Every {} days".format(current_task.recurring_value))
                                # current_task.recurring_value
                        elif current_task.recurring_type == 'weekday':
                                recurring_info.set_text("Every {}".format(current_task.recurring_value))
                                # current_task.recurring_value
                        elif current_task.recurring_type == 'month':
                                recurring_info.set_text("Every month")


                for element in self.get_children():
                        element.show()
                        if type(element) == Gtk.Box:
                                for subelement in element.get_children():
                                        subelement.show()
                                        if type(subelement) == Gtk.Box:
                                                for subsubelement in subelement.get_children():
                                                        subsubelement.show()

                date.show()


        def save_recurring(self,widget=None):
                self.current_task.recurring = widget.get_active()
                self.window.export_tasks()

        def save_date(self,widget=None):
                try: self.current_task.date_to_do = datetime.strptime(widget.get_text(),"%Y-%m-%d").date()
                except: pass
                self.window.export_tasks()

        def save_star(self,widget=None):
                self.current_task.star = widget.get_active()
                self.window.export_tasks()

        def save_task(self,widget,event_key):
                self.current_task.name = widget.get_text()
                self.window.export_tasks()

        def save_notes(self,widget,event_key):
                self.current_task.notes = widget.get_text()
                self.window.export_tasks()

        def toggle_done(self,widget):
                # current_page = self.window.tasks_notebook.get_current_page() # if setting as done
                self.current_task.done = widget.get_active()
                if self.current_task.done:
                        self.current_task.last_done = date.today()
                # print(self.current_task.name)
                self.window.export_tasks()
                self.window.add_pages(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
                self.window.add_tasks_lists(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)            
        
        def previous_task(self,widget):
                self.window.tasks_notebook.prev_page()

        def next_task(self,widget):
                self.window.tasks_notebook.next_page()

        # Remove task
        def RemoveTaskDialog(self,widget):
                dialog = Gtk.Dialog(title="Remove task", flags=0)
                dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
                )

                dialog.set_default_size(150, 100)
                dialog.move(1500,500)

                label = Gtk.Label(label="Are you sure you want to remove this task?")
                label.props.margin_left = 20
                label.props.margin_right = 20
                label.props.margin_top = 20
                label.props.margin_bottom = 20

                box = dialog.get_content_area()
                box.add(label)
                dialog.show_all()
                return dialog


        def on_clicking_remove(self,widget):
                current_page = self.window.tasks_notebook.get_current_page()

                dialog = self.RemoveTaskDialog(self)
                response = dialog.run()

                if response == Gtk.ResponseType.OK:
                        self.window.tasks_list.remove(self.current_task)
                        self.window.add_pages(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
                        self.window.add_tasks_lists(filter_by=self.window.filter_active,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
                elif response == Gtk.ResponseType.CANCEL:
                        pass

                self.window.tasks_notebook.set_current_page(current_page)

                dialog.destroy()


        def on_clicking_new(self,widget):
                current_tag = self.window.tag_active

                if current_tag == "All":
                        current_tag = next(iter([tag for tag in self.window.tags_list if tag.name == "Mauricio"]))
                else:
                        current_tag = next(iter([tag for tag in self.window.tags_list if tag.name == self.window.tag_active]))

                self.window.tasks_list.append(Task(name="New",done=False, notes="", recurring=False, date_started=None, date_to_do=None,star=False,tags=current_tag))
                
                filter_to_set = self.window.filter_active
                if filter_to_set == 'Done': filter_to_set = 'All'
                # Checking filter active
                self.window.add_pages(filter_by=filter_to_set,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
                self.window.add_tasks_lists(filter_by=filter_to_set,tag=self.window.tag_active,date_filter=self.window.date_filter_active)
                self.window.filters_elem.set_active(self.window.filters.index(filter_to_set))
                
                self.window.tasks_notebook.set_current_page((int(next(iter([index for (index, page) in enumerate(self.window.tasks_notebook.get_children()) if page.current_task.name == "New"])))))

                self.window.connect("destroy", Gtk.main_quit)
                self.window.show_all()
                Gtk.main()

        def on_clicking_recurring(self,widget):
                task_selected_name = self.window.tasks_notebook.get_tab_label_text(self.window.tasks_notebook.get_nth_page(self.window.tasks_notebook.get_current_page()))
                task_selected = next(iter([task for task in self.window.tasks_list if task.name == task_selected_name]))
                win = Recurring(task_selected)
                win.window.connect("destroy", Gtk.main_quit)
                win.window.show_all()
                Gtk.main()
                if win.info['recurring_type']:
                        task_selected.recurring = True
                        task_selected.recurring_type = win.info['recurring_type']
                        task_selected.recurring_value = win.info['value']
                        task_selected.date_started = datetime.strptime(win.info['startdate'],"%d/%m/%Y").date() 
                else:
                        task_selected.recurring = False
                        task_selected.recurring_type = None
                        task_selected.recurring_value = None                        

                self.window.export_tasks()