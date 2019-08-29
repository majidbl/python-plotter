import gi
from func.plot2DFunc import plot2DF
import pickle
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class plot2DUtils(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self.input_File = []
        self.Styles = "-"
        self.legend_Entry_txt = " "
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.Color = "b"
        self.Market = "None"
        self.plot_state = "Seperate"
        self.plot_func = "Sin"
        self.legend_loc = "best"
        self.edited_List = []
        menutoolbar = Gtk.Toolbar()
        self.pack_start(menutoolbar, False, False, 0)
        
        file_ToolButton = Gtk.ToolButton(Gtk.STOCK_FILE)
        menutoolbar.insert(file_ToolButton, 0)
        file_ToolButton.connect("clicked", self.on_file_clicked)
        file_ToolButton.set_tooltip_text("Select Plot Data File")
        
        add_ToolButton = Gtk.ToolButton(Gtk.STOCK_ADD)
        menutoolbar.insert(add_ToolButton, 1)
        add_ToolButton.connect("clicked", self.add_cb)
        add_ToolButton.set_tooltip_text("Add Data Row To Table")
        
        about_ToolButton = Gtk.ToolButton(Gtk.STOCK_EDIT)
        menutoolbar.insert(about_ToolButton, 2)
        about_ToolButton.connect("clicked", self.edit_cb)
        about_ToolButton.set_tooltip_text("Edit Selected Row!")
        
        plot_ToolButton = Gtk.ToolButton(Gtk.STOCK_MEDIA_PLAY)
        menutoolbar.insert(plot_ToolButton, 3)
        plot_ToolButton.connect("clicked", self.on_Plot_clicked)
        plot_ToolButton.set_tooltip_text("PlotM")
        
        save_ToolButton = Gtk.ToolButton(Gtk.STOCK_SAVE)
        menutoolbar.insert(save_ToolButton, 4)
        save_ToolButton.connect("clicked", self.on_Save_Plot_Clicked)
        save_ToolButton.set_tooltip_text("Save All Row in Table!")
        
        remove_all_ToolButton = Gtk.ToolButton(Gtk.STOCK_REFRESH)
        menutoolbar.insert(remove_all_ToolButton, 5)
        remove_all_ToolButton.connect("clicked", self.remove_all_cb)
        remove_all_ToolButton.set_tooltip_text("Remove All Row From Table!")
        
        remove_ToolButton = Gtk.ToolButton(Gtk.STOCK_DELETE)
        menutoolbar.insert(remove_ToolButton, 6)
        remove_ToolButton.connect("clicked", self.remove_cb)
        remove_ToolButton.set_tooltip_text("Remove Selected Row From Table!")
        
        type_Plot_ToolButton = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_LEFT)
        menutoolbar.insert(type_Plot_ToolButton, 7)
        type_Plot_ToolButton.connect("clicked", self.on_type_Plot_clicked)
        type_Plot_ToolButton.set_tooltip_text("Type Plot Data!")
        
        legend_ToolButton = Gtk.ToolButton(Gtk.STOCK_DND_MULTIPLE)
        legend_ToolButton.set_tooltip_text("Legend Loc!")
        menutoolbar.insert(legend_ToolButton, 8)
        legend_ToolButton.connect("clicked", self.on_legend_Plot_clicked)
        
        save_layout_ToolButton = Gtk.ToolButton(Gtk.STOCK_JUMP_TO)
        save_layout_ToolButton.set_tooltip_text("save Layout!")
        menutoolbar.insert(save_layout_ToolButton, 9)
        save_layout_ToolButton.connect("clicked", self.on_save_Layout_clicked)
        
        load_layout_ToolButton = Gtk.ToolButton(Gtk.STOCK_OPEN)
        load_layout_ToolButton.set_tooltip_text("Load Layout!")
        menutoolbar.insert(load_layout_ToolButton, 10)
        load_layout_ToolButton.connect("clicked",
                                       self.on_load_Layout_clicked)
        self.store = Gtk.ListStore(str, str, str, str, str,
                                   str, str, str)
        view = Gtk.TreeView(model=self.store)
        i = 0
        tilte_List = ['File Name', 'Style', 'Legend',
                      'X Axis', 'Y Axis', 'Color', 'Market',
                      'Func']
        for titles in tilte_List:
            renderer_1 = Gtk.CellRendererText()
            column_1 = Gtk.TreeViewColumn(titles, renderer_1, text=i)
            column_1.set_sort_column_id(i)
            view.append_column(column_1)
            i = i + 1
        # when a row of the treeview is selected, it emits a signal
        self.selection = view.get_selection()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(view)
        scrolled_window.set_min_content_height(200)
        self.pack_start(scrolled_window, True, True, 0)

    def on_file_clicked(self, widget):
        self.input_File = []
        self.Styles = "-"
        self.legend_Entry_txt = " "
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.Color = "b"
        self.Market = "None"
        self.plot_state = "Seperate"
        self.plot_func = "Sin"
        self.legend_loc = "upper right"
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)
        dialog.set_select_multiple(True)
        Gtk.FileChooser.set_select_multiple(dialog, True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("Files selected: ", dialog.get_filenames())
            self.input_File = dialog.get_filenames()
            print("File selected: ", len(self.input_File))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_style_ComboBox_Changed(self, combo):
            tree_iter = combo.get_active_iter()
            if tree_iter is not None:
                model = combo.get_model()
                self.Styles = model[tree_iter][0]
                print(self.Styles)

    def on_color_ComboBox_Changed(self, combo):
            tree_iter = combo.get_active_iter()
            if tree_iter is not None:
                model = combo.get_model()
                self.Color = model[tree_iter][0]
                print(self.Color)
            if self.Color == 'Red':
                self.Color = 'r'
            elif self.Color == 'Green':
                self.Color = 'g'
            elif self.Color == 'Blue':
                self.Color = 'b'
            elif self.Color == 'Yellow':
                self.Color = 'y'
            elif self.Color == 'Black':
                self.Color = 'k'
            elif self.Color == "Cyan":
                self.Color = 'c'
            elif self.Color == "Magenta":
                self.Color = 'm'
            elif self.Color == "White":
                self.Color = 'w'

    def on_market_ComboBox_Changed(self, combo):
            tree_iter = combo.get_active_iter()
            if tree_iter is not None:
                model = combo.get_model()
                self.Market = model[tree_iter][0]
                print(self.Market)

    def on_x_Entry_Changed(self, entry):
            self.x_Entry_txt = entry.get_text()

    def on_y_Entry_Changed(self, entry):
            self.y_Entry_txt = entry.get_text()

    def on_legend_Entry_Changed(self, entry):
        leg = entry.get_text()
        self.legend_Entry_txt = entry.get_text()
        return leg

    def get_legend_(self, entry):
        leg = entry.get_text()
        return leg

    def get_x_Entry(self, entry):
        x_entry = entry.get_text()
        return x_entry

    def get_y_Entry(self, entry):
        y_entry = entry.get_text()
        return y_entry

    def on_Plot_clicked(self, widget, data=None):
        myplot2DF = plot2DF()
        if len(self.store) > 0:
            myplot2DF.plotting(self.store, self.plot_state, self.legend_loc)
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Add One Or More Row To Plot")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                            dialog.destroy()

    def on_Cancel_clicked(self, widget):
        print("Cancel")

    def on_dialog_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO,
                                   "This is an QUESTION MessageDialog")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
        elif response == Gtk.ResponseType.NO:
            print("QUESTION dialog closed by clicking NO button")

        dialog.destroy()

    def on_x_y_dialog_clicked(self, widget):
        file_Label = self.input_File.split('/')
        d_file_Label_r = Gtk.Label(file_Label[-1])
        if file_Label[-1] == ' ':
            # self.on_dialog_clicked()
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "File Data For Plot Not Selected!")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                            dialog.destroy()
        elif file_Label[-1] != ' ':
            winEdit = Gtk.Window()
            d_file_Label_l = Gtk.Label("File Data")
            d_x_entry = Gtk.Entry()
            d_x_entry.connect("changed", self.on_x_Entry_Changed)
            d_x_label = Gtk.Label("X Axis : ")
            d_y_entry = Gtk.Entry()
            d_y_entry.connect("changed", self.on_y_Entry_Changed)
            d_y_label = Gtk.Label("Y Axis : ")
            d_color_Label = Gtk.Label("Color : ")
            d_color_Store = Gtk.ListStore(str)
            colors = ["Green", "Red", "Blue", "Yellow", "Black", "Cyan",
                      "Magenta", "White"]
            for color in colors:
                    d_color_Store.append([color])
            color_ComboBox = Gtk.ComboBox.new_with_model(d_color_Store)
            color_ComboBox.connect("changed", self.on_color_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            color_ComboBox.pack_start(renderer_text, True)
            color_ComboBox.add_attribute(renderer_text, "text", 0)
            d_legend_Label = Gtk.Label("Legend :")
            d_legend_Entry = Gtk.Entry()
            d_legend_Entry.connect("changed", self.on_legend_Entry_Changed)
            d_market_Label = Gtk.Label("Market : ")
            d_market_Store = Gtk.ListStore(str)
            markets = [".", ",", "o", "*", "+", "s", "P", "p", "D", "d", "<",
                       ">", "1", "2", "3", "4", "H", "v", "h", "|", "None"]
            for market in markets:
                    d_market_Store.append([market])
            d_market_ComboBox = Gtk.ComboBox.new_with_model(d_market_Store)
            d_market_ComboBox.connect("changed",
                                      self.on_market_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            d_market_ComboBox.pack_start(renderer_text, True)
            d_market_ComboBox.add_attribute(renderer_text, "text", 0)
            d_style_Label = Gtk.Label("Style : ")
            # d_style_Label.set_xalign(xalign=1)
            d_style_Store = Gtk.ListStore(str)
            styles = ["-", "--", ":", "-.", "None"]
            for style in styles:
                    d_style_Store.append([style])
            d_style_ComboBox = Gtk.ComboBox.new_with_model(d_style_Store)
            d_style_ComboBox.connect("changed", self.on_style_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            d_style_ComboBox.pack_start(renderer_text, True)
            d_style_ComboBox.add_attribute(renderer_text, "text", 0)
            d_func_Label = Gtk.Label("Func Plot : ")
            d_func_Store = Gtk.ListStore(str)
            funcs = ["Cos", "Sin", "log", "e", "None"]
            for func in funcs:
                    d_func_Store.append([func])
            d_func_ComboBox = Gtk.ComboBox.new_with_model(d_func_Store)
            d_func_ComboBox.connect("changed", self.on_func_ComboBox_Changed)
            renderer_textf = Gtk.CellRendererText()
            d_func_ComboBox.pack_start(renderer_textf, True)
            d_func_ComboBox.add_attribute(renderer_textf, "text", 0)
            ok_Button = Gtk.Button("OK")
            ok_Button.connect("clicked", self.on_ok_Bottun_Clicked, winEdit)
            cancel_Button = Gtk.Button("Cancel"	)
            cancel_Button.connect("clicked", self.on_cancel_Bottun_Clicked, winEdit)
            d_grid = Gtk.Grid()
            d_grid.set_border_width(20)
            d_grid.set_column_spacing(10)
            d_grid.set_row_spacing(10)
            d_grid.attach(d_file_Label_l, 0, 0, 1, 1)
            d_grid.attach(d_file_Label_r, 1, 0, 1, 1)
            d_grid.attach(d_x_label, 0, 1, 1, 1)
            d_grid.attach(d_x_entry, 1, 1, 1, 1)
            d_grid.attach(d_y_label, 0, 2, 1, 1)
            d_grid.attach(d_y_entry, 1, 2, 1, 1)
            d_grid.attach(d_color_Label, 0, 3, 1, 1)
            d_grid.attach(color_ComboBox, 1, 3, 1, 1)
            d_grid.attach(d_legend_Label, 0, 4, 1, 1)
            d_grid.attach(d_legend_Entry, 1, 4, 1, 1)
            d_grid.attach(d_market_Label, 0, 5, 1, 1)
            d_grid.attach(d_market_ComboBox, 1, 5, 1, 1)
            d_grid.attach(d_style_Label, 0, 6, 1, 1)
            d_grid.attach(d_style_ComboBox, 1, 6, 1, 1)
            d_grid.attach(d_func_Label, 0, 7, 1, 1)
            d_grid.attach(d_func_ComboBox, 1, 7, 1, 1)
            d_grid.attach(ok_Button, 0, 8, 1, 1)
            d_grid.attach(cancel_Button, 1, 8, 1, 1)
            d_grid.show_all()
            winEdit.add(d_grid)
            winEdit.show()

    def on_ok_Bottun_Clicked(self, button, window):
        dialog_update = Gtk.MessageDialog(None, 0,
                                          Gtk.MessageType.QUESTION,
                                          Gtk.ButtonsType.CLOSE,
                                          "Data For Plot Updated With New Value!")
        response_update = dialog_update.run()
        if response_update == Gtk.ResponseType.CLOSE:
            dialog_update.destroy()
        window.destroy()

    def on_cancel_Bottun_Clicked(self, button, window):
        self.input_File = " "
        self.Styles = "-"
        self.legend_Entry_txt = self.input_File
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.Color = "b"
        self.Market = "None"
        self.plot_func = "Sin"
        window.destroy()

    def remove_cb(self, button):
        # if there is still an entry in the model
        if len(self.store) != 0:
            # get the selection
            (model, iter) = self.selection.get_selected()
            # if there is a selection, print a message in the terminal
            # and remove it from the model
            # for i in model:
            #    for j in i:
            #        print(j)
            print("%s has been removed" % (model[iter][1]))
            print("model is : ", model[iter])
            print("iter is : ", iter)
            mylist = []
            for j in model[iter]:
                mylist.append(j)
                # print(j)
            print(mylist)
            mylist[0] = ' '
            print(mylist)
            self.store.remove(iter)
        # otherwise, ask the user to select something to remove
        else:
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Select a Row to remove")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()

            print("Select a title to remove")
            # else, if there are no entries in the model, print "Empty list"
            # in the terminal
            print("Empty list")

    def on_save_Layout_clicked(self, widget):
        # if there is still an entry in the model
        if len(self.store) != 0:
            print(len(self.store))
            mylist = []
            for row in self.store:
                # Print values of all columns
                mylist.append(row[:])
                print(row[:])
            print(mylist)
            layout_Name = "Test.mpl"
            # get the selection
            dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE,
                                            Gtk.ResponseType.OK))
            self.add_filters(dialog)

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                print("Open clicked")
                print("File selected: " + dialog.get_filename())
                layout_Name = dialog.get_filename()
                with open(layout_Name, "wb") as fp:   # Pickling
                        pickle.dump(mylist, fp)
            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel clicked")
            dialog.destroy()
            # self.store.remove(iter)
        # otherwise, ask the user to select something to remove
        else:
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "There Is Nothing For Save!!!")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()

    def on_load_Layout_clicked(self, widget):
        # if there is still an entry in the model
        # get the selection
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK,
                                        Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            layout_LName = dialog.get_filename()
            with open(layout_LName, "rb") as fp:   # Pickling
                b = pickle.load(fp)
            for List in b:
                self.store.append(List)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()
        # self.store.remove(iter)
        # otherwise, ask the user to select something to remove

    def edit_cb(self, button):
        if len(self.store) != 0:
            # get the selection
            (model, iter) = self.selection.get_selected()
            # if there is a selection, print a message in the terminal
            # and remove it from the model
            if iter is not None:
                # iter1 = self.store.prepend([-1, 1, -1])
                # self.store.swap(iter, iter1)
                mylist = []
                for j in model[iter]:
                    mylist.append(j)
                    self.edited_List.append(j)
                self.store.remove(iter)
                # self.input_File = self.edited_List[0]
                self.Styles = self.edited_List[1]
                self.legend_Entry_txt = self.edited_List[2]
                self.x_Entry_txt = self.edited_List[3]
                self.y_Entry_txt = self.edited_List[4]
                self.Color = self.edited_List[5]
                self.Market = self.edited_List[6]
                self.plot_func = self.edited_List[7]
                # print(j)
                # mylist[0] = ' '
                file_Label = mylist[0].split('/')
                d_file_Label_r = Gtk.Label(file_Label[-1])
                if file_Label[-1] == ' ':
                    # self.on_dialog_clicked()
                    dialog = Gtk.MessageDialog(None, 0,
                                               Gtk.MessageType.QUESTION,
                                               Gtk.ButtonsType.CLOSE,
                                               "File Data For Plot Not Selected!")
                    response = dialog.run()
                    if response == Gtk.ResponseType.CLOSE:
                        dialog.destroy()
                elif file_Label[-1] != ' ':
                    winEdit = Gtk.Window()
                    d_file_Label_l = Gtk.Label("File Data")
                    d_x_entry = Gtk.Entry()
                    d_x_entry.connect("changed", self.on_x_Entry_Changed)
                    d_x_label = Gtk.Label("X Axis : ")
                    d_y_entry = Gtk.Entry()
                    d_y_entry.connect("changed", self.on_y_Entry_Changed)
                    d_y_label = Gtk.Label("Y Axis : ")
                    d_color_Label = Gtk.Label("Color : ")
                    d_color_Store = Gtk.ListStore(str)
                    colors = ["Green", "Red", "Blue", "Yellow", "Black",
                              "Cyan", "Magenta", "White"]
                    for color in colors:
                        d_color_Store.append([color])
                    color_ComboBox = Gtk.ComboBox.new_with_model(d_color_Store)
                    color_ComboBox.connect("changed",
                                           self.on_color_ComboBox_Changed)
                    renderer_text = Gtk.CellRendererText()
                    color_ComboBox.pack_start(renderer_text, True)
                    color_ComboBox.add_attribute(renderer_text, "text", 0)
                    d_legend_Label = Gtk.Label("Legend :")
                    # d_legend_Label.set_xalign(xalign=1)
                    d_legend_Entry = Gtk.Entry()
                    d_legend_Entry.connect("changed",
                                           self.on_legend_Entry_Changed)
                    d_market_Label = Gtk.Label("Market : ")
                    d_market_Store = Gtk.ListStore(str)
                    markets = [".", ",", "o", "*", "+", "s", "P", "p", "D",
                               "d", "None"]
                    for market in markets:
                        d_market_Store.append([market])
                    d_market_ComboBox = Gtk.ComboBox.new_with_model(d_market_Store)
                    d_market_ComboBox.connect("changed",
                                              self.on_market_ComboBox_Changed)
                    renderer_text = Gtk.CellRendererText()
                    d_market_ComboBox.pack_start(renderer_text, True)
                    d_market_ComboBox.add_attribute(renderer_text, "text", 0)
                    d_style_Label = Gtk.Label("Style : ")
                    # d_style_Label.set_xalign(xalign=1)
                    d_style_Store = Gtk.ListStore(str)
                    styles = ["-", "--", ":", "-.", "None"]
                    for style in styles:
                        d_style_Store.append([style])
                    d_style_ComboBox = Gtk.ComboBox.new_with_model(d_style_Store)
                    d_style_ComboBox.connect("changed",
                                             self.on_style_ComboBox_Changed)
                    renderer_text = Gtk.CellRendererText()
                    d_style_ComboBox.pack_start(renderer_text, True)
                    d_style_ComboBox.add_attribute(renderer_text, "text", 0)
                    d_func_Label = Gtk.Label("Func Plot : ")
                    d_func_Store = Gtk.ListStore(str)
                    funcs = ["Cos", "Sin", "log", "e", "None"]
                    for func in funcs:
                        d_func_Store.append([func])
                    d_func_ComboBox = Gtk.ComboBox.new_with_model(d_func_Store)
                    d_func_ComboBox.connect("changed",
                                            self.on_func_ComboBox_Changed)
                    renderer_textf = Gtk.CellRendererText()
                    d_func_ComboBox.pack_start(renderer_textf, True)
                    d_func_ComboBox.add_attribute(renderer_textf, "text", 0)
                    ok_Button = Gtk.Button("Apply")
                    ok_Button.connect("clicked",
                                      self.on_ok_Edit_Bottun_Clicked,
                                      winEdit)
                    cancel_Button = Gtk.Button("Cancel")
                    cancel_Button.connect("clicked",
                                          self.on_cancel_Edit_Bottun_Clicked,
                                          winEdit)
                    d_grid = Gtk.Grid()
                    d_grid.set_border_width(20)
                    d_grid.set_column_spacing(10)
                    d_grid.set_row_spacing(10)
                    d_grid.attach(d_file_Label_l, 0, 0, 1, 1)
                    d_grid.attach(d_file_Label_r, 1, 0, 1, 1)
                    d_grid.attach(d_x_label, 0, 1, 1, 1)
                    d_grid.attach(d_x_entry, 1, 1, 1, 1)
                    d_grid.attach(d_y_label, 0, 2, 1, 1)
                    d_grid.attach(d_y_entry, 1, 2, 1, 1)
                    d_grid.attach(d_color_Label, 0, 3, 1, 1)
                    d_grid.attach(color_ComboBox, 1, 3, 1, 1)
                    d_grid.attach(d_legend_Label, 0, 4, 1, 1)
                    d_grid.attach(d_legend_Entry, 1, 4, 1, 1)
                    d_grid.attach(d_market_Label, 0, 5, 1, 1)
                    d_grid.attach(d_market_ComboBox, 1, 5, 1, 1)
                    d_grid.attach(d_style_Label, 0, 6, 1, 1)
                    d_grid.attach(d_style_ComboBox, 1, 6, 1, 1)
                    d_grid.attach(d_func_Label, 0, 7, 1, 1)
                    d_grid.attach(d_func_ComboBox, 1, 7, 1, 1)
                    d_grid.attach(ok_Button, 0, 8, 1, 1)
                    d_grid.attach(cancel_Button, 1, 8, 1, 1)
                    d_grid.show_all()
                    winEdit.add(d_grid)
                    winEdit.show()
                # otherwise, ask the user to select something to remove
            else:
                dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                           Gtk.ButtonsType.CLOSE,
                                           "Select a Row to remove")
                response = dialog.run()
                if response == Gtk.ResponseType.CLOSE:
                    dialog.destroy()

                print("Select a title to remove")
            # else, if there are no entries in the model, print "Empty list"
            # in the terminal
        else:
            print("Empty list")
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Empty list")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()
            print("Select a title to remove")
            # else, if there are no entries in the model, print "Empty list"
            # in the terminal

    def on_ok_Edit_Bottun_Clicked(self, button, window):
        if self.Styles != self.edited_List[1]:
            self.edited_List[1] = self.Styles
        if self.legend_Entry_txt != self.edited_List[2]:
            self.edited_List[2] = self.legend_Entry_txt
        if self.x_Entry_txt != self.edited_List[3]:
            self.edited_List[3] = self.x_Entry_txt
        if self.y_Entry_txt != self.edited_List[4]:
            self.edited_List[4] = self.y_Entry_txt
        if self.Color != self.edited_List[5]:
            self.edited_List[5] = self.Color
        if self.Market != self.edited_List[6]:
            self.edited_List[6] = self.Market
        if self.plot_func != self.edited_List[7]:
            self.edited_List[7] = self.plot_func
        print(self.edited_List)
        self.store.append(self.edited_List)
        self.edited_List = []
        dialog_update = Gtk.MessageDialog(None, 0,
                                          Gtk.MessageType.QUESTION,
                                          Gtk.ButtonsType.CLOSE,
                                          "Data For Plot Updated With New Value!")
        response_update = dialog_update.run()
        if response_update == Gtk.ResponseType.CLOSE:
            dialog_update.destroy()
        window.destroy()

    def on_cancel_Edit_Bottun_Clicked(self, button, window):
        self.store.append(self.edited_List)
        self.edited_List = []
        window.destroy()

    def remove_all_cb(self, button):
        # if there is still an entry in the model
        if len(self.store) != 0:
            # remove all the entries in the model
            for i in range(len(self.store)):
                iter = self.store.get_iter(0)
                self.store.remove(iter)
        # print a message in the terminal alerting that the model is empty
        print("Empty list")

    def add_cb(self, button):
        if len(self.input_File) == 0:
            dialog_add = Gtk.MessageDialog(None, 0,
                                           Gtk.MessageType.QUESTION,
                                           Gtk.ButtonsType.CLOSE,
                                           "First Select Data File!")
            response_add = dialog_add.run()
            if response_add == Gtk.ResponseType.CLOSE:
                            dialog_add.destroy()
            dialog_add.destroy()
        else:
            # append to the model the title that is in the entry
            # for b in self.input_File:
            #    print(b)
            for i in self.input_File:
                fileName_list = i
                style_list = self.Styles
                legend_list = self.legend_Entry_txt
                x_Axis_list = self.x_Entry_txt
                y_Axis_list = self.y_Entry_txt
                color_list = self.Color
                market_list = self.Market
                func_list = self.plot_func

                self.store.append([fileName_list, style_list, legend_list,
                                  x_Axis_list, y_Axis_list, color_list,
                                  market_list, func_list])

    def on_type_Plot_clicked(self, combo):
        if len(self.store) == 1:
            dialog_type = Gtk.MessageDialog(None, 0,
                                            Gtk.MessageType.QUESTION,
                                            Gtk.ButtonsType.CLOSE,
                                            "Data For Plot Most Two Or More!")
            response_update = dialog_type.run()
            if response_update == Gtk.ResponseType.CLOSE:
                            dialog_type.destroy()
        if len(self.store) == 0:
            dialog_type2 = Gtk.MessageDialog(None, 0,
                                             Gtk.MessageType.QUESTION,
                                             Gtk.ButtonsType.CLOSE,
                                             "Data For Plot Most Two Or More!")
            response_update = dialog_type2.run()
            if response_update == Gtk.ResponseType.CLOSE:
                            dialog_type2.destroy()
        if len(self.store) > 1:
            winType = Gtk.Window()
            t_type_g_Label = Gtk.Label("Select Your Type For Plotting default(Together)")
            t_type_Label = Gtk.Label("Market : ")
            # d_market_Label.set_xalign(xalign=1)
            t_type_Store = Gtk.ListStore(str)
            type_d = ["Together", "SubPlot-X", "SubPlot-Y", "Seperate"]
            for market in type_d:
                    t_type_Store.append([market])
            t_type_ComboBox = Gtk.ComboBox.new_with_model(t_type_Store)
            t_type_ComboBox.connect("changed",
                                    self.on_type_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            t_type_ComboBox.pack_start(renderer_text, True)
            t_type_ComboBox.add_attribute(renderer_text, "text", 0)
            ok_Type_Button = Gtk.Button("Ok")
            ok_Type_Button.connect("clicked", self.on_ok_Type_Bottun_Clicked, winType)
            grid_t = Gtk.Grid()
            grid_t.set_border_width(20)
            grid_t.set_column_spacing(10)
            grid_t.set_row_spacing(10)
            grid_t.attach(t_type_g_Label, 0, 0, 5, 1)
            grid_t.attach(t_type_Label, 0, 1, 1, 1)
            grid_t.attach(t_type_ComboBox, 1, 1, 4, 1)
            grid_t.attach(ok_Type_Button, 0, 2, 4, 1)
            grid_t.show_all()
            winType.add(grid_t)
            winType.show()

    def on_ok_Type_Bottun_Clicked(self, bottun, window):
        window.destroy()

    def on_type_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        type_ret = ' '
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_state = model[tree_iter][0]
            print(self.plot_state)
            type_ret = model[tree_iter][0]
        return type_ret

    def get_type_ComboBox(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_state = model[tree_iter][0]
            type_ret = model[tree_iter][0]
        return type_ret

    def on_legend_Plot_clicked(self, combo):
        if len(self.store) == 0:
            dialog_type = Gtk.MessageDialog(None, 0,
                                            Gtk.MessageType.QUESTION,
                                            Gtk.ButtonsType.CLOSE,
                                            "Data For Plot Most Two Or More!")
            response_update = dialog_type.run()
            if response_update == Gtk.ResponseType.CLOSE:
                            dialog_type.destroy()
        if len(self.store) > 0:
            winLegend = Gtk.Window()
            t_type_g_Label = Gtk.Label("Select Your Legend Position : ")
            t_type_Label = Gtk.Label("Location : ")
            t_type_Store = Gtk.ListStore(str)
            type_d = ["best", "upper right", "upper left", "lower left",
                      "lower right", "right", "center left", "center right",
                      "lower center", "upper center", "center"]
            for market in type_d:
                    t_type_Store.append([market])
            t_type_ComboBox = Gtk.ComboBox.new_with_model(t_type_Store)
            t_type_ComboBox.connect("changed",
                                    self.on_L_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            t_type_ComboBox.pack_start(renderer_text, True)
            t_type_ComboBox.add_attribute(renderer_text, "text", 0)
            ok_L_Button = Gtk.Button("Ok")
            ok_L_Button.connect("clicked", self.on_ok_L_Bottun_Clicked,
                                winLegend)
            grid_t = Gtk.Grid()
            grid_t.set_border_width(20)
            grid_t.set_column_spacing(10)
            grid_t.set_row_spacing(10)
            grid_t.attach(t_type_g_Label, 0, 0, 5, 1)
            grid_t.attach(t_type_Label, 0, 1, 1, 1)
            grid_t.attach(t_type_ComboBox, 1, 1, 4, 1)
            grid_t.attach(ok_L_Button, 0, 2, 4, 1)
            grid_t.show_all()
            winLegend.add(grid_t)
            winLegend.show()

    def on_ok_L_Bottun_Clicked(self, bottun, window):
        window.destroy()

    def on_L_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.legend_loc = model[tree_iter][0]
            print(self.legend_loc)

    def on_func_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        func_ret = ' '
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_func = model[tree_iter][0]
            print(self.plot_func)
            func_ret = model[tree_iter][0]
        return func_ret

    def get_func_ComboBox_(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            func_ret = model[tree_iter][0]
        return func_ret

    def on_Save_Plot_Clicked(self, button):
        myplot2DF = plot2DF()
        if len(self.store) > 0:
            myplot2DF.plot_Save(self.store, self.plot_state, self.legend_loc)
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Add One Or More Row To Plot")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                            dialog.destroy()