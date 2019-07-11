import unittest

from orangecontrib.oshap.widgets.OWShapSingle import OWShapSingle

from sklearn.ensemble.forest import RandomForestRegressor as SKL_RF
from Orange.regression.random_forest import RandomForestRegressor
from Orange.data import Table
from Orange.widgets.tests.base import WidgetTest
import matplotlib.pyplot as plt


class TestShapSingle(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(OWShapSingle)
        self.iris = Table('iris')

    def test_shap_summary(self):
        data = self.iris.copy()
        widget = self.widget
        rf = SKL_RF(n_estimators=10)
        model = RandomForestRegressor(rf)
        rf.fit(data.X, data.Y)
        #self.send_signals([(widget.Inputs.data, data), (widget.Inputs.model, model)])