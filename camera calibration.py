import cv2
import numpy as np
import os
import time

#  경로 설정 및 파라미터
video_path = "C:\\Users\\dideh\\OneDrive\\cvdata\\checkboard2.mp4"
chessboard_size = (10, 7)  # 내부 코너 수
output_video_path = "undistorted_output.avi"

print("[INFO] > > Step 1: Camera Calibration 시작...")

# 체스보드 객체 점 (3D)
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

objpoints = []  # 3D 점
imgpoints = []  # 2D 점
gray_shape = None

cap = cv2.VideoCapture(video_path)
frame_count = 0
used_frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if frame_count % 5 == 0:  # 성능 위해 매 5프레임만 사용
        print(f"[INFO] > 프레임 {frame_count}: 체스보드 {'검출 성공' if found else '실패'}")

        if found:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgpoints.append(corners2)
            gray_shape = gray.shape[::-1]
            used_frame_count += 1

    frame_count += 1

cap.release()

if len(objpoints) == 0:
    print("[ERROR]  캘리브레이션에 사용할 체스보드가 감지되지 않았습니다.")
    exit()
if gray_shape is None:
    print("[ERROR]  gray 이미지 크기를 알 수 없습니다.")
    exit()

print(f"[DEBUG] > calibrateCamera 호출 중... 사용된 프레임 수: {used_frame_count}")

# 타이머 시작
start_time = time.time()

try:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_shape, None, None)
except Exception as e:
    print("[ERROR]  calibrateCamera 중 에러 발생:", e)
    exit()

elapsed = time.time() - start_time
print(f"[INFO]  calibrateCamera 완료 (소요 시간: {elapsed:.2f}초)")

# RMSE 계산
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error
rmse = mean_error / len(objpoints)

print("\n[RESULT] > 카메라 캘리브레이션 결과")
print("Camera Matrix:\n", mtx)
print("Distortion Coefficients:\n", dist.ravel())
print("RMSE:\n", rmse)

np.savez("calibration_result.npz", mtx=mtx, dist=dist)

#  Step 2: 왜곡 보정
print("\n[INFO] > > Step 2: Distortion Correction 시작...")

cap = cv2.VideoCapture(video_path)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (w, h))

if not out.isOpened():
    print("[ERROR] 비디오 저장 실패. 코덱/경로 확인 필요.")
    exit()

frame_index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO]  왜곡 보정 완료")
        break

    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    out.write(dst)

    # 비교 이미지 저장 (첫 프레임만)
    if frame_index == 0:
        cv2.imwrite("original_frame.jpg", frame)
        cv2.imwrite("undistorted_frame.jpg", dst)

    if frame_index % 30 == 0 or frame_index == total_frames - 1:
        print(f"[INFO] > 왜곡 보정 진행 중... {frame_index + 1} / {total_frames}")

    frame_index += 1

cap.release()
out.release()

print("\n 모든 작업 완료!")
print(f"  보정된 영상 저장됨 → {output_video_path}")
print(f"  비교 이미지 저장됨 → original_frame.jpg, undistorted_frame.jpg")
print(f"  캘리브레이션 파라미터 저장됨 → calibration_result.npz")
