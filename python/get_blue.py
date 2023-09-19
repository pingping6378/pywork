import cv2
import numpy as np

def main(args=None):
    cap = cv2.VideoCapture(0)  # 카메라 장치 인덱스를 0으로 설정 (필요에 따라 수정)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 색상 범위 정의
        lower_blue = np.array([100, 100, 120])
        upper_blue = np.array([150, 255, 255])

        lower_green = np.array([50, 150, 50])
        upper_green = np.array([80, 255, 255])

        lower_red = np.array([150, 50, 50])
        upper_red = np.array([180, 255, 255])

        # 색상 마스크 생성
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        # 각 마스크에 대해 비트와이즈 연산 수행
        res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
        res_green = cv2.bitwise_and(frame, frame, mask=mask_green)
        res_red = cv2.bitwise_and(frame, frame, mask=mask_red)

        gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
        _, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = None
        largest_area = 0

        COLOR = (0, 255, 0)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > largest_area:
                largest_area = area
                largest_contour = cnt

        if largest_contour is not None:
            if largest_area > 500:
                x, y, width, height = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + width, y + height), COLOR, 2)
                center_x = x + width // 2
                center_y = y + height // 2

        cv2.imshow("VideoFrame", frame)
        cv2.imshow('Blue', res_blue)
        cv2.imshow('Green', res_green)
        cv2.imshow('Red', res_red)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
