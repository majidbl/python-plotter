import gi
from func.plot3DFunc import plot3DF
import pickle
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class plot3DUtils(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self.input_File = []
        self.Styles = "-"
        self.legend_Entry_txt = " "
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.z_Entry_txt = "Z"
        self.Color = "b"
        self.Market = "None"
        self.Plot_Type = "Line"
        self.plot_state = "Seperate"
        self.plot_func = "Sqrt"
        self.legend3D_loc = "best"
        self.Edit_List = []
        menutoolbar = Gtk.Toolbar()
        self.pack_start(menutoolbar, False, False, 0)
        file_ToolButton = Gtk.ToolButton(Gtk.STOCK_FILE)
        menutoolbar.insert(file_ToolButton, 0)
        file_ToolButton.connect("clicked", self.on_file_clicked)
        file_ToolButton.set_tooltip_text("Select Plot Data File")
        # x_y_ToolButton = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_LEFT)
        # menutoolbar.insert(x_y_ToolButton, 1)
        # x_y_ToolButton.connect("clicked", self.on_x_y_dialog_clicked)
        # x_y_ToolButton.set_tooltip_text("Insert Details")
        add_ToolButton = Gtk.ToolButton(Gtk.STOCK_ADD)
        menutoolbar.insert(add_ToolButton, 1)
        add_ToolButton.connect("clicked", self.add_cb)
        add_ToolButton.set_tooltip_text("Add Data Row To Table")
        about_ToolButton = Gtk.ToolButton(Gtk.STOCK_ABOUT)
        menutoolbar.insert(about_ToolButton, 2)
        about_ToolButton.connect("clicked", self.Edit_cb)
        about_ToolButton.set_tooltip_text("Edit Row!!!")
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
        type_Plot_ToolButton.set_tooltip_text("Type Plot Data!")
        legend_ToolButton = Gtk.ToolButton(Gtk.STOCK_DND_MULTIPLE)
        legend_ToolButton.set_tooltip_text("Legend Loc!")
        menutoolbar.insert(legend_ToolButton, 8)
        legend_ToolButton.connect("clicked", self.on_legend_Plot_clicked)
        save_layout_ToolButton = Gtk.ToolButton(Gtk.STOCK_STRIKETHROUGH)
        save_layout_ToolButton.set_tooltip_text("save Layout!")
        menutoolbar.insert(save_layout_ToolButton, 9)
        save_layout_ToolButton.connect("clicked", self.on_save_Layout_clicked)
        load_layout_ToolButton = Gtk.ToolButton(Gtk.STOCK_REVERT_TO_SAVED)
        load_layout_ToolButton.set_tooltip_text("Load Layout!")
        menutoolbar.insert(load_layout_ToolButton, 10)
        load_layout_ToolButton.connect("clicked",
                                       self.on_load_Layout_clicked)
       
        self.store = Gtk.ListStore(str, str, str, str, str,
                                   str, str, str, str, str)
        view = Gtk.TreeView(model=self.store)
        i = 0
        tilte_List = ['File Name', 'Style', 'Legend',
                      'X Axis', 'Y Axis', 'Z Axis', 'Color', 'Market',
                      'Plot Type', 'Function Type']
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
        self.z_Entry_txt = "Z"
        self.Color = "b"
        self.Market = "None"
        self.Plot_Type = "Line"
        self.plot_state = "Seperate"
        self.plot_func = "Sqrt"
        self.Edit_List = []
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        Gtk.FileChooser.set_select_multiple(dialog, True)
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: ", dialog.get_filenames())
            self.input_File = dialog.get_filenames()
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

        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV files")
        filter_csv.add_mime_type("text/x-csv")
        dialog.add_filter(filter_csv)

        filter_xnp = Gtk.FileFilter()
        filter_xnp.set_name("1D Numpy Array")
        filter_xnp.add_mime_type("text/x-xnp")
        dialog.add_filter(filter_xnp)

        filter_xynp = Gtk.FileFilter()
        filter_xynp.set_name("2D Numpy Array")
        filter_xynp.add_mime_type("text/x-xynp")
        dialog.add_filter(filter_xynp)

        filter_xyznp = Gtk.FileFilter()
        filter_xyznp.set_name("3D Numpy Array")
        filter_xyznp.add_mime_type("text/x-xyznp")
        dialog.add_filter(filter_xyznp)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_color_Map_ComboBox_Changed(self, combo):
            tree_iter = combo.get_active_iter()
            if tree_iter is not None:
                model = combo.get_model()
                self.Color_Map = model[tree_iter][0]
                print(self.Color_Map)

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

    def on_z_Entry_Changed(self, entry):
            self.z_Entry_txt = entry.get_text()

    def on_legend_Entry_Changed(self, entry):
            self.legend_Entry_txt = entry.get_text()

    def on_Plot_clicked(self, widget, data=None):
        myplot3DF = plot3DF()
        if len(self.store) > 0:
            myplot3DF.plotting3D(self.store, self.plot_state,
                                 self.legend3D_loc)
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
            winE3 = Gtk.Window()

            d_file_Label_l = Gtk.Label("File Data")
            d_x_entry = Gtk.Entry()
            d_x_entry.connect("changed", self.on_x_Entry_Changed)
            d_x_label = Gtk.Label("X Axis : ")
            d_y_entry = Gtk.Entry()
            d_y_entry.connect("changed", self.on_y_Entry_Changed)
            d_y_label = Gtk.Label("Y Axis : ")
            d_z_entry = Gtk.Entry()
            d_z_entry.connect("changed", self.on_z_Entry_Changed)
            d_z_label = Gtk.Label("Z Axis : ")

            d_color_Label = Gtk.Label("Color Map: ")
            # d_color_Label.set_xalign(xalign=1)
            d_color_Store = Gtk.ListStore(str)
            colors = ["Green", "Red", "Blue", "Yellow", "Black", "Cyan",
                      "Magenta", "White", "viridis", "plasma", "inferno",
                      "magma",
                      "Greys", "Purples", "Blues", "Greens", "Oranges",
                      "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "RdPu",
                      "BuPu", "GnBu", "PuBu", "YlGnBu", "PuBuGn", "BuGn",
                      "YlGn", "binery", "gist_gray", "bone", "pink", "spring",
                      "summer", "autumn", "winter", "cool", "Wistia", "hot",
                      "afmhot", "gist_heat", "copper", "PiYG", "PRGn", "BrBg",
                      "PuOr", "RdGy", "RdBu", "RdYlBu", "RdYlGn", "Spectral",
                      "coolwarm", "bwr", "seismic", "Pastel1", "Pastel2",
                      "Paired", "Accent", "Dak2", "Set1", "Set2", "Set3",
                      "Set3", "tab10", "tab20", "tab20b", "tab20c", "flag",
                      "prism", "ocean", "gist_earth", "terrain", "gist_stern",
                      "gnuplot", "gnuplot2", "CMRmap", "cubehelix", "brg",
                      "hsv", "gist_rainbow", "rainbow", "jet", "nipy_spectral",
                      "gist_ncar", "viridis_r", "plasma_r", "inferno_r",
                      "magma_r", "Greys_r", "Purples_r", "Blues_r", "Greens_r",
                      "Oranges_r", "Reds_r", "YlOrBr_r", "YlOrRd_r", "OrRd_r",
                      "PuRd_r", "RdPu_r", "BuPu_r", "GnBu_r", "PuBu_r",
                      "YlGnBu_r", "PuBuGn_r", "BuGn_r", "YlGn_r", "binery_r",
                      "gist_gray_r", "bone_r", "pink_r", "spring_r",
                      "summer_r", "autumn_r", "winter_r", "cool_r", "Wistia_r",
                      "hot_r", "afmhot_r", "gist_heat_r", "copper_r", "PiYG_r",
                      "PRGn_", "BrBg_r", "PuOr_r", "RdGy_r", "RdBu_r",
                      "RdYlBu_r", "RdYlGn", "Spectral", "coolwarm_r", "bwr_r",
                      "seismic_r", "Pastel1_r", "Pastel2_r", "Paired_r",
                      "Accent_r", "Dark2_r", "Set1_r", "Set2_r", "Set3_r",
                      "Set3_r", "tab10_r", "tab20_r", "tab20b_r", "tab20c_r",
                      "flag_r", "prism_r", "ocean_r", "gist_earth_r",
                      "terrain_r", "gist_stern_r", "gnuplot_r", "gnuplot2_r",
                      "CMRmap_r", "cubehelix_r", "brg_r",
                      "hsv_r", "gist_rainbow_r", "rainbow_r", "jet_r",
                      "nipy_spectral_r", "gist_ncar_r"]
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
            d_market_Label = Gtk.Label("Market : ")
            # d_market_Label.set_xalign(xalign=1)
            d_market_Store = Gtk.ListStore(str)
            markets = ["None", ".", ",", "o", "*", "+", "s", "H", "h", "P",
                       "p", "x", "1", "2", "3", "4", "<", ">", "^", "V", "D",
                       "d"]
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
            d_type_label = Gtk.Label("Type Plot :")
            d_type_Store = Gtk.ListStore(str)
            typeP = ["None", "Line", "Scatter"]
            for d_type in typeP:
                d_type_Store.append([d_type])
            d_type_ComboBox = Gtk.ComboBox.new_with_model(d_type_Store)
            d_type_ComboBox.connect("changed",
                                    self.on_typeP_ComboBox_Changed)
            renderer_textP = Gtk.CellRendererText()
            d_type_ComboBox.pack_start(renderer_textP, True)
            d_type_ComboBox.add_attribute(renderer_textP, "text", 0)
            d_typeF_label = Gtk.Label("Type Function :")
            d_typeF_Store = Gtk.ListStore(str)
            typePF = ["None", "Sin Cos", "sqrt"]
            for d_typeF in typePF:
                d_typeF_Store.append([d_typeF])
            d_typeF_ComboBox = Gtk.ComboBox.new_with_model(d_typeF_Store)
            d_typeF_ComboBox.connect("changed",
                                     self.on_typePF_ComboBox_Changed)
            renderer_textPF = Gtk.CellRendererText()
            d_typeF_ComboBox.pack_start(renderer_textPF, True)
            d_typeF_ComboBox.add_attribute(renderer_textPF, "text", 0)
            ok_button_Edit = Gtk.Button("OK")
            ok_button_Edit.connect("clicked", self.on_ok_Edit_clicked, winE3)
            cancel_button_Edit = Gtk.Button("Cancel")
            cancel_button_Edit.connect("clicked", self.on_Cancel_Edit_clicked,
                                       winE3)
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
            d_grid.attach(d_z_label, 0, 7, 1, 1)
            d_grid.attach(d_z_entry, 1, 7, 1, 1)
            d_grid.attach(d_z_label, 0, 8, 1, 1)
            d_grid.attach(d_z_entry, 1, 8, 1, 1)
            d_grid.attach(d_type_label, 0, 9, 1, 1)
            d_grid.attach(d_type_ComboBox, 1, 9, 1, 1)
            d_grid.attach(d_typeF_label, 0, 10, 1, 1)
            d_grid.attach(d_typeF_ComboBox, 1, 10, 1, 1)
            d_grid.attach(ok_button_Edit, 0, 11, 1, 1)
            d_grid.attach(cancel_button_Edit, 1, 11, 1, 1)
            d_grid.show_all()
            winE3.add(d_grid)
            winE3.show()

    def on_ok_Edit_clicked(self, button, Window):
        dialog_update = Gtk.MessageDialog(None, 0,
                                          Gtk.MessageType.QUESTION,
                                          Gtk.ButtonsType.CLOSE,
                                          "Data For Plot Updated With New Value!")
        response_update = dialog_update.run()
        if response_update == Gtk.ResponseType.CLOSE:
            dialog_update.destroy()
        Window.destroy()

    def on_Cancel_Edit_clicked(self, button, Window):
        self.input_File = " "
        self.Styles = "-"
        self.legend_Entry_txt = self.input_File
        self.x_Entry_txt = "X"
        self.y_Entry_txt = "Y"
        self.z_Entry_txt = "Z"
        self.Color = "b"
        self.Market = "None"
        self.Plot_Type = "Line"
        self.plot_func = "Sqrt"
        Window.destroy()

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

    def Edit_cb(self, button):
        # if there is still an entry in the model
        if len(self.store) != 0:
            # get the selection
            (model, iter) = self.selection.get_selected()
            # if there is a selection, print a message in the terminal
            # and remove it from the model
            if iter is not None:
                print("%s has been removed" % (model[iter][0]))
                # self.store.remove(iter)
                # otherwise, ask the user to select something to remove
                mylist = []
                for j in model[iter]:
                    mylist.append(j)
                    self.Edit_List.append(j)
                self.store.remove(iter)
                # self.input_File = self.Edit_List[0]
                self.Styles = self.Edit_List[1]
                self.legend_Entry_txt = self.Edit_List[2]
                self.x_Entry_txt = self.Edit_List[3]
                self.y_Entry_txt = self.Edit_List[4]
                self.z_Entry_txt = self.Edit_List[5]
                self.Color = self.Edit_List[6]
                self.Market = self.Edit_List[7]
                self.Plot_Type = self.Edit_List[8]
                self.plot_func = self.Edit_List[9]
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
                    winE3 = Gtk.Window()
                    d_file_Label_l = Gtk.Label("File Data")
                    d_x_entry = Gtk.Entry()
                    d_x_entry.connect("changed", self.on_x_Entry_Changed)
                    d_x_label = Gtk.Label("X Axis : ")
                    d_y_entry = Gtk.Entry()
                    d_y_entry.connect("changed", self.on_y_Entry_Changed)
                    d_y_label = Gtk.Label("Y Axis : ")
                    d_z_entry = Gtk.Entry()
                    d_z_entry.connect("changed", self.on_z_Entry_Changed)
                    d_z_label = Gtk.Label("Z Axis : ")
                    d_color_Label = Gtk.Label("Color Map: ")
                    d_color_Store = Gtk.ListStore(str)
                    colors = ["Green", "Red", "Blue", "Yellow", "Black",
                              "Cyan", "Magenta", "White", "viridis",
                              "plasma", "inferno", "magma", "Greys",
                              "Purples", "Blues", "Greens", "Oranges",
                              "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd",
                              "RdPu", "BuPu", "GnBu", "PuBu", "YlGnBu",
                              "PuBuGn", "BuGn", "YlGn", "binery", "gist_gray",
                              "bone", "pink", "spring", "summer", "autumn",
                              "winter", "cool", "Wistia", "hot", "afmhot",
                              "gist_heat", "copper", "PiYG", "PRGn", "BrBg",
                              "PuOr", "RdGy", "RdBu", "RdYlBu", "RdYlGn",
                              "Spectral", "coolwarm", "bwr", "seismic",
                              "Pastel1", "Pastel2", "Paired", "Accent", "Dak2",
                              "Set1", "Set2", "Set3", "Set3", "tab10", "tab20",
                              "tab20b", "tab20c", "flag", "prism", "ocean",
                              "gist_earth", "terrain", "gist_stern", "gnuplot",
                              "gnuplot2", "CMRmap", "cubehelix", "brg", "hsv",
                              "gist_rainbow", "rainbow", "jet",
                              "nipy_spectral", "gist_ncar", "viridis_r",
                              "plasma_r", "inferno_r", "magma_r", "Greys_r",
                              "Purples_r", "Blues_r", "Greens_r", "Oranges_r",
                              "Reds_r", "YlOrBr_r", "YlOrRd_r", "OrRd_r",
                              "PuRd_r", "RdPu_r", "BuPu_r", "GnBu_r", "PuBu_r",
                              "YlGnBu_r", "PuBuGn_r", "BuGn_r", "YlGn_r", "binery_r",
                              "gist_gray_r", "bone_r", "pink_r", "spring_r",
                              "summer_r", "autumn_r", "winter_r", "cool_r", "Wistia_r",
                              "hot_r", "afmhot_r", "gist_heat_r", "copper_r", "PiYG_r",
                              "PRGn_", "BrBg_r", "PuOr_r", "RdGy_r", "RdBu_r",
                              "RdYlBu_r", "RdYlGn", "Spectral", "coolwarm_r", "bwr_r",
                              "seismic_r", "Pastel1_r", "Pastel2_r", "Paired_r",
                              "Accent_r", "Dark2_r", "Set1_r", "Set2_r", "Set3_r",
                              "Set3_r", "tab10_r", "tab20_r", "tab20b_r", "tab20c_r",
                              "flag_r", "prism_r", "ocean_r", "gist_earth_r",
                              "terrain_r", "gist_stern_r", "gnuplot_r",
                              "gnuplot2_r", "CMRmap_r", "cubehelix_r", "brg_r",
                              "hsv_r", "gist_rainbow_r", "rainbow_r", "jet_r",
                              "nipy_spectral_r", "gist_ncar_r"]
                    for color in colors:
                        d_color_Store.append([color])
                    color_ComboBox = Gtk.ComboBox.new_with_model(d_color_Store)
                    color_ComboBox.connect("changed",
                                           self.on_color_ComboBox_Changed)
                    renderer_text = Gtk.CellRendererText()
                    color_ComboBox.pack_start(renderer_text, True)
                    color_ComboBox.add_attribute(renderer_text, "text", 0)
                    d_legend_Label = Gtk.Label("Legend :")
                    d_legend_Entry = Gtk.Entry()
                    d_legend_Entry.connect("changed",
                                           self.on_legend_Entry_Changed)
                    d_market_Label = Gtk.Label("Market : ")
                    d_market_Store = Gtk.ListStore(str)
                    markets = ["None", ".", ",", "o", "*", "+", "s", "H", "h",
                               "P", "p", "x", "1", "2", "3", "4", "<", ">",
                               "^", "V", "D", "d"]
                    for market in markets:
                        d_market_Store.append([market])
                    d_market_ComboBox = Gtk.ComboBox.new_with_model(d_market_Store)
                    d_market_ComboBox.connect("changed",
                                              self.on_market_ComboBox_Changed)
                    renderer_text = Gtk.CellRendererText()
                    d_market_ComboBox.pack_start(renderer_text, True)
                    d_market_ComboBox.add_attribute(renderer_text, "text", 0)
                    d_style_Label = Gtk.Label("Style : ")
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
                    d_type_label = Gtk.Label("Type Plot :")
                    d_type_Store = Gtk.ListStore(str)
                    typeP = ["None", "Line", "Scatter", "Surface",
                             "Simple Contour", "Fill Contour", "WireFrame",
                             "Contour3D"]
                    for d_type in typeP:
                        d_type_Store.append([d_type])
                    d_type_ComboBox = Gtk.ComboBox.new_with_model(d_type_Store)
                    d_type_ComboBox.connect("changed",
                                            self.on_typeP_ComboBox_Changed)
                    renderer_textP = Gtk.CellRendererText()
                    d_type_ComboBox.pack_start(renderer_textP, True)
                    d_type_ComboBox.add_attribute(renderer_textP, "text", 0)
                    d_typeF_label = Gtk.Label("Type Function :")
                    d_typeF_Store = Gtk.ListStore(str)
                    typePF = ["None", "Sin Cos", "sqrt"]
                    for d_typeF in typePF:
                        d_typeF_Store.append([d_typeF])
                    d_typeF_ComboBox = Gtk.ComboBox.new_with_model(d_typeF_Store)
                    d_typeF_ComboBox.connect("changed",
                                             self.on_typePF_ComboBox_Changed)
                    renderer_textPF = Gtk.CellRendererText()
                    d_typeF_ComboBox.pack_start(renderer_textPF, True)
                    d_typeF_ComboBox.add_attribute(renderer_textPF, "text", 0)
                    ok_button_Edit = Gtk.Button("Apply")
                    ok_button_Edit.connect("clicked",
                                           self.on_EOk_Bottun_Clicked,
                                           winE3)
                    cancel_button_Edit = Gtk.Button("Cancel")
                    cancel_button_Edit.connect("clicked",
                                               self.on_Canceled_Edit_Bottun_Clicked,
                                               winE3)
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
                    d_grid.attach(d_z_label, 0, 7, 1, 1)
                    d_grid.attach(d_z_entry, 1, 7, 1, 1)
                    d_grid.attach(d_z_label, 0, 8, 1, 1)
                    d_grid.attach(d_z_entry, 1, 8, 1, 1)
                    d_grid.attach(d_type_label, 0, 9, 1, 1)
                    d_grid.attach(d_type_ComboBox, 1, 9, 1, 1)
                    d_grid.attach(d_typeF_label, 0, 10, 1, 1)
                    d_grid.attach(d_typeF_ComboBox, 1, 10, 1, 1)
                    d_grid.attach(ok_button_Edit, 0, 11, 1, 1)
                    d_grid.attach(cancel_button_Edit, 1, 11, 1, 1)
                    d_grid.show_all()
                    winE3.add(d_grid)
                    winE3.show()
            else:
                print("Select a title to remove")
                # self.on_dialog_clicked()
                dialog = Gtk.MessageDialog(None, 0,
                                           Gtk.MessageType.QUESTION,
                                           Gtk.ButtonsType.CLOSE,
                                           "File Data For Plot Not Selected!")
                response = dialog.run()
                if response == Gtk.ResponseType.CLOSE:
                    dialog.destroy()
            # else, if there are no entries in the model, print "Empty list"
            # in the terminal
        else:
            print("Empty list")

    def on_EOk_Bottun_Clicked(self, button, window):
        if self.Styles != self.Edit_List[1]:
            self.Edit_List[1] = self.Styles
        if self.legend_Entry_txt != self.Edit_List[2]:
            self.Edit_List[2] = self.legend_Entry_txt
        if self.x_Entry_txt != self.Edit_List[3]:
            self.Edit_List[3] = self.x_Entry_txt
        if self.y_Entry_txt != self.Edit_List[4]:
            self.Edit_List[4] = self.y_Entry_txt
        if self.z_Entry_txt != self.Edit_List[5]:
            self.Edit_List[5] = self.z_Entry_txt
        if self.Color != self.Edit_List[6]:
            self.Edit_List[6] = self.Color
        if self.Market != self.Edit_List[7]:
            self.Edit_List[7] = self.Market
        if self.Plot_Type != self.Edit_List[8]:
            self.Edit_List[8] = self.Plot_Type
        if self.plot_func != self.Edit_List[9]:
            self.Edit_List[9] = self.plot_func
        print(self.Edit_List)
        self.store.append(self.Edit_List)
        self.Edit_List = []
        dialog_update = Gtk.MessageDialog(None, 0,
                                          Gtk.MessageType.QUESTION,
                                          Gtk.ButtonsType.CLOSE,
                                          "Data For Plot Updated With New Value!")
        response_update = dialog_update.run()
        if response_update == Gtk.ResponseType.CLOSE:
            dialog_update.destroy()
        window.destroy()

    def on_Canceled_Edit_Bottun_Clicked(self, button, window):
        # self.Edit_List[0] = self.input_File
        self.Edit_List[1] = self.Styles
        self.Edit_List[2] = self.legend_Entry_txt
        self.Edit_List[3] = self.x_Entry_txt
        self.Edit_List[4] = self.y_Entry_txt
        self.Edit_List[5] = self.z_Entry_txt
        self.Edit_List[6] = self.Color
        self.Edit_List[7] = self.Market
        self.Edit_List[8] = self.Plot_Type
        self.Edit_List[9] = self.plot_func
        self.store.append(self.Edit_List)
        self.Edit_List = []
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
        print(self.input_File)
        print(len(self.input_File))
        if len(self.input_File) == 1:
            print("hi!!!!!")
            # append to the model the title that is in the entry
            fileName_list = self.input_File[0]
            style_list = self.Styles
            legend_list = self.legend_Entry_txt
            x_Axis_list = self.x_Entry_txt
            y_Axis_list = self.y_Entry_txt
            z_Axis_list = self.z_Entry_txt
            color_list = self.Color
            market_list = self.Market
            plot_list = self.Plot_Type
            function_list = self.plot_func
            self.store.append([fileName_list, style_list, legend_list,
                               x_Axis_list, y_Axis_list, z_Axis_list,
                               color_list, market_list, plot_list,
                               function_list])
        if len(self.input_File) > 1:
            for i in self.input_File:
                # append to the model the title that is in the entry
                fileName_list = i
                style_list = self.Styles
                legend_list = self.legend_Entry_txt
                x_Axis_list = self.x_Entry_txt
                y_Axis_list = self.y_Entry_txt
                z_Axis_list = self.z_Entry_txt
                color_list = self.Color
                market_list = self.Market
                plot_list = self.Plot_Type
                function_list = self.plot_func
                self.store.append([fileName_list, style_list, legend_list,
                                  x_Axis_list, y_Axis_list, z_Axis_list,
                                  color_list, market_list, plot_list,
                                  function_list])

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
            winT = Gtk.Window()
            t_type_g_Label = Gtk.Label("Select Your Type For Plotting default(Together)")
            t_type_Label = Gtk.Label("Market : ")
            t_type_Store = Gtk.ListStore(str)
            type_d = ["None", "SubPlot", "Seperate"]
            for market in type_d:
                    t_type_Store.append([market])
            t_type_ComboBox = Gtk.ComboBox.new_with_model(t_type_Store)
            t_type_ComboBox.connect("changed",
                                    self.on_type_ComboBox_Changed)
            renderer_text = Gtk.CellRendererText()
            t_type_ComboBox.pack_start(renderer_text, True)
            t_type_ComboBox.add_attribute(renderer_text, "text", 0)
            ok_btn = Gtk.Button("Apply")
            ok_btn.connect("clicked", self.on_ok_Type_clicked, winT)
            grid_t = Gtk.Grid()
            grid_t.set_border_width(20)
            grid_t.set_column_spacing(10)
            grid_t.set_row_spacing(10)
            grid_t.attach(t_type_g_Label, 0, 0, 5, 1)
            grid_t.attach(t_type_Label, 0, 1, 1, 1)
            grid_t.attach(t_type_ComboBox, 1, 1, 4, 1)
            grid_t.attach(t_type_ComboBox, 1, 2, 4, 1)
            grid_t.attach(ok_btn, self.on_ok_Type_clicked)
            grid_t.show_all()
            winT.add(grid_t)
            winT.show()

    def on_ok_Type_clicked(self, button, window):
        window.destroy()

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
            self.legend3D_loc = model[tree_iter][0]
            print(self.legend3D_loc)

    def on_type_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_state = model[tree_iter][0]
            print(self.plot_state)

    def on_typeP_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.Plot_Type = model[tree_iter][0]
            print(self.Plot_Type)

    def on_typePF_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.plot_func = model[tree_iter][0]
            print(self.plot_func)

    def on_Save_Plot_Clicked(self, button):
        myplot3DF = plot3DF()
        if len(self.store) > 0:
            myplot3DF.plot_Save(self.store, self.plot_state, self.legend3D_loc)
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.CLOSE,
                                       "Add One Or More Row To Plot")
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                            dialog.destroy()

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
