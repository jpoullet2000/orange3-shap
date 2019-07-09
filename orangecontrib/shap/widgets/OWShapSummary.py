import numpy
import shap
import matplotlib.pyplot as plt

from Orange.base import Model
from Orange.data import Table
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.utils.webview import WebviewWidget


class ShapSummaryGraph(WebviewWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def _update(self):
        X = self.parent.dataset.X
        model = self.parent.model
        features = [feature.name for feature in self.parent.dataset.domain.attributes]

        shap_values = shap.TreeExplainer(model.skl_model).shap_values(X)
        shap.summary_plot(shap_values, X, feature_names=features)

class OWShapSummary(OWWidget):
    name = "Shap summary plot"
    description = "Plot shap summary"
    icon = "icons/Shap.png"
    priority = 10

    class Inputs:
        data = Input('Data', Table)
        model = Input('Model', Model)

    class Outputs:
        sample = Output("Sampled Data", Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '')
        box = gui.vBox(self.mainArea, True, margin=0.1)
        self.graph = ShapSummaryGraph(self)
        box.layout().addWidget(self.graph)

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            indices = numpy.random.permutation(len(dataset))
            indices = indices[:int(numpy.ceil(len(dataset) * 0.1))]
            sample = dataset[indices]
            self.infob.setText('%d sampled instances' % len(sample))
            self.Outputs.sample.send(sample)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
            self.Outputs.sample.send("Sampled Data")
        
        self.dataset =  dataset

    @Inputs.model
    def set_model(self, model):
        if model is not None:
            self.model = model
            """
            from sklearn.ensemble import RandomForestRegressor
            clf = RandomForestRegressor(n_estimators=100)
            clf.fit(self.dataset.X, self.dataset.Y)
            self.clf = clf
            """
        else:
            self.model = None

    def handleNewSignals(self):
        self.graph._update()

#import numpy
#import concurrent.futures
#from AnyQt.QtCore import pyqtSlot
#from AnyQt.QtGui import QPainter
#import pyqtgraph as pg
#
#from Orange.base import Model
#from Orange.data import Table
#from Orange.widgets.utils.concurrent import ThreadExecutor, FutureWatcher
#from Orange.widgets.widget import OWWidget, Input, Output
#from Orange.widgets.utils.widgetpreview import WidgetPreview
#from Orange.widgets import gui
#from AnyQt.QtWidgets import QScrollArea
#
#import shap
#import matplotlib
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
#
#try:
#    from Orange.widgets.utils.webview import WebviewWidget
#except ImportError:
#    # If required interfaces not available, provide some mocks
#    raise ImportError('opyhighcharts requires interface '
#                        'Orange.widgets.utils.webview.WebviewWidget'
#                        'positioned at '
#                        '__opyhighcharts_interfaces.WebviewWidget')
#
##class Painter():
##    """
##    Painter class used to draw cells in a matplotlib figure
##    """
##    DEFAUlT_DPI = 100
##
##    def __init__(self, box):
##        ADJUST_VERTICAL = 0.5
##        ADJUST_HORIZONTAL = 0.5
##        WIDTH = 600 + 2 * ADJUST_HORIZONTAL
##        HEIGHT = 400 + 2 * ADJUST_VERTICAL
##
##        #plt.close("all")
##        figure = plt.figure(figsize=(WIDTH,HEIGHT), dpi=Painter.DEFAUlT_DPI)
##        figure.set_visible(False)
##        #plt.draw()
##        breakpoint()
##        canvas = FigureCanvasQTAgg(figure)
##        cs = canvas.sizeHint()
##        canvas.resize(cs.width(), cs.height())
##        box.setWidget(canvas)
##
##        self.box = box
##        self.figure = figure
##        self.canvas = canvas
##        subplot = figure.add_subplot(1, 1, 1)
##        self.subplot = subplot
##
##    def remove(self):
##        self.box.hide()
##        self.figure.set_visible(False)
##    
##    def reveale(self):
##        self.figure.tight_layout()
##        self.box.show()
##        self.figure.set_visible(True)
##        self.canvas.draw()
#
#class ShapSummaryGraph(WebviewWidget):
#    def __init__(self, parent):
#        super().__init__(parent)
##        self.view_box = self.getViewBox()
##        self.selection = set()
##        self.legend = self._create_legend(((1, 0), (1, 0)))
##        self.getPlotItem().buttonsHidden = True
##        self.setRenderHint(QPainter.Antialiasing, True))
#        self.parent = parent
#        #print(self.__dict__)
#        #self._update()
#
#    def _update(self):
#        print(self.parent.dataset.x)
#
#
#
#class Task:
#    """
#    Task class to perform computations in parallels
#    """
#    def __init__(self):
#        self.future = None
#        self.watcher = None
#
#
#class OWShapSummary(OWWidget):
#    name = "Shap summary plot"
#    description = "Plot shap summary"
#    icon = "icons/Shap.png"
#    priority = 10
#    want_main_area = True
#    resizing_enabled = True
#
#    class Inputs:
#        data = Input("Data", Table)
#        model = Input("Model", Model)
#
#
#    def __init__(self):
#        super().__init__()
#
##        self._executor = ThreadExecutor()
##        self.is_ready = True
##        self.dataset = None
##        self.painter = None
#        #self.graph = None
#        #self.infoa = None
#        self.dataset = None
#        self.model = None
#        #self.setup_gui()
#        # GUI
#        box = gui.widgetBox(self.controlArea, "Info")
#        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
#        box = gui.vBox(self.mainArea, True, margin=0.1)
#        self.graph = ShapSummaryGraph(self)
#        box.layout().addWidget(self.graph)
#
#    def handleNewSignals(self):
#        pass
#        #print(self.dataset.__dict__)
#        #self.graph._update()
#
#    
#    def setup_gui(self):
#        self._add_graph()
#        self._add_controls()
#
#    def _add_controls(self):
#        # GUI
#        box = gui.widgetBox(self.controlArea, "Info")
#        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
#    
#    def _add_graph(self):
#        box = gui.vBox(self.mainArea, True, margin=0.1)
#        self.graph = ShapSummaryGraph(self)
#        box.layout().addWidget(self.graph)
#        # GUI
#        #box = gui.widgetBox(self.controlArea, "Info")
#        #self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
#        #self.infob = gui.widgetLabel(box, '')
#
#        #matplotlib.rcParams["figure.dpi"]=Painter.DEFAUlT_DPI
#        #plt.tight_layout()
#
# #        self.grid_resolution = 5
# #        self.plots_per_line = 3
#
##        box = gui.widgetBox(self.controlArea, "Customization")
##        gui.widgetLabel(box, "Number of plots per line")
##        gui.spin(box, self, "plots_per_line", 3,6)
##        gui.widgetLabel(box, "Number of points per plots")
##        gui.spin(box, self, "grid_resolution", 3, 100)
##        self.button = gui.button(box, self, "Regenerate plots", callback=self._on_click_button, )
##        self.info_label = gui.widgetLabel(box, "No input data...")
##
##        box = gui.widgetBox(self.mainArea, "Shap summary Plot")
##        scroll = QScrollArea(box)
##        box.layout().addWidget(scroll)
##
##        self.scroll = scroll
#
#    def _add_controls(self):
#        pass
#
#    @Inputs.data
#    def set_data(self, dataset):
#        #self.closeContext()
#        if self.dataset is not None:
#            self.dataset = dataset
#            self.infoa.setText('%d instances in input dataset' % len(dataset))
#        else: 
#            self.dataset = None
#            self.infoa.setText('No data on input yet, waiting to get something.')
#        #self.clear()
#        #self.check_data()
#        #self.check_display_options()
##        if self.data is not None:
##            self.group_vars.set_domain(self.data.domain)
##            self.group_view.setEnabled(len(self.group_vars) > 1)
##            self.group_var = self.data.domain.class_var \
##                if self.data.domain.has_discrete_class else None
##
##        self.openContext()
##        self.setup_plot()
#        print(self.dataset)
#        #self.graph._update()
#        #self.commit()
#
#    def setup_plot(self):
#        if self.dataset is None:
#            return
#        ticks = [a.name for a in self.graph_variables]
##        self.graph.getAxis("bottom").set_ticks(ticks)
##        self.plot_groups()
##        self.apply_selection()
#        self.graph.view_box.enableAutoRange()
#        self.graph.view_box.updateAutoRange()
#
#    def commit(self):
#        pass
##    @pyqtSlot(float)
##    def setProgressValue(self, value):
##        self.progressBarSet(value)
##    
##    @pyqtSlot(concurrent.futures.Future)
##    def __update_is_done(self, f):
##        self.turn_app_ready()
##        #self.painter.reveale()
##    
##    def handleNewSignals(self):
##        self.deal_incoming_changes()
##    def _on_click_button(self):
##        self.deal_incoming_changes()
##
##    def deal_incoming_changes(self):
##        if self.is_ready:
##            if self.dataset is None or self.model is None:
##                self.info_label.setText("No input data...")
##                return
##            
##            if self.painter is not None:
##                self.painter.remove()
##                self.painter = None
###
###            N = len(self.dataset.domain.attributes)
###            n_cols = self.plots_per_line
###            n_rows = round_with_atc(N/n_cols) + 1
##            #self.painter = Painter(self.scroll)
###            ADJUST_VERTICAL = 0.5
###            ADJUST_HORIZONTAL = 0.5
###            WIDTH = 600 + 2 * ADJUST_HORIZONTAL
###            HEIGHT = 400 + 2 * ADJUST_VERTICAL
##
##            #figure = plt.figure(figsize=(WIDTH,HEIGHT), dpi=Painter.DEFAUlT_DPI)
##            #figure.set_visible(False)
##
##            self.turn_app_busy()
##            self.task = Task()
##            self.task.future = self._executor.submit(self._update)
##            self.task.watcher = FutureWatcher(self.task.future)
##            self.task.watcher.done.connect(self.__update_is_done)
##
##    def _update(self):
##        X = self.dataset.X
##        model = self.model
##        shap_df = shap.TreeExplainer(model).shap_values(X)
##        features = [feature.name for feature in self.dataset.domain.attributes]
##        #shap_importance_means = shap_df.abs().mean()
##        #shap_importances = (shap_importance_means / shap_importance_means.sum()).sort_values(ascending=False)
##        #shap.summary_plot(shap_df.values, X)
##        ax = self.painter.subplot[0]
##        ax.plot([1, 2, 3], [4, 5, 6])
##
##    def turn_app_busy(self):
##        self.is_ready = False
##        #self.progressBarInit()
##        self.button.setEnabled(False)
##        self.info_label.setText("Data are not rendered yet, please wait...")
##
##    def turn_app_ready(self):
##        self.button.setEnabled(True)
##        self.is_ready = True
##        #self.progressBarFinished()
##        self.info_label.setText("Plots are up to date!")
##
##    def _on_click_button(self):
##        self.deal_incoming_changes()
##
##    @Inputs.data
##    def set_data(self, dataset):
##        if dataset is not None:
##            self.infoa.setText('%d instances in input dataset' % len(dataset))
##            #indices = numpy.random.permutation(len(dataset))
##            #indices = indices[:int(numpy.ceil(len(dataset) * 0.1))]
##            #sample = dataset[indices]
##            #self.infob.setText('%d sampled instances' % len(sample))
##            self.dataset = dataset
##        else:
##            self.infoa.setText('No data on input yet, waiting to get something.')
##            self.infob.setText('')
##    
#    @Inputs.model
#    def set_model(self, model):
#        if model is not None:
#            self.model = model
#            """
#            from sklearn.ensemble import RandomForestRegressor
#            clf = RandomForestRegressor(n_estimators=100)
#            clf.fit(self.dataset.X, self.dataset.Y)
#            self.clf = clf
#            """
#        else:
#            self.model = None
#
#
#if __name__ == "__main__":  # pragma: no cover
#    data = Table("iris")
#    model = Model(domain=data.domain)
#    WidgetPreview(OWShapSummary).run(set_data=data, set_model=model)