import numpy
import pandas as pd
from shap import TreeExplainer, summary_plot
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


class OWShapSummary(OWWidget):
    name = "Shap summary plot"
    description = "Plot shap summary"
    icon = "icons/shap_summary.png"
    priority = 10

    class Inputs:
        data = Input('Data', Table)
        model = Input('Model', Model)

    class Outputs:
        sample = Output('Top Features', AttributeList)

    want_main_area = False

    def __init__(self):
        plt.tight_layout()
        self.max_nr_features = 20
        self.dataset = None
        self.model = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        gui.widgetLabel(box, 'Maximum number of features')
        gui.spin(box, self, 'max_nr_features', 1, 20)
        self.button = gui.button(box, self, 'Regenerate plots', callback=self._on_click_button)

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            sample = dataset
            self.Outputs.sample.send(sample)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            return
        
        self.dataset =  dataset

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
        if self.dataset is None or self.model is None:
            self.infoa.setText('No input data...')
            return

        plt.close('all')
        self.__update()

    def __update(self):
        X = self.dataset.X
        model = self.model
        features = [feature.name for feature in self.dataset.domain.attributes]
        shap_values = TreeExplainer(model.skl_model).shap_values(X)
        if isinstance(self.model.skl_model, SKL_RF):
            shap_df = pd.DataFrame(shap_values, columns=features)
            shap_importances = shap_df.abs().mean()
            shap_importances = shap_importances / shap_importances.sum()
            shap_importances = shap_importances.sort_values(ascending=False)
            shap_importance_features = list(shap_importances[:self.max_nr_features].index)
            attribute_list = [attr for attr in self.dataset.domain.attributes if attr.name in shap_importance_features]
            self.Outputs.sample.send(attribute_list)
        summary_plot(shap_values, X, feature_names=features, max_display=int(self.max_nr_features))


if __name__ == "__main__":  # pragma: no cover
    data = Table('housing')
    rf = SKL_RF(n_estimators=10)
    rf.fit(data.X, data.Y)
    model_rf = RandomForestRegressor(rf)
    WidgetPreview(OWShapSummary).run(set_data=data, set_model=model_rf)
