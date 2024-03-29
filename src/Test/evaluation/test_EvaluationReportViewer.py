"""simple test for the report viewer"""
import uuid

from src.DataObjects.Record import Label
from src.Evaluation.EvaluationReportModel import EvaluationReportModel
from src.Evaluation.EvaluationReportViewer import EvaluationReportViewer
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig

e = EvaluationReportViewer()
eva = EvaluationReportModel(EvaluationSystemConfig())
a = [""] * 50
b = [""] * 50
for x in range(0, 50):
    uid = str(uuid.uuid4())
    a[x] = Label(label="moderate", uuid=uid)
for x in range(0, 50):
    b[x] = Label(label="high", uuid=a[x].uuid)
eva.labels = [a, b]
tick = ["X"] * 50
e.save_evaluation_result(eva, tick)
