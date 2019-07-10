import unittest

from orangecontrib.oshap.widgets.OWShapSummary import OWShapSummary

from sklearn.ensemble.forest import RandomForestRegressor as SKL_RF
from Orange.regression.random_forest import RandomForestRegressor
from Orange.data import Table
from Orange.widgets.tests.base import WidgetTest


class TestShapSummary(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(OWShapSummary)
        self.iris = Table('iris')

    def test_shap_summary(self):
        data = self.iris.copy()
        widget = self.widget
        model = RandomForestRegressor(SKL_RF(n_estimators=10))
        self.send_signals([(widget.Inputs.data, data), (widget.Inputs.model, model)])
        self.assertEquals(2, 2)