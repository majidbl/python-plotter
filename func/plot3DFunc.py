# Thu 02 Aug 2018 01:22:32 PM +0430
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy as np
import os
import gi
from numpy import array
from matplotlib import cm
import math
from .fileExtract import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class plot3DF():

    def __init__(self):
        self.File_Save_Name = "test"
        self.spin_button_digits = 1000
        self.Format_Save = "eps"
        self.Paths = "/home/majid"

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

    def plotting3D(self, inputList, stateP, legloc):
        if stateP == "SubPlot":
            fig = plt.figure(figsize=plt.figaspect(0.5))
            column = dict([(1, 1), (2, 2), (3, 2), (4, 2), (5, 3), (6, 3),
                           (7, 3), (8, 3), (9, 3), (10, 4), (11, 4),
                           (12, 4)])
            row = dict([(1, 1), (2, 1), (3, 2), (4, 2), (5, 2), (6, 2),
                        (7, 2), (8, 2), (9, 3), (10, 3), (11, 3), (12, 3)])
        for i in range(len(inputList)):
            fex = dataExtract()
            fex.getData3d(inputList[i][0], inputList[i][9], inputList[i][8])
            X = fex.x
            Y = fex.y
            Z = fex.z
            if stateP == "Seperate":
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                if inputList[i][8] == "Line":
                    ax.plot(X, Y, Z, marker=inputList[i][7],
                            linestyle=inputList[i][1],
                            color=inputList[i][6], label=inputList[i][2])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Scatter":
                    ax.scatter(X, Y, Z, marker=inputList[i][7],
                               linestyle=inputList[i][1],
                               color=inputList[i][6], label=inputList[i][2])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Surface":
                    ax.plot_surface(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Simple Contour":
                    ax.contour(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Fill Contour":
                    ax.contourf(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

                if inputList[i][8] == "Contour3D":
                    ax.contourf3D(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

                if inputList[i][8] == "WireFrame":
                    ax.plot_surface(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

            if stateP == "SubPlot":
                ax = fig.add_subplot(row[len(inputList)],
                                     column[len(inputList)],
                                     i+1, projection='3d')
                ax = fig.gca(projection='3d')
                if inputList[i][8] == "Line":
                    ax.plot(X, Y, Z, marker=inputList[i][7],
                            linestyle=inputList[i][1],
                            color=inputList[i][6], label=inputList[i][2])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Scatter":
                    ax.scatter(X, Y, Z, marker=inputList[i][7],
                               linestyle=inputList[i][1],
                               color=inputList[i][6], label=inputList[i][2])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Surface":
                    ax.plot_surface(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Simple Contour":
                    ax.contour(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputList[i][8] == "Fill Contour":
                    ax.contourf(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

                if inputList[i][8] == "Contour3D":
                    ax.contourf3D(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

                if inputList[i][8] == "WireFrame":
                    ax.plot_surface(X, Y, Z, cmap=inputList[i][6])
                    ax.set(xlabel=inputList[i][3], ylabel=inputList[i][4],
                           zlabel=inputList[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
        plt.show()

    def plot_Save(self, inputList, stateP, leg):
        winSave = Gtk.Window()
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
        save_ok_button = Gtk.Button("OK")
        save_ok_button.connect("clicked", self.on_save_ok_clicked, inputList,
                               stateP, winSave, leg)
        save_cancel_button = Gtk.Button("Cancel")
        save_cancel_button.connect("clicked", self.on_save_cancel_clicked,
                                   winSave)

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
        d_grid.attach(save_ok_button, 0, 4, 1, 1)
        d_grid.attach(save_cancel_button, 1, 4, 1, 1)
        d_grid.show_all()
        winSave.add(d_grid)
        winSave.show()

    def on_save_ok_clicked(self, button, inputL, stateP, windowS, legloc):
        windowS.destroy()
        if stateP == "SubPlot":
            fig = plt.figure(figsize=plt.figaspect(0.5))
            column = dict([(1, 1), (2, 2), (3, 2), (4, 2), (5, 3), (6, 3),
                           (7, 3), (8, 3), (9, 3), (10, 4), (11, 4),
                           (12, 4)])
            row = dict([(1, 1), (2, 1), (3, 2), (4, 2), (5, 2), (6, 2),
                       (7, 2), (8, 2), (9, 3), (10, 3), (11, 3), (12, 3)])
        for i in range(len(inputL)):
            fex3d = dataExtract()
            fex3d.getData3d(inputL[i][0], inputL[i][9], inputL[i][8])
            X = fex3d.x
            Y = fex3d.y
            Z = fex3d.z
            if stateP == "Seperate":
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                if inputL[i][8] == "Line":
                    ax.plot(X, Y, Z, marker=inputL[i][7],
                            linestyle=inputL[i][1],
                            color=inputL[i][6],
                            label=inputL[i][2])
                    ax.set(xlabel=inputL[i][3],
                           ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Scatter":
                    ax.scatter(X, Y, Z, marker=inputL[i][7],
                               linestyle=inputL[i][1],
                               color=inputL[i][6],
                               label=inputL[i][2])
                    ax.set(xlabel=inputL[i][3],
                           ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Surface":
                    ax.plot_surface(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Simple Contour":
                    ax.contour(x, y, z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Fill Contour":
                    ax.contourf(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Contour3D":
                    ax.contourf3D(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "WireFrame":
                    ax.plot_surface(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                pathSave3D = self.Paths + "/" + self.File_Save_Name + "_" + str(i + 1) + "." + self.Format_Save
                fig.savefig(pathSave3D, format=self.Format_Save,
                            dpi=self.spin_button_digits)
            if stateP == "SubPlot":
                ax = fig.add_subplot(row[len(inputL)],
                                     column[len(inputL)],
                                     i+1, projection='3d')
                if inputL[i][8] == "Line":
                    ax.plot(X, Y, Z, marker=inputL[i][7],
                            linestyle=inputL[i][1],
                            color=inputL[i][6],
                            label=inputL[i][2])
                    ax.set(xlabel=inputL[i][3],
                           ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Scatter":
                    ax.scatter(X, Y, Z, marker=inputL[i][7],
                               linestyle=inputL[i][1],
                               color=inputL[i][6],
                               label=inputL[i][2])
                    ax.set(xlabel=inputL[i][3],
                           ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Surface":
                    ax.plot_surface(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Simple Contour":
                    ax.contour(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "Fill Contour":
                    ax.contourf(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)

                if inputL[i][8] == "Contour3D":
                    ax.contourf3D(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
                if inputL[i][8] == "WireFrame":
                    ax.plot_surface(X, Y, Z, cmap=inputL[i][6])
                    ax.set(xlabel=inputL[i][3], ylabel=inputL[i][4],
                           zlabel=inputL[i][5])
                    plt.gca().invert_yaxis()
                    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
                    # ax.legend([fake2Dline], [inputList[i][2]], numpoints=1)
                    ax.label_outer()
                    ax.legend(loc=legloc)
            if stateP == "SubPlot":
                pathSave3DS = self.Paths + "/" + self.File_Save_Name + "." + self.Format_Save
                plt.savefig(pathSave3DS, format=self.Format_Save,
                            dpi=self.spin_button_digits)
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.CLOSE,
                                   "Save Fig !")
        response = dialog.run()
        if response == Gtk.ResponseType.CLOSE:
                    dialog.destroy()

    def on_save_cancel_clicked(self, button, window):
        window.destroy()

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", None,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
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