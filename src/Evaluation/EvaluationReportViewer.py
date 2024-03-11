from PIL import Image, ImageDraw, ImageFont


class EvaluationReportViewer:


    def print(self,labels,security_labels):
        print("Printing .png evaluation report.")

        width = 512
        height = 512
        message = "Hello boss!"
        font = ImageFont.truetype("arial.ttf", size=20)

        img = Image.new('RGB', (width, height), color='blue')

        imgDraw = ImageDraw.Draw(img)

        imgDraw.text((10, 10), message, font=font, fill=(255, 255, 0))

        img.save('result.png')
        pass

#e = EvaluationReportViewer()
#e.print()