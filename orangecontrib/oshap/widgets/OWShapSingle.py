import numpy
import pandas as pd
import shap
import matplotlib.pyplot as plt
from Orange.base import Model
from Orange.data import Table
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.widget import AttributeList
from Orange.widgets.utils.webview import WebviewWidget
from sklearn.ensemble.forest import RandomForestRegressor as SKL_RF
from Orange.regression.random_forest import RandomForestRegressor
from Orange.widgets.utils.concurrent import ThreadExecutor, FutureWatcher
import concurrent.futures
from AnyQt.QtCore import pyqtSlot

class OWShapSingle(OWWidget):
    name = "Shap single plot"
    description = "Plot shap single prediction explanation"
    icon = "icons/shap_single.png"
    priority = 10

    class Inputs:
        data = Input('Data', Table)
        model = Input('Model', Model)

    want_main_area = False

    def __init__(self):
        plt.tight_layout()
        self.sample_index = 0
        self.dataset = None
        self.model = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        gui.widgetLabel(box, 'Sample index')
        self.sample_box = gui.spin(box, self, 'sample_index', 0, 0)
        self.button = gui.button(box, self, 'Regenerate plots', callback=self._on_click_button)

        self._executor = ThreadExecutor()
        self.is_ready = True


    def turn_app_busy(self):
        self.is_ready = False
        self.progressBarInit()
        self.button.setEnabled(False)
        self.infoa.setText("Data are not rendered yet, please wait...")

    def turn_app_ready(self):
        self.button.setEnabled(True)
        self.is_ready = True
        self.progressBarFinished()
        self.infoa.setText("Plots are up to date!")
    
    @pyqtSlot(float)
    def setProgressValue(self, value):
        self.progressBarSet(value)
    
    @pyqtSlot(concurrent.futures.Future)
    def __update_is_done(self, f):
        self.turn_app_ready()

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            return

        self.dataset = dataset
        self.sample_box.setMaximum(len(dataset.X) - 1)

    @Inputs.model
    def set_model(self, model):
        if model is not None:
            self.model = model
        else:
            self.model = None

    def handleNewSignals(self):
        self._update()
    
    def _on_click_button(self):
        self._update()


    def _update(self):
        if self.is_ready:    
            if self.dataset is None or self.model is None:
                self.infoa.setText('No input data...')
                return

        plt.close('all')
#        self.turn_app_busy()
#        self.task = Task()
#        self.task.future = self._executor.submit(self.__update)
#        self.task.watcher = FutureWatcher(self.task.future)
#        self.task.watcher.done.connect(self.__update_is_done)
        self.__update()

    def __update(self):
        X = self.dataset.X
        idx = int(self.sample_index)
        model = self.model
        if isinstance(self.model.skl_model, SKL_RF):
            features = [feature.name for feature in self.dataset.domain.attributes]
            explainer = shap.TreeExplainer(model.skl_model)
            shap_values = explainer.shap_values(X)
            shap.force_plot(explainer.expected_value, shap_values[idx, :], X[idx, :], feature_names=features, matplotlib=True)
        else:  # model.skl_model should be RandomForestClassifier
            features = [feature.name for feature in self.dataset.domain.attributes]
            explainer = shap.TreeExplainer(model.skl_model)
            shap_values = explainer.shap_values(X)
            for c in range(len(shap_values)):
                shap.force_plot(explainer.expected_value[c], shap_values[c][idx, :], X[idx, :], feature_names=features, matplotlib=True)


class Task:
    """
    Task class to perform computations in parallels
    """
    def __init__(self):
        self.future = None
        self.watcher = None

if __name__ == "__main__":  # pragma: no cover
    data = Table('housing')
    rf = SKL_RF(n_estimators=10)
    rf.fit(data.X, data.Y)
    model_rf = RandomForestRegressor(rf)
    WidgetPreview(OWShapSingle).run(set_data=data, set_model=model_rf)
