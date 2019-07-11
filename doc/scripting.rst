Scripting
=========

Load libraries.

>>> from orangecontrib.oshap.widgets.OWShapSingle import OWShapSingle
>>> from orangecontrib.oshap.widgets.OWShapSummary import OWShapSummary
>>> from sklearn.ensemble.forest import RandomForestRegressor as SKL_RF
>>> from Orange.regression.random_forest import RandomForestRegressor
>>> from Orange.widgets.utils.widgetpreview import WidgetPreview
>>> from Orange.data import Table

Load data and model.

>>> data = Table('housing')
>>> rf = SKL_RF(n_estimators=10)
>>> rf.fit(data.X, data.Y)
>>> model_rf = RandomForestRegressor(rf)

Explain single prediction.

>>> WidgetPreview(OWShapSingle).run(set_data=data, set_model=model_rf)


Explain general prediction.

>>> WidgetPreview(OWShapSummary).run(set_data=data, set_model=model_rf)
