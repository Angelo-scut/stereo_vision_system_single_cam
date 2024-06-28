import math
import os

import numpy as np
import cv2

factor = 5
ls = 0.
lwd = 0.
theta_m2 = (90 - 54.19) * math.pi / 180
h_m2 = 35


def mathmatical_model(f, ws, ls, lm, lwd, theta_m1, theta_m2, h_m2, w_m1, theta_w, d_w):
    theta_wfov = 2 * math.atan2(ws, 2 * f)
    xc = (2 * f * ls * math.tan(theta_m1)) / (2 * f * math.tan(theta_m1) - ws)
    yc = (ws * ls * math.tan(theta_m1)) / (2 * f * math.tan(theta_m1) - ws)
    print("(x_c, y_c) = ({:.2f}, {:.2f})".format(xc, yc))
    kcc1 = math.tan(2 * theta_m1 - theta_wfov / 2)
    # kcc1 = math.tan(2 * theta_m1 - math.atan(abs(math.tan(theta_wfov / 2))))
    bcc1 = ((ws * ls * math.tan(theta_m1)) / (2 * f * math.tan(theta_m1) - ws) -
            (2 * f * ls * math.tan(theta_m1) * math.tan(2 * theta_m1 - theta_wfov / 2)) / (2 * f * math.tan(theta_m1) - ws))
    km2m2_1 = math.tan(theta_m2)
    bm2m2_1 = h_m2 - ls * math.tan(theta_m2)
    xc1 = (bm2m2_1 - bcc1) / (kcc1 - km2m2_1)
    yc1 = kcc1 * (bm2m2_1 - bcc1) / (kcc1 - km2m2_1) + bcc1
    print("(x_c1, y_c1) = ({:.2f}, {:.2f})".format(xc1, yc1))

    kc1c2 = -math.tan(math.atan(abs(kcc1)) - 2 * theta_m2)
    bc1c2 = kcc1 * (bm2m2_1 - bcc1) / (kcc1 - km2m2_1) + bcc1 - kc1c2 * (bm2m2_1 - bcc1) / (kcc1 - km2m2_1)
    yc2 = kc1c2 * (ls + lm + lwd) + bc1c2
    print("y_c2 = {:.2f}".format(yc2))

    xa = ls + w_m1 / math.tan(theta_m1)
    ya = w_m1
    print("(x_a, y_a) = ({:.2f}, {:.2f})".format(xa, ya))

    koa = w_m1 * math.tan(theta_m1) / (w_m1 + ls * math.tan(theta_m1))
    kaa1 = math.tan(2 * theta_m1 - math.atan(abs(koa)))
    baa1 = w_m1 - (w_m1 - ls * math.tan(theta_m1)) * math.tan(2 * theta_m1 + math.atan(abs(koa))) / math.tan(theta_m1)

    xa1 = (bm2m2_1 - baa1) / (kaa1 - km2m2_1)
    ya1 = kaa1 * (bm2m2_1 - baa1) / (kaa1 - km2m2_1) + baa1
    print("(x_a1, y_a1) = ({:.2f}, {:.2f})".format(xa1, ya1))

    ka1a2 = -math.tan(math.atan(abs(kaa1)) - 2 * theta_m2)
    ba1a2 = kaa1 * (bm2m2_1 - baa1) / (kaa1 - km2m2_1) + baa1 - ka1a2 * (bm2m2_1 - baa1) / (kaa1 - km2m2_1)

    ya2 = ka1a2 * (ls + lm + lwd) + ba1a2
    print("y_a2 = {:.2f}".format(ya2))

    xa1a2_mm1 = (ls * math.tan(theta_m1) + ba1a2) / (math.tan(theta_m1) - ka1a2)
    print("xa1a2_mm1 = {:.2f}".format(xa1a2_mm1))
    xb1 = ((ls + lm + lwd + d_w) * math.tan(theta_w / 2) - h_m2 + ls * math.tan(theta_m2)) / (math.tan(theta_m2) + math.tan(theta_w / 2))
    yb1 = -math.tan(theta_w / 2) * xb1 + (ls + lm + lwd + d_w) * math.tan(theta_w / 2)
    print("x_b1 = {:.2f}".format(xb1))

    img = np.ones((int(h_m2 + lm * math.tan(theta_m2)), int(ls + lm + lwd + d_w), 3), dtype=np.uint8)
    img = img * 255

    # mirror 1
    cv2.line(img, (int(ls), 0), (int(ls + lm), int(lm * math.tan(theta_m1))), (0, 255, 0), 1)

    # mirror 2
    cv2.line(img, (int(ls), int(h_m2)), (int(ls + lm), int(h_m2 + lm * math.tan(theta_m2))), (0, 255, 0), 1)

    # weldment
    cv2.line(img, (int(ls + lm + lwd + d_w), 0), (int(ls + lm + lwd), int(d_w * math.tan(theta_w / 2))), (0, 0, 255), 1)
    cv2.line(img, (int(ls + lm + lwd), int(d_w * math.tan(theta_w / 2))), (int(ls + lm + lwd), int(d_w * math.tan(theta_w / 2) + 20)), (0, 0, 255), 1)

    # light a
    cv2.line(img, (0, 0), (int(xa), int(ya)), (255, 0, 0), 1)  # oa
    cv2.line(img, (int(xa), int(ya)), (int(xa1), int(ya1)), (255, 0, 0), 1)  # aa1
    cv2.line(img, (int(xa1), int(ya1)), (int(ls + lm + lwd), int(ya2)), (255, 0, 0), 1)  # a1a2

    # light c
    cv2.line(img, (0, 0), (int(xc), int(yc)), (255, 0, 0), 1)  # oc
    cv2.line(img, (int(xc), int(yc)), (int(xc1), int(yc1)), (255, 0, 0), 1)  # cc1
    cv2.line(img, (int(xc1), int(yc1)), (int(ls + lm + lwd), int(yc2)), (255, 0, 0), 1)  # cc2

    # light b
    cv2.line(img, (int(ls + lm + lwd + d_w), 0), (int(xb1), int(yb1)), (255, 0, 0), 1)  # b1b2

    img = cv2.flip(img, 0)
    img = cv2.resize(img, (img.shape[1] * factor, img.shape[0] * factor))
    # return img
    cv2.imshow("Stereo_system", img)


def update_ls(val):
    global ls
    ls = val
    mathmatical_model(25, 6.4, ls, 30, lwd, 45. * math.pi / 180, theta_m2, h_m2, 2,
                      90 * math.pi / 180, 6)


def update_lwd(val):
    global lwd
    lwd = val
    mathmatical_model(25, 6.4, ls, 30, lwd, 45. * math.pi / 180, theta_m2, h_m2, 2,
                      90 * math.pi / 180, 6)


def update_theta_m2(val):
    global theta_m2
    theta_m2 = (90 - val) * math.pi / 180
    mathmatical_model(25, 6.4, ls, 30, lwd, 45. * math.pi / 180, theta_m2, h_m2, 2,
                      90 * math.pi / 180, 6)


def update_h_m2(val):
    global h_m2
    h_m2 = val
    mathmatical_model(25, 6.4, ls, 30, lwd, 45. * math.pi / 180, theta_m2, h_m2, 2,
                      90 * math.pi / 180, 6)


cv2.namedWindow("Stereo_system", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("ls", "Stereo_system", 50, 400, update_ls)
cv2.createTrackbar("lwd", "Stereo_system", 150, 400, update_lwd)
cv2.createTrackbar("theta_m2", "Stereo_system", 54, 90, update_theta_m2)
cv2.createTrackbar("h_m2", "Stereo_system", 35, 200, update_h_m2)
mathmatical_model(25, 6.4, 50, 30, 150, 45. * math.pi / 180,
                        (90 - 54.19) * math.pi / 180, 35, 2, 90 * math.pi / 180, 6)
while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

# if __name__ == '__main__':
    # img = mathmatical_model(25, 6.4, 50, 30, 150, 45. * math.pi / 180, (90 - 54.19) * math.pi / 180, 35, 2, 90 * math.pi / 180, 6)
    # cv2.imshow("Stereo_system", img)
    # cv2.waitKey()
