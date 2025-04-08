# Camera-Calibration
The program utilizes OpenCV to implement camera calibration and distortion correction. It can analyze images with checkboard patterns to calculate the camera's internal parameters and distortion coefficients, and correct distortion


##  Camera Calibration & Distortion Correction

### 사용한 데이터 

- **핸드폰으로 찍은 체크보드 영상**: `checkboard2.mp4`  
- **체크보드 패턴의 정보** : 11x8 칸 → 내부 코너 수 (10, 7)  

---

###  Step 1. Camera Calibration

- 다양한 각도에서 촬영한 체스보드 프레임들에서 내부 코너점 검출
- `cv2.calibrateCamera()`를 통해 내 카메라의 **내부 파라미터 행렬**, **왜곡 계수** 등을 추정

####  Calibration 결과 _(직접 코드에서 복사해서 채워주세요)_

| 항목 | 값 |
|------|----|
| **fx, fy (focal length)** | 예: `mtx[0, 0]`, `mtx[1, 1]` |
| **cx, cy (principal point)** | 예: `mtx[0, 2]`, `mtx[1, 2]` |
| **왜곡 계수 (k1, k2, p1, p2, k3)** | `dist.flatten()` |
| **RMSE (재투영 오차)** | `ret` 값 |

> 실제 결과는 `calibration_result.npz`에 저장됨.  

---

###  Step 2. Lens Distortion Correction

- 얻은 파라미터를 기반으로 `cv2.undistort()` 수행
- **렌즈의 왜곡을 제거한 보정 영상**을 생성

####  결과 파일

| 파일명 | 설명 |
|--------|------|
| `undistorted_output.avi` | 왜곡이 보정된 결과 영상 |
| `original_frame.jpg` | 원본 영상의 첫 프레임 |
| `undistorted_frame.jpg` | 보정된 영상의 첫 프레임 |
| `calibration_result.npz` | 보정에 사용된 파라미터 저장 파일 |

---

###  핵심 코드 구조

- `camera_calibration.py`: 체크보드 인식 및 카메라 보정 수행
- OpenCV 함수:
  - `cv2.findChessboardCorners()`
  - `cv2.calibrateCamera()`
  - `cv2.undistort()`

---

###  extra info

- 동영상은 약 369 프레임
- 총 74개의 프레임에서 체크보드 검출 성공

---
## 원본 동영상
#### before
- https://github.com/user-attachments/assets/87e6ffe1-918b-4b99-9ba3-fcb4e0f02a00
#### after

--- 
#### 전 후 사진 비교 
 - ![미리보기 이미지](original_frame/cvdata.jpg)
 - ![미리보기 이미지](undistorted_frame/cvdata.jpg)
## calibrataion_result.npz
-


