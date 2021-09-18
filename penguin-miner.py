#!/usr/bin/env python3

import pyautogui as auto
import numpy as np
import random as rd
import time
import threading
# import Xlib.threaded  # to fix pyautogui runtime errors


class PenguinMiner:
    def __init__(self, name="Penguin", lock=threading.Lock()):
        self.name = name
        self.lock = lock

        self.topL = (292, 140)  # Enter your static coordinates here
        self.botR = (1617, 979)
        self.pos = tuple()
        self.ROI = {}

        self.mouseSpeed = 100.0
        self.pengSpeed = 15.0
        self.mineTime = 10  # in seconds
        self.mineTimeVar = 3  # in seconds
        self.minSpacing = 8

    def computeVariables(self):
        width = self.botR[0] - self.topL[0]
        self.mouseSpeed *= width / 130
        self.pengSpeed *= width / 130
        self.minSpacing *= width / 130

        # ROI is the region of interest, whose coordinates can be calculated from the ones of the game window
        self.ROI["left"] = int(self.topL[0] + width * 0.46)
        self.ROI["top"] = int(self.topL[1] + width * 0.37)
        self.ROI["right"] = int(self.ROI["left"] + width * 0.3)
        self.ROI["bottom"] = int(self.ROI["top"] + width * 0.19)
        self.pos = (self.ROI["left"], self.ROI["top"])
        print(
            f"Game window coordinates: top left={self.topL} ; bottom right={self.botR}")
        print(f"Mining in ROI with dimensions:\n{self.ROI}")

    def getBoundingBoxCorner(self, corner):
        key = ""
        while key != 'c' or key != 'q':
            key = input(
                f"{self.name}: Position your mouse at the {corner} corner of the game window and enter \'C\'.\nEnter \'Q\' to use the default values.\n>>> ").lower()
            if key == 'c':
                return auto.position()
            elif key == 'q':
                return None

    def setBoundingBox(self):
        topL = self.getBoundingBoxCorner("top left")
        if topL != None:
            botR = self.getBoundingBoxCorner("bottom right")
            if botR != None:
                self.topL = topL
                self.botR = botR
        self.computeVariables()

    def initPos(self):
        auto.moveTo(self.ROI["left"], self.ROI["top"])

    def cursorInROI(self):
        pos = auto.position()
        return pos[0] > self.ROI["left"] and pos[0] < self.ROI["right"] and pos[1] > self.ROI["top"] and pos[1] < self.ROI["bottom"]

    def mine(self, newPos, sleep=0.2):
        print(f"{self.name} moving to {newPos}")
        distance = np.linalg.norm(np.subtract(self.pos, newPos))
        with self.lock:
            self.pos = newPos
            mineTimeRand = self.mineTime + \
                rd.randrange(-self.mineTimeVar * 10,
                             self.mineTimeVar * 10)/10.0

            auto.moveTo(x=newPos[0], y=newPos[1], duration=(
                0.4 + rd.random())*distance / self.mouseSpeed, tween=auto.easeOutQuad)
            auto.click()
            time.sleep(sleep + distance / self.pengSpeed)
            auto.typewrite('d')
            print(f"{self.name} mining for {mineTimeRand} seconds")

        time.sleep(mineTimeRand)

    def changePos(self):
        spaced = False
        while not spaced:
            newPos = (
                rd.randrange(int(self.ROI["left"]), int(self.ROI["right"])),
                rd.randrange(int(self.ROI["top"]), int(self.ROI["bottom"]))
            )
            spaced = np.linalg.norm(np.subtract(
                self.pos, newPos)) > self.minSpacing
            if not spaced:
                print("New position is too close, trying again")

        self.mine(newPos)

    def run(self):
        c = 0
        while(True):
            try:
                self.changePos()
                c += 1
                print(f"{self.name} mined {c} times")
            except (auto.FailSafeException, KeyboardInterrupt):
                print("Exiting...")
                break


if __name__ == '__main__':
    print("By github.com/HamletDuFromage. This code is licensed under the GPLv3.")
    print("\n \n   ___                     _        __  ____              \n  / _ \___ ___  ___ ___ __(_)__    /  |/  (_)__  ___ ____ \n / ___/ -_) _ \/ _ `/ // / / _ \  / /|_/ / / _ \/ -_) __/ \n/_/   \__/_//_/\_, /\_,_/_/_//_/ /_/  /_/_/_//_/\__/_/    \n              /___/                                       \n \n")

    miners = list()
    threads = list()
    lock = threading.Lock()

    key = ""
    while not(key.isnumeric()) and key != 'q':
        key = input(
            f"Enter the number of miners.\nEnter \'Q\' to use the default value (1).\n>>> ").lower()

    n = int(key) if key != 'q' else 1
    for i in range(n):
        miner = PenguinMiner(f"Penguin_{i + 1}", lock)
        miner.setBoundingBox()
        miners.append(miner)

    for miner in miners:
        x = threading.Thread(target=miner.run)
        threads.append(x)
        time.sleep(3)
        x.start()

    for thread in threads:
        thread.join()
