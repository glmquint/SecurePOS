import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


class EvaluationReportViewer:
    """
        This class is responsible for visualizing the evaluation report. It initializes the viewer with a configuration,
        generates a .png image of the report, and saves it.

        Attributes:
            width: The width of the image.
            height: The height of the image.
            second_column_offset: The offset for the second column in the image.
            third_column_offset: The offset for the third column in the image.
            format_date: The format for the date in the title.
            format_timestamp: The format for the timestamp in the filename.
            title: The title of the report.
            row_id_x_offset: The x offset for the row id.
            first_label_x_offset: The x offset for the first label.
            second_label_x_offset: The x offset for the second label.
            x0_rect: The x coordinate for the rectangle.
            x1_rect_offset: The offset for the x1 coordinate of the rectangle.
            row_offset: The offset for the row.
            tick_x_offset: The x offset for the tick.
            black: The color black.
            green: The color green.
            red: The color red.
            font: The font used in the image.

        Methods:
            y_offset: Returns the y offset for a given y offset.
            save_evaluation_result: Generates a .png image of the report and saves it.
    """

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

    def y_offset(self, y_off: int):
        """simple class for the offset"""
        return 10 + 30 * y_off

    def save_evaluation_result(self, model_controller, tick_array):
        """function that save .png with the result"""
        print("Printing .png evaluation report.")
        self.title = "Evaluation report, " + \
            str(datetime.now().strftime(self.format_date))
        labels = model_controller.labels[0]
        security_labels = model_controller.labels[1]
        font = self.font
        img = Image.new('RGB', (self.width, self.height), color='white')
        img_draw = ImageDraw.Draw(img)
        img_draw.text((10, 5), self.title, font=font, fill=self.black)
        for x_iterator in range(1, model_controller.sufficient_label_number + 1):
            # first row
            if x_iterator <= self.row_offset:
                img_draw.text(
                    (self.row_id_x_offset,
                     self.y_offset(x_iterator)),
                    str(x_iterator) + ")",
                    font=font,
                    fill=self.black)
                img_draw.text((self.first_label_x_offset, self.y_offset(x_iterator)), str(
                    labels[x_iterator - 1].label), font=font, fill=self.black)
                img_draw.text((self.second_label_x_offset, self.y_offset(
                    x_iterator)), security_labels[x_iterator - 1].label, font=font, fill=self.black)
                img_draw.rectangle([(self.x0_rect,
                                    self.y_offset(x_iterator)),
                                   (self.x0_rect + self.x1_rect_offset,
                                    self.y_offset(x_iterator) + self.x1_rect_offset)],
                                  None,
                                  "black")
                if tick_array[x_iterator - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                img_draw.text((self.tick_x_offset, self.y_offset(x_iterator)),
                             tick_array[x_iterator - 1], font=font, fill=tick_color)
            # second row
            elif self.row_offset < x_iterator <= self.row_offset * 2:
                y_iterator = x_iterator - self.row_offset
                img_draw.text(
                    (self.row_id_x_offset +
                     self.second_column_offset,
                     self.y_offset(y_iterator)),
                    str(x_iterator) +
                    ")",
                    font=font,
                    fill=(
                        0,
                        0,
                        0))
                img_draw.text((self.first_label_x_offset +
                        self.second_column_offset, self.y_offset(y_iterator)),
                              labels[x_iterator -
                                    1].label, font=font, fill=(0, 0, 0))
                img_draw.text((self.second_label_x_offset +
                        self.second_column_offset,
                        self.y_offset(y_iterator)),
                        security_labels[x_iterator -
                            1].label, font=font, fill=(0, 0, 0))
                img_draw.rectangle([(self.x0_rect +
                                    self.second_column_offset,
                                     self.y_offset(y_iterator)), (self.x0_rect +
                                    self.x1_rect_offset +
                                    self.second_column_offset, self.y_offset(y_iterator) +
                                    self.x1_rect_offset)], None, "black")
                if tick_array[x_iterator - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                img_draw.text((self.tick_x_offset + self.second_column_offset,
                        self.y_offset(y_iterator)),
                              tick_array[x_iterator - 1], font=font, fill=tick_color)
            # third row
            elif x_iterator <= 50:
                y_iterator = x_iterator - self.row_offset * 2
                img_draw.text(
                    (self.row_id_x_offset +
                     self.third_column_offset,
                     self.y_offset(y_iterator)),
                    str(x_iterator) +
                    ")",
                    font=font,
                    fill=self.black)
                img_draw.text((self.first_label_x_offset +
                              self.third_column_offset,
                               self.y_offset(y_iterator)), labels[x_iterator -
                                    1].label, font=font, fill=self.black)
                img_draw.text([self.second_label_x_offset +
                              self.third_column_offset, self.y_offset(y_iterator)], " " +
                             security_labels[x_iterator -
                                             1].label, font=font, fill=self.black)
                img_draw.rectangle([(self.x0_rect +
                                    self.third_column_offset,
                                     self.y_offset(y_iterator)), (self.x0_rect +
                                                self.x1_rect_offset +
                                                self.third_column_offset,
                                                                  self.y_offset(y_iterator) +
                                                self.x1_rect_offset)], None, "black")
                if tick_array[x_iterator - 1] == "V":
                    tick_color = self.green
                else:
                    tick_color = self.red
                img_draw.text((self.tick_x_offset + self.third_column_offset,
                        self.y_offset(y_iterator)),
                              tick_array[x_iterator - 1], font=font, fill=tick_color)

        report_x = 600
        report_y = 810
        report_first_row = 430
        report_second_row = 470
        report_third_row = 510
        report_forth_row = 550

        if model_controller.total_error < model_controller.total_error_tollerated:
            color = self.green
        else:
            color = self.red
        img_draw.text((report_x, report_first_row),
                     "Errors: ", font=font, fill=self.black)
        img_draw.text((report_y, report_first_row), str(
            model_controller.total_error), font=font, fill=color)

        img_draw.text(
            (report_x,
             report_second_row),
            "Max Toll. Error: ",
            font=font,
            fill=self.black)
        img_draw.text((report_y, report_second_row), str(
            model_controller.total_error_tollerated), font=font, fill=self.black)

        img_draw.text(
            (report_x,
             report_forth_row),
            "Consecutive Toll.: ",
            font=font,
            fill=(
                0,
                0,
                0))
        img_draw.text((report_y, report_forth_row), str(
            model_controller.consecutive_error_tollerated), font=font, fill=self.black)

        if model_controller.consecutive_error < model_controller.consecutive_error_tollerated:
            color = self.green
        else:
            color = self.red
        img_draw.text(
            (report_x,
             report_third_row),
            "Max Consec. Error: ",
            font=font,
            fill=self.black)
        img_draw.text((report_y, report_third_row), str(
            model_controller.consecutive_error), font=font, fill=color)

        width_line = 4
        first_corner = 560
        second_corner = 400
        img_draw.line([(first_corner,
                       second_corner),
                      (first_corner,
                       self.height)],
                     fill=(self.black),
                     width= width_line)
        img_draw.line([(first_corner,
                       second_corner),
                      (self.width,
                       second_corner)],
                     fill=(self.black),
                     width=width_line)

        img.save(f'{os.path.dirname(__file__)}/data/result_' +
                 str(datetime.now().strftime(self.format_timestamp)) + '.png')
