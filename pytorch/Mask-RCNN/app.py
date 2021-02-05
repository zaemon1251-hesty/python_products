from flask import Flask, render_template, request  #, redirect, url_for, abort
# This Python file uses the following encoding: unicode
# PyTorch関連
import numpy as np
import torch
#import torch.nn as nn
#import torch.nn.functional as F
import torchvision
from torchvision import datasets, transforms
torch.set_grad_enabled(False)

# OpenCV、Pillow(PIL)、datetime
#import cv2
from PIL import Image, ImageOps
from datetime import datetime

#os
import os


#plot
import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
plt.rcParams["axes.grid"] = False


model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model = model.eval()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        # アプロードされたファイルをいったん保存する
        f = request.files["file"]
        filepath = "./static/request/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        f.save(filepath)
        # 画像ファイルを読み込む
        image = Image.open(filepath)
        image_tensor = transforms.functional.to_tensor(image)
        if image_tensor.shape[0]>3:
            image_tensor=image_tensor[1:4]

        output = model([image_tensor])[0]

        masks = None
        for score, mask in zip(output['scores'], output['masks']):
            if score > 0.5:
                if masks is None:
                    masks = mask
                else:
                    masks = torch.max(masks, mask)
        
        #mask画像を保存
        mask_array = masks.squeeze(0).cpu().detach().numpy()
        mask_array = mask_array * 256
        mask_img = Image.fromarray(np.uint8(mask_array))
        mask_path= "./static/mask/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        mask_img.save(mask_path)

        return render_template("index.html", filepath=filepath, maskpath=mask_path)

if __name__ == "__main__":
    app.run(debug=True)

        
