# Copyright 2024 (C) antillia.com. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

#
# statistics.py

# 2024/02/02 : Toshiyuki Arai antillia.com

import glob
import os
import sys
import traceback
import matplotlib.pyplot as plt
import numpy as np 

def count_image_files(root_dir, title):
  sub_dirs = os.listdir(root_dir)
  dataset = {}
  n = 1
  x = []
  y = []
  labels = []
  for sub_dir in sub_dirs:
    x.append(n)
    n += 1
    labels.append(sub_dir +"/images")
    
    subsub_dirs = os.listdir(root_dir + "/"+ sub_dir)
    
    for subsub_dir in subsub_dirs:
       fullpath = root_dir + "/" +  sub_dir + "/" + subsub_dir
       if subsub_dir == "masks":
          continue
       files = glob.glob(fullpath + "/*.jpg")
       count = len(files)
       y.append(count)

  plot_statistics(x, y, labels, title)


def add_value_label(x_list, y_list):
  for i in range(1, len(x_list) + 1):
    plt.text(i, y_list[i - 1], y_list[i - 1], ha="center")


def plot_statistics(x, y, labels, title):

  fig, ax = plt.subplots()
  ax.bar(x, y, tick_label=labels)
  add_value_label(x, y)

  #ax.legend()
  plt.title(title)
  plt.ylabel("Number of Images")

  #plt.show()
  filename = title.replace("/", "_").replace(".", "") + ".png"
  plt.savefig(filename)


if __name__ == "__main__":
  try:
    root_dir = "./CAMUS_public-ImageMask-Dataset/Cardiac-Acquisition/"
    count_image_files(root_dir, root_dir)

  except:
    traceback.print_exc()
 
