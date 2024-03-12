from datetime import datetime
from tkinter import font

from PIL import Image, ImageDraw, ImageFont
from pip._vendor.pygments.formatters import img


class EvaluationReportViewer:
    def __init__(self):
        self.width = 724
        self.height = 612
        self.second_column_offset = 240
        self.third_column_offset = 480
        self.format_date = "%Y-%m-%d %H:%M:%S"
        self.title = "Evaluation report, " + str(datetime.now().strftime(self.format_date))
        self.row_id_x_offset = 5
        self.first_label_x_offset = 40
        self.second_label_x_offset = 120
        self.x0_rect = 200
        self.x1_rect_offset = 20
        self.row_offset = 19

    def y_offset(self, y: int):
        return 10 + 30 * y

    def print(self, labels, security_labels):
        print("Printing .png evaluation report.")
        font = ImageFont.truetype("arial.ttf", size=20)
        img = Image.new('RGB', (self.width,self.height), color='white')
        imgDraw = ImageDraw.Draw(img)
        imgDraw.text((10, 5), self.title, font=font, fill=(0, 0, 0))
        # for x in range(0,len(labels)):
        # imgDraw.text((15, 10+30*x), str(x)+") "+labels[0].attackRiskLabel[1], font=font, fill=(255, 255, 0))
        # imgDraw.text((95, 10+30*x), security_labels[0].attackRiskLabel[1], font=font, fill=(255, 255, 0))
        for x in range(1, 51):
            #first row
            if x <= self.row_offset:
                imgDraw.text((self.row_id_x_offset, self.y_offset(x)), str(x) + ")", font=font, fill=(0, 0, 0))
                imgDraw.text((self.first_label_x_offset, self.y_offset(x)), "high", font=font, fill=(0, 0, 0))
                imgDraw.text((self.second_label_x_offset, self.y_offset(x)), "medium", font=font, fill=(0, 0, 0))
                imgDraw.rectangle([(self.x0_rect, self.y_offset(x)), (
                self.x0_rect + self.x1_rect_offset, self.y_offset(x) + self.x1_rect_offset)], None, "black")
            #second row
            elif self.row_offset < x <= self.row_offset *2:
                y = x - self.row_offset
                imgDraw.text((self.row_id_x_offset + self.second_column_offset, self.y_offset(y)), str(x) + ")", font=font, fill=(0, 0, 0))
                imgDraw.text((self.first_label_x_offset + self.second_column_offset, self.y_offset(y)), "medium", font=font, fill=(0, 0, 0))
                imgDraw.text((self.second_label_x_offset + self.second_column_offset, self.y_offset(y)), "medium", font=font, fill=(0, 0, 0))
                imgDraw.rectangle([(self.x0_rect + self.second_column_offset, self.y_offset(y)), (
                self.x0_rect + self.x1_rect_offset + self.second_column_offset, self.y_offset(y) + self.x1_rect_offset)], None, "black")
            #third row
            elif x <= 50:
                y = x - self.row_offset * 2
                imgDraw.text((self.row_id_x_offset + self.third_column_offset, self.y_offset(y)), str(x) + ")", font=font, fill=(0, 0, 0))
                imgDraw.text((self.first_label_x_offset + self.third_column_offset, self.y_offset(y)), " medium", font=font, fill=(0, 0, 0))
                imgDraw.text([self.second_label_x_offset + self.third_column_offset, self.y_offset(y)], " medium", font=font, fill=(0, 0, 0))
                imgDraw.rectangle([(self.x0_rect + self.third_column_offset, self.y_offset(y)), (
                self.x0_rect + self.x1_rect_offset + self.third_column_offset, self.y_offset(y) + self.x1_rect_offset)], None, "black")
            imgDraw.text((500,420),"Max Error: ",font=font,fill=(0,0,0))
            imgDraw.text((550,450),str(50),font=font,fill=(0,0,0))

            imgDraw.text((500,490),"Max Tollerated Error: ",font=font,fill=(0,0,0))
            imgDraw.text((550,520),str(50),font=font,fill=(0,0,0))

        img.save('../data/result.png')
        pass



e = EvaluationReportViewer()
e.print(["ciao"], ["nonno"])
