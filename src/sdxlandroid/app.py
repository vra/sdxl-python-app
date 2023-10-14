"""
An Application based on Python and LeptonAI!
"""
import json
import io
import os
import urllib.request

from PIL import Image as PIL_Image

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class AISDK:
    def __init__(self):
        # Android 端没法用环境变量，这里只能将 TOKEN 写死在代码中
        api_token = "xxxxxxxxxxxx"
        self.url = "https://xxx-sdxl-deploy.bjz.edr.lepton.ai/run"
        self.headers = {
            "Content-Type": "application/json",
            "accept": "image/png",
            "Authorization": f"Bearer {api_token}",
        }

    def process(self, prompt, img_save_path):
        print("ai processing begin...")
        data = {"num_inference_steps": 25, "prompt": prompt, "seed": 42}
        req = urllib.request.Request(self.url, headers=self.headers, data=json.dumps(data).encode('utf-8'))
        response = urllib.request.urlopen(req)
        res = response.read()

        image_data = io.BytesIO(res)
        image = PIL_Image.open(image_data)
        image.save(img_save_path)
        print("ai processing done")


class SDXLApp(toga.App):
    def startup(self):
        self.sdk = AISDK()
        self.img_save_path = os.path.join(os.path.dirname(__file__), "aigc_img.jpg")

        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label("Your prompt: ", style=Pack(padding=(0, 5)))
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Generate Image", on_press=self.run_aigc, style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        print(self.img_save_path)
        self.image = toga.Image(self.img_save_path)
        self.image_view = toga.ImageView(self.image)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.content.add(self.image_view)
        self.main_window.show()

    def run_aigc(self, widget):
        # 清除已有结果
        self.main_window.content.remove(self.image_view)
        self.image_view = toga.ImageView(image=None)

        prompt = self.name_input.value
        self.sdk.process(prompt, self.img_save_path)

        image = toga.Image(self.img_save_path)
        self.image_view = toga.ImageView(image)
        self.main_window.content.add(self.image_view)


def main():
    return SDXLApp()


if __name__ == "__main__":
    SDXLApp()