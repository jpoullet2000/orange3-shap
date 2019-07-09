import numpy
import pandas as pd
import shap
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from Orange.base import Model
from Orange.data import Table
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.utils.webview import WebviewWidget
from AnyQt.QtWidgets import QScrollArea

from sklearn.ensemble.forest import RandomForestRegressor as SKL_RF
from Orange.regression.random_forest import RandomForestRegressor

#class ShapSummaryGraph(WebviewWidget):
class Painter:
    DEFAULT_DPI = 100 
    def __init__(self, parent, box):
        #super().__init__(parent)
        self.parent = parent
        ADJUST_VERTICAL = 0.5
        ADJUST_HORIZONTAL = 0.5
        #WIDTH = n_cols * 3 + 2 * ADJUST_HORIZONTAL
        #HEIGHT = n_rows * 3 + 2 * ADJUST_VERTICAL
        WIDTH = 60
        HEIGHT = 80
        plt.close("all")
        figure = plt.figure(figsize=(WIDTH,HEIGHT), dpi=Painter.DEFAULT_DPI)
        figure.set_visible(False)
        plt.draw()

        canvas = FigureCanvasQTAgg(figure)
        cs = canvas.sizeHint()
        canvas.resize(cs.width(), cs.height())
        box.setWidget(canvas)

        self.figure = figure
        self.canvas = canvas


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
        matplotlib.rcParams["figure.dpi"]=Painter.DEFAULT_DPI
        plt.tight_layout()
        self.max_nr_features = 20

        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '')
        gui.widgetLabel(box, 'Maximum number of features')
        gui.spin(box, self, 'max_nr_features', 1, 20)
        self.button = gui.button(box, self, 'Regenerate plots', callback=self._on_click_button)
        #box = gui.vBox(self.mainArea, True, margin=0.1)
        #self.graph = ShapSummaryGraph(self, box)
        box = gui.widgetBox(self.mainArea, 'Shap Summary Plot')
        scroll = QScrollArea(box)
        box.layout().addWidget(scroll)   
        #self.painter = None
        # box.layout().addWidget(self.graph)

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            sample = dataset
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
        self._update()
    
    def _on_click_button(self):
        self._update()

    def _update(self):
        X = self.dataset.X
        model = self.model
        features = [feature.name for feature in self.dataset.domain.attributes]
        shap_values = shap.TreeExplainer(model.skl_model).shap_values(X)
        shap_df = pd.DataFrame(shap_values, columns=features)
        shap_importances = shap_df.abs().mean()
        shap_importances = shap_importances / shap_importances.sum()
        shap_importances = shap_importances.sort_values(ascending=False)
        shap_importance_features = list(shap_importances[:self.max_nr_features].index)
        #print(shap_importance_features)
        shap.summary_plot(shap_values, X, feature_names=features, max_display=int(self.max_nr_features))
        idx =  [i in shap_importance_features for i in features].index(True)
        sample = self.dataset[idx]
        #self.Outputs.sample.send(sample)


if __name__ == "__main__":  # pragma: no cover
    data = Table('housing')
    rf = SKL_RF(n_estimators=10)
    rf.fit(data.X, data.Y)
    model_rf = RandomForestRegressor(rf)
    WidgetPreview(OWShapSummary).run(set_data=data, set_model=model_rf)