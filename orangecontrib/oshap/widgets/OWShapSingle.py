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
        super().__init__()
        plt.tight_layout()
        self.max_nr_features = 20
        self.sample_index = 0
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        gui.widgetLabel(box, 'Sample index')
        self.sample_box = gui.spin(box, self, 'sample_index', 0, 0)
        self.button = gui.button(box, self, 'Regenerate plots', callback=self._on_click_button)

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
        
        self.dataset =  dataset
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
        X = self.dataset.X
        idx = int(self.sample_index)
        model = self.model
        features = [feature.name for feature in self.dataset.domain.attributes]
        explainer = shap.TreeExplainer(model.skl_model)
        shap_values = explainer.shap_values(X)
        plt.close('all')
        shap.force_plot(explainer.expected_value, shap_values[idx, :], X[idx, :], feature_names=features, matplotlib=True)


if __name__ == "__main__":  # pragma: no cover
    data = Table('housing')
    rf = SKL_RF(n_estimators=10)
    rf.fit(data.X, data.Y)
    model_rf = RandomForestRegressor(rf)
    WidgetPreview(OWShapSingle).run(set_data=data, set_model=model_rf)
