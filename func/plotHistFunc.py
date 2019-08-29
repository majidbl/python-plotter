import matplotlib.pyplot as plt
import gi
import os
import numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class plotHistF():

    def __init__(self):
        self.File_Save_Name = "test"
        self.spin_button_digits = 1000
        self.Format_Save = "eps"
        self.Paths = "~"
        self.Type_Save = "Line"

    def f1(self, x):
        return np.sin(x)

    def f2(self, x):
        return np.cos(x)

    def f3(self, x):
        return np.log(x)

    def f4(self, x):
        return np.e(x)

    def on_format_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.Format_Save = model[tree_iter][0]
            print(self.Format_Save)
        # return self.Format_Save

    def on_type_ComboBox_Changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.Type_Save = model[tree_iter][0]
            print(self.Type_Save)
        # return self.Format_Save

    def on_spin_btn_Changed(self, spinbutton):
        self.spin_button_digits = spinbutton.get_value_as_int()
        print(self.spin_button_digits)
        # return spin_button_digits

    def on_d_save_file_name_Entry_Changed(self, entry):
        self.File_Save_Name = entry.get_text()
        print(self.File_Save_Name)
        # return File_Save_Name

    def simple_Plot(self, input_List, stateP):
        if stateP == "SubPlot-X":
            figx, axs = plt.subplots(1, len(input_List), sharex=True,
                                     tight_layout=True)
        if stateP == "SubPlot-Y":
            figy, ays = plt.subplots(len(input_List), 1, sharey=True,
                                     tight_layout=True)
        for i in range(len(input_List)):
            X_L = input_List[i][2]
            Y_L = input_List[i][3]
            N_Bin = int(input_List[i][7])
            legend_list = input_List[i][1].split()
            print(N_Bin)
            X = np.zeros(shape=())
            ext1 = os.path.splitext(input_List[i][0])[-1].lower()
            if ext1 == ".histdata":
                X = np.loadtxt(input_List[i][0])
            if stateP == "Seperate":
                plt.figure()
                plt.hist(X, bins=N_Bin)
                plt.xlabel(X_L)
                plt.ylabel(Y_L)
                plt.legend(legend_list)
            if stateP == "SubPlot-X":
                print(type(X))
                print(X.shape)
                print(X.ndim)
                axs[i].hist(X, bins=N_Bin)
            if stateP == "SubPlot-Y":
                print(type(X))
                ays[i].hist(X, bins=N_Bin)
        plt.show()
    def simple_Save(self, input_List, stateP):
        save_dialog = Gtk.Dialog()
        save_dialog.add_buttons(Gtk.STOCK_SAVE, 42)
        save_dialog.add_buttons(Gtk.STOCK_NO, 43)
        save_dialog_area = save_dialog.get_content_area()
        d_format_Label = Gtk.Label("format Save : ")
        d_format_Store = Gtk.ListStore(str)
        formats = ["None", "eps", "jpeg", "jpg", "pdf", "pgf", "png", "ps",
                   "raw", "rgba", "svg", "svgz", "tif", "tiff"]
        for d_format in formats:
            d_format_Store.append([d_format])
        d_format_ComboBox = Gtk.ComboBox.new_with_model(d_format_Store)
        d_format_ComboBox.connect("changed",
                                  self.on_format_ComboBox_Changed)
        renderer_text = Gtk.CellRendererText()
        d_format_ComboBox.pack_start(renderer_text, True)
        d_format_ComboBox.add_attribute(renderer_text, "text", 0)
        d_spin_btn_Label = Gtk.Label("DPI : ")
        adjustment = Gtk.Adjustment(1000, 0, 10000, 1, 10, 0)
        d_spin_btn = Gtk.SpinButton()
        d_spin_btn.set_adjustment(adjustment)
        d_spin_btn.connect("changed",
                           self.on_spin_btn_Changed)
        d_save_fle_name_Label = Gtk.Label("File Name : ")
        d_save_file_name_Entry = Gtk.Entry()
        d_save_file_name_Entry.connect("changed",
                                       self.on_d_save_file_name_Entry_Changed)
        d_folder_btn_Label = Gtk.Label("Path To Save : ")
        d_folder_btn = Gtk.Button("Select Folder")
        d_folder_btn.connect("clicked", self.on_folder_clicked)
        d_grid = Gtk.Grid()
        d_grid.set_border_width(20)
        d_grid.set_column_spacing(10)
        d_grid.set_row_spacing(10)
        d_grid.attach(d_format_Label, 0, 0, 1, 1)
        d_grid.attach(d_format_ComboBox, 1, 0, 1, 1)
        d_grid.attach(d_spin_btn_Label, 0, 1, 1, 1)
        d_grid.attach(d_spin_btn, 1, 1, 1, 1)
        d_grid.attach(d_save_fle_name_Label, 0, 2, 1, 1)
        d_grid.attach(d_save_file_name_Entry, 1, 2, 1, 1)
        d_grid.attach(d_folder_btn_Label, 0, 3, 1, 1)
        d_grid.attach(d_folder_btn, 1, 3, 1, 1)
        d_grid.attach(d_folder_btn_Label, 0, 3, 1, 1)
        d_grid.attach(d_folder_btn, 1, 3, 1, 1)
        d_grid.show_all()
        save_dialog_area.pack_start(d_grid, True, True, 0)
        save_dialog_response = save_dialog.run()
        print(save_dialog_response)
        if save_dialog_response == 42:
            save_dialog.destroy()
            if stateP == "SubPlot-X":
                figx, axs = plt.subplots(1, len(input_List), sharex=True,
                                         tight_layout=True)
            if stateP == "SubPlot-Y":
                figy, ays = plt.subplots(len(input_List), 1, sharey=True,
                                         tight_layout=True)
            for i in range(len(input_List)):
                X_L = input_List[i][2]
                Y_L = input_List[i][3]
                legend_list = input_List[i][1].split()
                N_Bin = input_List[i][7]
                X = np.zeros(shape=())
                ext1 = os.path.splitext(input_List[i][0])[-1].lower()
                if ext1 == ".txt":
                    X_t = []
                    for line in open(input_List[i][0], 'r'):
                        values = [float(s) for s in line.split()]
                        colv = len(values)
                        for k in range(len(values)):
                            X_t.append(values[k])
                    X = np.zeros(shape=(int(len(X_t)/colv), colv))
                    for i in range(colv):
                        j = i
                        row = 0
                        while j < len(X_t):
                            temp = X_t[j]
                            X[row, i] = temp
                            j = j + colv
                            row = row + 1
                if ext1 == ".xynp":
                    A = np.loadtxt(input_List[i][0])
                    X = A[:, 0]
                if ext1 == ".xnp":
                    A = np.loadtxt(input_List[i][0])
                    X = A[:0]
                if stateP == "Seperate":
                    plt.hist(X, bins=N_Bin)
                    plt.xlabel(X_L)
                    plt.ylabel(Y_L)
                    plt.legend(legend_list)
                    pathSave = self.Paths + "/" + self.File_Save_Name + "_" + str(i + 1)
                    plt.savefig(pathSave, format=self.Format_Save,
                                dpi=self.spin_button_digits)
                if stateP == "SubPlot-X":
                    axs[i].hist(X, bins=int(input_List[i][7]))
                if stateP == "SubPlot-Y":
                    ays[i].hist(X, bins=int(input_List[i][7]))
                if stateP == "SubPlot-X":
                    pathSaveSx = self.Paths + "/" + self.File_Save_Name
                    figx.savefig(pathSaveSx, format=self.Format_Save,
                                 dpi=self.spin_button_digits)
                if stateP == "SubPlot-Y":
                    pathSaveSy = self.Paths + "/" + self.File_Save_Name
                    figy.savefig(pathSaveSy, format=self.Format_Save,
                                 dpi=self.spin_button_digits)
        if save_dialog_response == 43:
            save_dialog.destroy()
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.CLOSE,
                                   "Save Fig !")
        response = dialog.run()
        if response == Gtk.ResponseType.CLOSE:
                    dialog.destroy()

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", None,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.Paths = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()