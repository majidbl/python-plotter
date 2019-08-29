import gi
from utils.plot2DUtils import plot2DUtils
from utils.plot3DUtils import plot3DUtils
from utils.plotHistUtils import plotHistUtils
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PlotM(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='PlotM')
        notebook = Gtk.Notebook()
        self.add(notebook)
        self.set_default_size(550, 500)
        plot2dutils_box1 = plot2DUtils()
        label2d = Gtk.Label('  2D  ')
        notebook.append_page(plot2dutils_box1, label2d)
        page2 = plot3DUtils()
        # page2.set_border_width(10)
        label3d = Gtk.Label('  3D  ')
        notebook.append_page(page2, label3d)
        page3 = plotHistUtils()
        # page2.set_border_width(10)
        labelhist = Gtk.Label('  Hist  ')
        notebook.append_page(page3, labelhist)

win = PlotM()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
