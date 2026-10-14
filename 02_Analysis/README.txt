Phasera — A901005 | 실행 및 방법론 안내

[빠른 시작]
1. A901005.zip과 A901005_weights.zip을 같은 폴더에 압축 해제합니다.
   02_Analysis/model_bundle/manifest.json이 있으면 가중치 복원이 완료된 것입니다.
2. 02_Analysis에서 conda env create -f environment.yml 후 conda activate komap-oct09
3. python Phasera.pyz validate
4. python Phasera.pyz predict --input /path/to/test/images --output /path/to/new_output
입력은 원본 PNG만 있는 폴더, 출력은 아직 존재하지 않는 폴더입니다.
Python 실행 패키지(.pyz)이며 Python을 포함한 독립 EXE는 아닙니다.
검증 환경은 Linux x86_64, Python 3.12.3, PyTorch 2.8.0+cu128, NVIDIA CUDA입니다.
Windows는 일반 ZIP 압축 해제가 가능하며 GPU 실행은 WSL2/Linux CUDA 환경을 사용합니다.
설치 이후 추론에는 네트워크·토큰·정답이 필요하지 않습니다.

[핵심 방법론과 코드 위치]
• 원본 해상도 U-Net: code/src/native_unet.py
  U-Net skip 구조로 미세 공정 Si 경계 정보를 보존합니다. 블록 자체의 원천 발명을 주장하지 않습니다.
• 동결 DINOv2 문맥 결합: code/experiments/oct04_context/train_whole_semantic_base.py
  전체 시야 특징을 학습 가능한 1×1 projection으로 native bottleneck에 합산합니다.
• 확률 앙상블: code/inference/predict.py, worker_new.py
  9개 고유 checkpoint의 15개 경로를 원본 좌표계로 복원하고 순서·정밀도를 고정해 결합합니다.
• 조성 조건부 보정과 성분 정제: code/inference/postprocess.py
  HuBMAP의 조건별 threshold 전략을 예측 조성 기반 9계수 log-offset으로 확장합니다.
  작은 Primary Si 성분만 정제하고 테두리는 보호합니다. 정답 존재 상을 추론에 입력하지 않습니다.
• 공식 지표·손실: code/evaluate.py, code/experiments/oct09_official/official_metric.py
  GT에 있는 상의 IoU를 이미지별 평균한 뒤 영상을 동일 가중 평균합니다.
  soft-IoU+CE는 실험용 대리식입니다. Lovasz 및 logit adjustment의 정확한 재현 구현은 아닙니다.
• 보정 비교: code/experiments/oct09_official/calibrate_context.py, components_context.py
  낮은 차원 차분진화와 보정 단계 그룹 교차검증을 사용했습니다. 비채택 실험도 포함됩니다.
각 핵심 파일의 한국어 주석에 설계 의도, 원문 URL, 과제별 변형, 한계를 기록했습니다.

[성능과 재현 범위]
python Phasera.pyz evaluate --predictions validation_predictions --masks /path/to/valid/masks --output evaluation.json
제공 valid20 공식 점수: 81.0665%. 보정 단계 그룹 교차검증: 80.6410%.
valid를 모델·보정 선택에 반복 사용했으므로 독립 test 또는 전체 nested CV 성능이 아닙니다.
세 추가 학습 실험은 시작 step 0이 선택되어 최종 가중치에 추가되지 않았습니다.
python code/bootstrap_training.py --data /path/to/DATA --bundle model_bundle
python code/experiments/oct09_official/train_aligned.py --mode control
aligned와 mixed 모드도 제공됩니다. DATA는 train/valid의 images, masks 폴더를 포함해야 합니다.
전체 후보 검색에는 제출에 없는 과거 확률 캐시가 추가로 필요합니다.

[가중치와 무결성]
WEIGHTS_INDEX.csv: 15개 경로 이름·계열·가중치·파일 경로·SHA256을 대응시킨 목록.
model_bundle: 내용 해시 기반 파일명과 경로를 유지합니다. 실제 추론 가중치는 9개이며,
이전 번들의 무결성 계약에 필요한 비활성 2개를 포함해 총 11개 파일입니다. WEIGHTS_FILES.csv에 역할을 표시했습니다.
이번 개정은 주석 추가입니다. 9개 핵심 모듈의 실행 AST 동일성과 가중치 바이트 일치를 검사했습니다.
주석으로 바뀐 runtime 해시만 manifest에 갱신했으며 모델 구성·계수·예측 PNG는 동일합니다.
변경 추적: reports/comment_revision_verification.json. 과거 실행 기록의 manifest 해시는 당시 버전입니다.

[그림·참고문헌]
별도 분석 환경에서 pip install -r report_requirements.txt
python code/report_figures.py --data /path/to/DATA --output /path/to/new_figures
python code/report_architecture.py --output /path/to/new_figures
원본 데이터는 대회 제공본을 사용합니다. 문헌 URL은 reports/research_sources_oct14.json에 있습니다.
2025/2026 관련 연구 및 기관 연계는 후속 검증 방향이며 모두 구현된 방법이라는 뜻은 아닙니다.
참고 코드 고지/라이선스는 기존 NOTICE를 보존했습니다. 외부 저장소 변경은 하지 않았습니다.
