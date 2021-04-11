import gc, sys
import KPU as kpu
from Maix import GPIO, I2S
from fpioa_manager import fm
import sensor, image, lcd, time
from Maix import MIC_ARRAY as mic
from speech_recognizer import isolated_word
#setup
sample_rate   = 16000
record_time   = 4
#fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
#fm.register(18,fm.fpioa.I2S0_SCLK, force=True)
#fm.register(19,fm.fpioa.I2S0_WS, force=True)
#rx = I2S(I2S.DEVICE_0)
#rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
#rx.set_sample_rate(sample_rate)
#sr = isolated_word(dmac=2, i2s=I2S.DEVICE_0, size=10, shift=1)
#sr.set_threshold(0, 0, 10000)

mic.init(i2s_d3=17, i2s_ws=16, i2s_sclk=15)
sensor.reset(freq=15000000)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.run(1)
lcd.init(type=1)
lcd.rotation(2)
sensor.set_hmirror(False)
lcd.clear(lcd.WHITE)
task = kpu.load("/sd/m.kmodel")
labels = ["0", "1"]
anchors = [0.875, 1.09375, 2.59375, 3.375, 4.03125, 5.40625, 3.3125, 4.34375, 1.6875, 2.125]
kpu.init_yolo2(task, 0.5, 0, 5, anchors)

def findmasks():
    objects = kpu.run_yolo2(task, img)
    if objects:
        for obj in objects:
            pos = obj.rect()
            if obj.classid() == 0:
                img.draw_rectangle(pos, color=(255,0,0))
            if obj.classid() == 1:
                img.draw_rectangle(pos, color=(0,255,0))
            return pos

def findke():
    if sr.Done == sr.recognize():
        res = sr.result()

def array():
    imga = mic.get_map()
    b = mic.get_dir(imga)
    a = mic.set_led(b,(0,0,255))
    imgb = imga.resize(80,80)
    imgc = imgb.to_rainbow(1)
    return imgc

while 0:
  print(sr.state())
  if sr.Done == sr.record(0):
    data = sr.get(0)
    print(data)
    break
  if sr.Speak == sr.state():
    print('speak A')
while(True):
    im1 = image.Image()
    img = sensor.snapshot()
    pos1 = findmasks()
    if pos1:
        im2 = img.copy(pos1)
        im1.draw_image(im2,240,80,x_scale=(80/pos1[2]),y_scale=(80/pos1[2]))
    im1.draw_image(img,(0,0),x_scale=1.07,y_scale=1.07)
    im1.draw_image(array(),(240,0))
    lcd.display(im1)
