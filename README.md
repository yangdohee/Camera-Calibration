# Camera-Calibration
The program utilizes OpenCV to implement camera calibration and distortion correction. It can analyze images with checkboard patterns to calculate the camera's internal parameters and distortion coefficients, and correct distortion

`calibration_result.npz` 파일이 아직 업로드되지 않아서 내부 파라미터를 자동으로 가져오진 못했어.  
아래처럼 **네가 코드 실행 시 출력된 실제 값**을 직접 입력해줘!

---

## 📷 Camera Calibration & Distortion Correction

### ✅ 과제 목표  
내 카메라(노트북/휴대폰 등)로 촬영한 체스보드 영상을 이용해  
OpenCV를 통해 **카메라 캘리브레이션**과 **렌즈 왜곡 보정**을 수행한다.

---

### 📁 사용한 데이터

- **체스보드 영상**: `checkboard2.mp4`  
- **체스보드 패턴**: 11x8 칸 → 내부 코너 수 (10, 7)  
- **촬영 장치**: [사용자 장치명]

---

### 🧪 Step 1. Camera Calibration

- 다양한 각도에서 촬영한 체스보드 프레임들에서 내부 코너점 검출
- `cv2.calibrateCamera()`를 통해 내 카메라의 **내부 파라미터 행렬**, **왜곡 계수** 등을 추정

#### 🔧 Calibration 결과 _(직접 코드에서 복사해서 채워주세요)_

| 항목 | 값 |
|------|----|
| **fx, fy (focal length)** | 예: `mtx[0, 0]`, `mtx[1, 1]` |
| **cx, cy (principal point)** | 예: `mtx[0, 2]`, `mtx[1, 2]` |
| **왜곡 계수 (k1, k2, p1, p2, k3)** | `dist.flatten()` |
| **RMSE (재투영 오차)** | `ret` 값 |

> 실제 결과는 `calibration_result.npz`에 저장됨.  

---

### 🔧 Step 2. Lens Distortion Correction

- 위에서 얻은 파라미터로 `cv2.undistort()` 수행
- **렌즈의 왜곡을 제거한 보정 영상**을 생성

#### 🎥 결과 파일

| 파일명 | 설명 |
|--------|------|
| `undistorted_output.avi` | 왜곡이 제거된 영상 |
| `original_frame.jpg` | 원본 영상의 첫 프레임 |
| `undistorted_frame.jpg` | 보정된 첫 프레임 |
| `calibration_result.npz` | 보정에 사용된 파라미터 저장 파일 |

---

### 📌 참고 코드 구조

- `camera_calibration.py`: 체스보드 인식 및 카메라 보정 수행
- OpenCV 함수:
  - `cv2.findChessboardCorners()`
  - `cv2.calibrateCamera()`
  - `cv2.undistort()`

---

### 💬 참고 사항

- 동영상은 약 369 프레임
- 총 74개의 프레임에서 체스보드 검출 성공
- 해상도와 영상 길이에 따라 계산 시간은 수 분 소요될 수 있음
- OpenCV 4.x 버전 사용

---

📌 **마지막 단계**  
`calibration_result.npz` 파일을 업로드해주면 내가 직접 결과 채워서 다시 만들어줄 수도 있어!  
아니면 위의 설명대로 **너가 출력된 결과를 복사해서 표에 붙여 넣기**만 하면 돼.  
필요하면 `.md` 파일 형태로도 만들어줄게.
