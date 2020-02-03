# /*
#  * @Author: Leohearts 
#  * @Date: 2020-02-03 18:33:40 
#  * @Last Modified by:   Leohearts 
#  * @Last Modified time: 2020-02-03 18:33:40 
#  */
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import os
import time
import shutil
import _thread as thread


newpic = True
lock = False
finishedthread = 0
resp = 0
MAX_THREADS = 64        #<=64 is recommended, increases fps and CPU load.
WARMUP_TIME = 10  # generally MAX_THREADS/6, increase it if backtracking appears


def updateimg(tid):
    global newpic, lock, finishedthread, resp
    try:
        resp = os.system("adb shell screencap -p > .usbviewtmp/."+str(tid))
        while lock:
            time.sleep(0.01)
        lock = True
        os.replace(".usbviewtmp/."+str(tid), ".usbviewtmp/tmp.png")
        lock = False
        newpic = True
    except:
        time.sleep(1)
        pass
    finishedthread += 1


def daemon():
    global finishedthread, resp
    while True:
        finishedthread = 0
        #print(finishedthread)
        for i in range(MAX_THREADS):
            thread.start_new_thread(updateimg, (i,))
            time.sleep(WARMUP_TIME/MAX_THREADS)
        while finishedthread < MAX_THREADS:
            time.sleep(0.1)
            #print(finishedthread)


def updatefig(fig):
    global newpic
    plt.clf()
    plt.axis('off')
    succ = 0
    while (succ == 0):
        try:
            while not newpic:
                time.sleep(0.05)
            newpic = False
            lena = mpimg.imread('.usbviewtmp/tmp.png')
            lena.shape
            im = plt.imshow(lena, animated=True)
            succ = 1
        except Exception as e:
            print(e)
            time.sleep(1)
    return im,


if __name__ == "__main__":
    try:
        os.mkdir(".usbviewtmp")
    except:
        pass
    fig = plt.figure()
    os.system("adb shell screencap -p > .usbviewtmp/tmp.png")
    lena = mpimg.imread('.usbviewtmp/tmp.png')
    lena.shape
    im = plt.imshow(lena, animated=True)
    plt.axis('off')
    thread.start_new_thread(daemon, ())
    ani = animation.FuncAnimation(fig, updatefig, interval=50)
    plt.show()
    shutil.rmtree(".usbviewtmp")
