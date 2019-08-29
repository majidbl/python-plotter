import gi
from func.plotHistFunc import plotHistF
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class plotHistUtils(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self.input_File = " "
        self.legend_Entry_txt = self.input_File
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.Color = "b"
        self.Type = "bar"
        self.plot_state = "Seperate"
        self.plot_log = "False"
        self.n_Points_Plot = '20'
        menutoolbar = Gtk.Toolbar()
        self.pack_start(menutoolbar, False, False, 0)
        file_ToolButton = Gtk.ToolButton(Gtk.STOCK_FILE)
        menutoolbar.insert(file_ToolButton, 0)
        file_ToolButton.connect("clicked", self.on_file_clicked)
        file_ToolButton.set_tooltip_text("Select Plot Data File")
        x_y_ToolButton = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_LEFT)
        menutoolbar.insert(x_y_ToolButton, 1)
        x_y_ToolButton.connect("clicked", self.on_x_y_dialog_clicked)
        x_y_ToolButton.set_tooltip_text("Insert Details")
        add_ToolButton = Gtk.ToolButton(Gtk.STOCK_ADD)
        menutoolbar.insert(add_ToolButton, 2)
        add_ToolButton.connect("clicked", self.add_cb)
        add_ToolButton.set_tooltip_text("Add Data Row To Table")
        plot_ToolButton = Gtk.ToolButton(Gtk.STOCK_EXECUTE)
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
        remove_ToolButton = Gtk.ToolButton(Gtk.STOCK_EDIT)
        menutoolbar.insert(remove_ToolButton, 6)
        remove_ToolButton.connect("clicked", self.remove_cb)
        remove_ToolButton.set_tooltip_text("Remove Selected Row From Table!")
        type_Plot_ToolButton = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_LEFT)
        menutoolbar.insert(type_Plot_ToolButton, 7)
        type_Plot_ToolButton.connect("clicked", self.on_type_Plot_clicked)
        about_ToolButton = Gtk.ToolButton(Gtk.STOCK_ABOUT)
        type_Plot_ToolButton.set_tooltip_text("Type Plot Data!")
        menutoolbar.insert(about_ToolButton, 8)
        self.store = Gtk.ListStore(str, str, str, str,
                                   str, str, str, str)
        view = Gtk.TreeView(model=self.store)
        i = 0
        tilte_List = ['File Name', 'Legend',
                      'X Axis', 'Y Axis', 'Color', 'Type',
                      'Log', 'N Piont']
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
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.input_File = dialog.get_filename()
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

    def on_typeh_ComboBox_Changed(self, combo):
            tree_iter = combo.get_active_iter()
            if tree_iter is not None:
                model = combo.get_model()
                self.Type = model[tree_iter][0]
                print(self.Type)

    def on_x_Entry_Changed(self, entry):
            self.x_Entry_txt = entry.get_text()

    def on_y_Entry_Changed(self, entry):
            self.y_Entry_txt = entry.get_text()

    def on_legend_Entry_Changed(self, entry):
            self.legend_Entry_txt = entry.get_text()

    def on_Plot_clicked(self, widget, data=None):
        myplotHistF = plotHistF()
        if len(self.store) > 0:
            myplotHistF.simple_Plot(self.store, self.plot_state)
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
            dialog2 = Gtk.Dialog()
            dialog2.add_buttons(Gtk.STOCK_ADD, 42)
            dialog2.add_buttons(Gtk.STOCK_CLOSE, 43)
            dialog2_area = dialog2.get_content_area()
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
            # d_legend_Label.set_xalign(xalign=1)
            d_legend_Entry = Gtk.Entry()
            d_legend_Entry.connect("changed", self.on_legend_Entry_Changed)
            d_typeh_Label = Gtk.Label("Type Hist : ")
            # d_market_Label.set_xalign(xalign=1)
            d_typeh_Store = Gtk.ListStore(str)
            typehs = ["bar", "barstacked", "step", "stepfilled"]
            for typeh in typehs:
                    d_typeh_Store.append([typeh])
            d_typeh_ComboBox = Gtk.ComboBox.new_with_model(d_typeh_Store)
            d_typeh_ComboBox.connect("changed",
                                     self.on_typeh_ComboBox_Changed)
            renderer_texth = Gtk.CellRendererText()
            d_typeh_ComboBox.pack_start(renderer_texth, True)
            d_typeh_ComboBox.add_attribute(renderer_texth, "text", 0)
            d_func_Label = Gtk.Label("Func Plot : ")
            d_func_Store = Gtk.ListStore(str)
            funcs = ["True", "False"]
            for func in funcs:
                    d_func_Store.append([func])
            d_func_ComboBox = Gtk.ComboBox.new_with_model(d_func_Store)
            d_func_ComboBox.connect("changed", self.on_func_ComboBox_Changed)
            renderer_textf = Gtk.CellRendererText()
            d_func_ComboBox.pack_start(renderer_textf, True)
            d_func_ComboBox.add_attribute(renderer_textf, "text", 0)
            d_n_point_entry = Gtk.Entry()
            d_n_point_entry.connect("changed", self.on_n_point_Entry_Changed)
            d_n_point_label = Gtk.Label("N Point : ")
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
            d_grid.attach(d_typeh_Label, 0, 5, 1, 1)
            d_grid.attach(d_typeh_ComboBox, 1, 5, 1, 1)
            d_grid.attach(d_func_Label, 0, 6, 1, 1)
            d_grid.attach(d_func_ComboBox, 1, 6, 1, 1)
            d_grid.attach(d_n_point_label, 0, 7, 1, 1)
            d_grid.attach(d_n_point_entry, 1, 7, 1, 1)
            d_grid.show_all()
            dialog2_area.pack_start(d_grid, True, True, 0)
            response2 = dialog2.run()
            if response2 == 42:
                dialog_update = Gtk.MessageDialog(None, 0,
                                                  Gtk.MessageType.QUESTION,
                                                  Gtk.ButtonsType.CLOSE,
                                                  "Data For Plot Updated With New Value!")
                response_update = dialog_update.run()
                if response_update == Gtk.ResponseType.CLOSE:
                            dialog_update.destroy()
            elif response2 == 43:
                self.input_File = " "
                self.Styles = "-"
                self.legend_Entry_txt = self.input_File
                self.x_Entry_txt = "X"
                self.y_Entry_txt = "Y"
                self.Color = "b"
                self.Market = "*"
                self.plot_log = "False"
                self.n_Points_Plot = "20"
            print(response2)
            dialog2.destroy()

    def remove_cb(self, button):
        # if there is still an entry in the model
        if len(self.store) != 0:
            # get the selection
            (model, iter) = self.selection.get_selected()
            # if there is a selection, print a message in the terminal
            # and remove it from the model
            if iter is not None:
                print("%s has been removed" % (model[iter][0]))
                self.store.remove(iter)
                # otherwise, ask the user to select something to remove
            else:
                print("Select a title to remove")
            # else, if there are no entries in the model, print "Empty list"
            # in the terminal
        else:
            print("Empty list")

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
        if self.input_File == " ":
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
            fileName_list = self.input_File
            legend_list = self.legend_Entry_txt
            x_Axis_list = self.x_Entry_txt
            y_Axis_list = self.y_Entry_txt
            color_list = self.Color
            type_hist = self.Type = "bar"
            plot_log_list = self.plot_log
            n_Points_Plot_list = self.n_Points_Plot
            self.store.append([fileName_list, legend_list,
                              x_Axis_list, y_Axis_list, color_list,
                              type_hist, plot_log_list, n_Points_Plot_list])

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
            dialog_t = Gtk.Dialog()
            dialog_t.add_buttons(Gtk.STOCK_ADD, 42)
            dialog_t_area = dialog_t.get_content_area()
            t_type_g_Label = Gtk.Label("Select Your Type For Plotting default(Together)")
            t_type_Label = Gtk.Label("Market : ")
            # d_market_Label.set_xalign(xalign=1)
            t_type_Store = Gtk.ListStore(str)
            type_d = ["None", "SubPlot-X", "SubPlot-Y", "Seperate"]
            for market in type_d:
                    t_type_Store.append([market])
            t_type_ComboBox = Gtk.ComboBox.new_with_model(t_type_Store)
            t_type_ComboBox.connect("changed",
                                    self.on_type_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            t_type_ComboBox.pack_start(renderer_text, True)
            t_type_ComboBox.add_attribute(renderer_text, "text", 0)
            grid_t = Gtk.Grid()
            grid_t.set_border_width(20)
            grid_t.set_column_spacing(10)
            grid_t.set_row_spacing(10)
            grid_t.attach(t_type_g_Label, 0, 0, 5, 1)
            grid_t.attach(t_type_Label, 0, 1, 1, 1)
            grid_t.attach(t_type_ComboBox, 1, 1, 4, 1)
            grid_t.show_all()
            dialog_t_area.pack_start(grid_t, False, False, 0)
            dialogt_response = dialog_t.run()
            print(dialogt_response)
            if dialogt_response == 42:
                dialog_t.destroy()
            dialog_t.destroy()

    def on_type_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_state = model[tree_iter][0]
            print(self.plot_state)

    def on_n_point_Entry_Changed(self, entry):
            self.n_Points_Plot = entry.get_text()
            print(self.n_Points_Plot)

    def on_func_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_log = model[tree_iter][0]
            print(self.plot_log)

    def on_Save_Plot_Clicked(self, button):
        myplotHistF = plotHistF()
        if len(self.store) > 0:
            myplotHistF.simple_Save(self.store, self.plot_state)
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Add One Or More Row To Plot")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                            dialog.destroy()
