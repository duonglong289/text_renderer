import numpy as np
import random
import cv2
import os 

class Frame:
    def __init__(self, type_frame):
        self.type_frame = type_frame

    def __call__(self, image_text, text, border, gap):
        if self.type_frame == "underline":
            image_text = self._underline(image_text, text, border)
            return image_text

        elif self.type_frame == "separated_box":
            image_text = self._separatedBox(image_text, text, border, gap)
            return image_text

        elif self.type_frame == "connected_box":
            image_text = self._connectedBox(image_text, text, border)
            return image_text

        elif self.type_frame == "one_box":
            image_text = self._oneBox(image_text, text, border)
            return image_text

        elif self.type_frame == "dotline":
            image_text = self._dotline(image_text, text, border)
            return image_text

        elif self.type_frame == "dashedline":
            image_text = self._dashedline(image_text, text, border)
            return image_text    
        else:
            print("Do not recognize this type of frame")
            return None

    def _underline(self, image_text, text, border):
        thickness = np.random.randint(2, 5) 
        h,w = image_text.shape[:2]
        pt1 = (0, h-border + np.random.randint(-3,3))
        pt2 = (w, h-border + np.random.randint(-3,3))
        cv2.line(image_text, pt1, pt2, (0,0,0), thickness)
        return image_text
        

    def _dotline(self, image_text, text, border):
        gap = np.random.randint(10, 30)
        thickness = np.random.randint(2,3)
 
        h,w = image_text.shape[:2]
        pt1 = (0, h-border + np.random.randint(-10, 10))
        pt2 = (w, h-border + np.random.randint(-10, 10))
        
        dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
        pts= []
        for i in  np.arange(0,dist,gap):
            r=i/dist
            x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
            y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
            p = (x,y)
            pts.append(p)
               
        for p in pts:
            cv2.circle(image_text,p,thickness,(0,0,0),thickness)
        return image_text

    def _dashedline(self, image_text, text, border):
        gap = np.random.randint(10, 70)
        thickness = np.random.randint(3,4)
 
        h,w = image_text.shape[:2]
        pt1 = (0, h-border + np.random.randint(-10, 10))
        pt2 = (w, h-border + np.random.randint(-10, 10))
        
        dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
        pts= []
        for i in  np.arange(0,dist,gap):
            r=i/dist
            x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
            y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
            p = (x,y)
            pts.append(p)

        s=pts[0]
        e=pts[0]
        i=0
        for p in pts:
            s=e
            e=p
            if i%2==1:
                cv2.line(image_text, s, e, (0,0,0), thickness)
            i+=1
        return image_text

    def _separatedBox(self, image_text, text, border, gap):
        thickness = np.random.randint(2,4)
        h,w = image_text.shape[:2]

        pt1 = (border, border)
        pt2 = (w-border, border)
        dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
        length_box = int(np.round((dist/len(text)))) - gap
        for i in range(len(text)):
            tl = (i*(length_box+gap)  + border, border)
            tr = ((i+1)*length_box + i*gap - thickness + border, border)
            br = ((i+1)*length_box + i*gap - thickness + border, h-border)
            bl = (i*(length_box+gap) + border, h-border)
            cv2.line(image_text, tl, tr, (0,0,0), thickness)
            cv2.line(image_text, tr, br, (0,0,0), thickness)
            cv2.line(image_text, br, bl, (0,0,0), thickness)
            cv2.line(image_text, bl, tl, (0,0,0), thickness)

        return image_text

    def _connectedBox(self, image_text, text, border):
        thickness = np.random.randint(3,5)
        h,w = image_text.shape[:2]
        image_text = self._oneBox(image_text, text, border)
        pt_s = (border, border)
        pt_e = (w-border, border)

        dist =((pt_s[0]-pt_e[0])**2+(pt_s[1]-pt_e[1])**2)**.5
        length_box = int(np.round((dist/len(text))))
        for i in range(len(text)-1):
            point_top = ((i+1)*length_box + thickness//2 + border, border)
            point_bot = ((i+1)*length_box + thickness//2 + border, h-border)
            cv2.line(image_text, point_top, point_bot, (0,0,0), thickness)
        return image_text
        
        

    def _oneBox(self, image_text, text, border):
        thickness = np.random.randint(3,5)
        h,w = image_text.shape[:2]

        pt1 = (border, border)
        pt2 = (w-border-thickness, border)
        pt3 = (w-border-thickness, h-border)
        pt4 = (border, h-border)
        cv2.line(image_text, pt1, pt2, (0,0,0), thickness)
        cv2.line(image_text, pt2, pt3, (0,0,0), thickness)
        cv2.line(image_text, pt3, pt4, (0,0,0), thickness)
        cv2.line(image_text, pt4, pt1, (0,0,0), thickness)
        return image_text