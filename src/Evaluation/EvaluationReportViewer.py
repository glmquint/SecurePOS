import os
import uuid
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from src.DataObjects.Record import Label
from src.Evaluation.EvaluationReportModel import EvaluationReportModel
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig


class EvaluationReportViewer:
    def __init__(self):
        self.width = 842
        self.height = 612
        self.second_column_offset = 275
        self.third_column_offset = 555
        self.format_date = "%Y-%m-%d %H:%M:%S"
        self.format_timestamp = "%Y-%m-%d_%H-%M-%S"
        self.title = "Evaluation report, " + \
            str(datetime.now().strftime(self.format_date))
        self.row_id_x_offset = 5
        self.first_label_x_offset = 45
        self.second_label_x_offset = 145
        self.x0_rect = 250
        self.x1_rect_offset = 20
        self.row_offset = 19
        self.tick_x_offset = 253
        self.black = (0, 0, 0)
        self.green = (34, 139, 34)
        self.red = (255, 0, 0)
        if os.name == 'nt':  # for Windows
            self.font = ImageFont.truetype("arial.ttf", 20)
        else:  # for case sensitive systems
            self.font = ImageFont.truetype("Arial.ttf", 20)

    def y_offset(self, y: int):
        return 10 + 30 * y

    def save_evaluation_result(self, modelcontroller, tick_array):
        print("Printing .png evaluation report.")
        self.title = "Evaluation report, " + \
            str(datetime.now().strftime(self.format_date))
        labels = modelcontroller.labels[0]
        security_labels = modelcontroller.labels[1]
        font = self.font
        img = Image.new('RGB', (self.width, self.height), color='white')
        imgDraw = ImageDraw.Draw(img)
        imgDraw.text((10, 5), self.title, font=font, fill=self.black)
        for x in range(1, modelcontroller.sufficient_label_number + 1):
            # first row
            if x <= self.row_offset:
                imgDraw.text(
                    (self.row_id_x_offset,
                     self.y_offset(x)),
                    str(x) + ")",
                    font=font,
                    fill=self.black)
                imgDraw.text((self.first_label_x_offset, self.y_offset(x)), str(
                    labels[x - 1].label), font=font, fill=self.black)
                imgDraw.text((self.second_label_x_offset, self.y_offset(
                    x)), security_labels[x - 1].label, font=font, fill=self.black)
                imgDraw.rectangle([(self.x0_rect,
                                    self.y_offset(x)),
                                   (self.x0_rect + self.x1_rect_offset,
                                    self.y_offset(x) + self.x1_rect_offset)],
                                  None,
                                  "black")
                if tick_array[x - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                imgDraw.text((self.tick_x_offset, self.y_offset(x)),
                             tick_array[x - 1], font=font, fill=tick_color)
            # second row
            elif self.row_offset < x <= self.row_offset * 2:
                y = x - self.row_offset
                imgDraw.text(
                    (self.row_id_x_offset +
                     self.second_column_offset,
                     self.y_offset(y)),
                    str(x) +
                    ")",
                    font=font,
                    fill=(
                        0,
                        0,
                        0))
                imgDraw.text((self.first_label_x_offset +
                              self.second_column_offset, self.y_offset(y)), labels[x -
                                                                                   1].label, font=font, fill=(0, 0, 0))
                imgDraw.text((self.second_label_x_offset +
                              self.second_column_offset, self.y_offset(y)), security_labels[x -
                                                                                            1].label, font=font, fill=(0, 0, 0))
                imgDraw.rectangle([(self.x0_rect +
                                    self.second_column_offset, self.y_offset(y)), (self.x0_rect +
                                                                                   self.x1_rect_offset +
                                                                                   self.second_column_offset, self.y_offset(y) +
                                                                                   self.x1_rect_offset)], None, "black")
                if tick_array[x - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                imgDraw.text((self.tick_x_offset + self.second_column_offset,
                             self.y_offset(y)), tick_array[x - 1], font=font, fill=tick_color)
            # third row
            elif x <= 50:
                y = x - self.row_offset * 2
                imgDraw.text(
                    (self.row_id_x_offset +
                     self.third_column_offset,
                     self.y_offset(y)),
                    str(x) +
                    ")",
                    font=font,
                    fill=self.black)
                imgDraw.text((self.first_label_x_offset +
                              self.third_column_offset, self.y_offset(y)), labels[x -
                                                                                  1].label, font=font, fill=self.black)
                imgDraw.text([self.second_label_x_offset +
                              self.third_column_offset, self.y_offset(y)], " " +
                             security_labels[x -
                                             1].label, font=font, fill=self.black)
                imgDraw.rectangle([(self.x0_rect +
                                    self.third_column_offset, self.y_offset(y)), (self.x0_rect +
                                                                                  self.x1_rect_offset +
                                                                                  self.third_column_offset, self.y_offset(y) +
                                                                                  self.x1_rect_offset)], None, "black")
                if tick_array[x - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                imgDraw.text((self.tick_x_offset + self.third_column_offset,
                             self.y_offset(y)), tick_array[x - 1], font=font, fill=tick_color)

        report_x = 600
        report_y = 810
        report_first_row = 430
        report_second_row = 470
        report_third_row = 510
        report_forth_row = 550

        if modelcontroller.TotalError < modelcontroller.TotalErrorTollerated:
            color = self.green
        else:
            color = self.red
        imgDraw.text((report_x, report_first_row),
                     "Errors: ", font=font, fill=self.black)
        imgDraw.text((report_y, report_first_row), str(
            modelcontroller.TotalError), font=font, fill=color)

        imgDraw.text(
            (report_x,
             report_second_row),
            "Max Toll. Error: ",
            font=font,
            fill=self.black)
        imgDraw.text((report_y, report_second_row), str(
            modelcontroller.TotalErrorTollerated), font=font, fill=self.black)

        imgDraw.text(
            (report_x,
             report_forth_row),
            "Consecutive Toll.: ",
            font=font,
            fill=(
                0,
                0,
                0))
        imgDraw.text((report_y, report_forth_row), str(
            modelcontroller.ConsecutiveErrorTollerated), font=font, fill=self.black)

        if modelcontroller.ConsecutiveError < modelcontroller.ConsecutiveErrorTollerated:
            color = self.green
        else:
            color = self.red
        imgDraw.text(
            (report_x,
             report_third_row),
            "Max Consec. Error: ",
            font=font,
            fill=self.black)
        imgDraw.text((report_y, report_third_row), str(
            modelcontroller.ConsecutiveError), font=font, fill=color)

        self.widthline = 4
        self.firstcorner = 560
        self.secondcorner = 400
        imgDraw.line([(self.firstcorner,
                       self.secondcorner),
                      (self.firstcorner,
                       self.height)],
                     fill=(self.black),
                     width=self.widthline)
        imgDraw.line([(self.firstcorner,
                       self.secondcorner),
                      (self.width,
                       self.secondcorner)],
                     fill=(self.black),
                     width=self.widthline)

        img.save(f'{os.path.dirname(__file__)}/data/result_' +
                 str(datetime.now().strftime(self.format_timestamp)) + '.png')
        pass
