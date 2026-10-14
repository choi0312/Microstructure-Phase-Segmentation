from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
R=Path(__file__).resolve().parents[1];F=R/'docs/figures';O=R/'docs/Microstructure_Phase_Segmentation.pdf'
pdfmetrics.registerFont(TTFont('Nanum',str(R/'docs/fonts/NanumGothic-Regular.ttf')))
pdfmetrics.registerFont(TTFont('NanumBold',str(R/'docs/fonts/NanumGothic-Bold.ttf')))
pdfmetrics.registerFontFamily('Nanum',normal='Nanum',bold='NanumBold',italic='Nanum',boldItalic='NanumBold')
styles={
 'title':ParagraphStyle('title',fontName='NanumBold',fontSize=22,leading=31,spaceAfter=18,wordWrap='CJK'),
 'h1':ParagraphStyle('h1',fontName='NanumBold',fontSize=17,leading=24,spaceAfter=15,wordWrap='CJK'),
 'h2':ParagraphStyle('h2',fontName='NanumBold',fontSize=11.5,leading=17,spaceBefore=12,spaceAfter=7,wordWrap='CJK'),
 'body':ParagraphStyle('body',fontName='Nanum',fontSize=10.2,leading=16.2,spaceAfter=9,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='Nanum',fontSize=8.4,leading=12.5,spaceAfter=8,wordWrap='CJK',textColor=HexColor('#475569')),
 'cell':ParagraphStyle('cell',fontName='Nanum',fontSize=9,leading=13,wordWrap='CJK'),
 'head':ParagraphStyle('head',fontName='NanumBold',fontSize=9,leading=13,wordWrap='CJK',textColor=white),
}
S=[];W=A4[0]-96

def fmt(t):return str(t).replace('₃','<sub>3</sub>').replace('ᵢ','<sub>i</sub>').replace('−','-').replace('σ','표준편차').replace('á','a')
def p(t,style='body'):S.append(Paragraph(fmt(t),styles[style]))
def h(t):p(t,'h2')
def fig(name,width=W):
 path=F/name;im=PILImage.open(path);w,ht=im.size;S.append(Image(str(path),width=width,height=width*ht/w));S.append(Spacer(1,5))
def cap(t):p(t,'small')
def table(headers,rows,widths):
 data=[[Paragraph(fmt(c),styles['head']) for c in headers]]+[[Paragraph(fmt(c),styles['cell']) for c in row] for row in rows]
 t=Table(data,colWidths=[W*v for v in widths],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#263f51')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f1f5f8')]),('GRID',(0,0),(-1,-1),.4,HexColor('#ced7df')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));S.append(t);S.append(Spacer(1,10))
def page(n,title):
 if S:S.append(PageBreak())
 p(f'{n:02d}  {title}','h1')

p('미세조직 영상의<br/>조성 조건부 상 분할','title')
p('국소·전역 특징 결합과 영상별 결정 경계 적응','h1')
p('개인 연구 프로젝트 · 기술 보고서 · 2026년 10월','small')
h('초록')
p('고탄성 알루미늄 합금의 미세조직 정량화는 상의 면적뿐 아니라 입자의 크기·형상과 가는 경계의 보존을 요구한다. 본 연구는 광학현미경 영상을 Al, Primary Si, Al₃Ni, Eutectic Si로 분할하고, 상별 공간 스케일과 영상별 분포 변화에 대응하는 추론 구조를 구성하였다.')
p('원본 해상도 U-Net에 동결 DINOv2의 전체 시야 특징을 결합하고, 서로 다른 모델 경로의 확률을 원본 좌표에서 집계하였다. 예측 상 질량에서 추출한 연속 문맥으로 세 비기준 상의 log 확률을 보정하는 9계수 모델을 적용하고, 초정 Si에만 선택적 연결 성분 정제를 수행하였다.')
p('외부 제공 영상 중 학습 70장과 개발 검증 20장을 사용했다. 정답 존재 상을 평균한 이미지별 IoU는 기본 구성의 80.5277%에서 81.0665%로 증가했다. 보정 단계 그룹 교차검증은 80.6410%였다. 검증셋을 모델과 설정 선택에 반복 사용했으므로 결과는 개발 검증 성능으로 해석한다.')
table(['핵심 구성','연구적 역할'],[['원본 해상도 + 전역 문맥','미세 경계와 큰 입자의 주변 조직을 함께 표현'],['조성 조건부 확률 보정','영상별 예측 상 분포에 따라 상 간 결정 경계를 조절'],['상별 선택적 정제','큰 초정 입자와 가는 공정 조직에 다른 형상 규칙 적용']],[.36,.64])
h('핵심 결과와 해석')
p('최종 구성은 9개 고유 checkpoint와 15개 추론 경로이다. 조건부 보정은 81.0151%, 성분 정제 결합은 81.0665%를 기록했다. 추가 학습과 가중치 재탐색에서 개선이 확인되지 않은 변경은 최종 구성에 포함하지 않았다.')
cap('연구 범위: 광학현미경 영상의 2차원 의미 분할. 화학 조성 추정, 실측 물성 예측 및 외부 시편 일반화는 본 결과가 직접 입증하는 범위에 포함하지 않는다.')

page(2,'연구 문제와 소재 도메인')
h('2.1 상별 형상이 만드는 다중 스케일 문제')
p('Al 기지는 상대적으로 밝고 연속적인 영역을 형성한다. 초정 Si는 큰 어두운 각형 입자로, Al₃Ni는 판·막대·섬 형태로 관찰된다. 공정 Si는 가는 망상 조직을 이루므로 같은 영상에서도 보존해야 하는 공간 크기가 크게 다르다. 명도는 관찰 특징이며 화학 조성의 직접 측정값이 아니다.')
table(['상','영상에서 관찰한 경향','모델링 함의'],[['Al','밝고 연속적인 기지','넓은 영역의 안정적인 확률 유지'],['Primary Si','큰 어두운 각형 입자','주변 문맥으로 미세 공정 조직과 구분'],['Al₃Ni','판·막대·섬 형태','국소 형태와 인접 조직의 동시 해석'],['Eutectic Si','얇은 어두운 망상 구조','원본 해상도 특징과 경계 정보 전달']],[.20,.36,.44])
h('2.2 물성 해석으로 이어지는 조직 정보')
p('고탄성은 탄성 변형에 대한 강성과 관련되며 인장강도와 동일한 개념이 아니다. 상 분할의 활용 가치는 단순한 색 영역 면적을 넘어 상별 분율, 입자 형상, 분포와 공간적 관계를 정량화하는 데 있다. 이러한 지표는 조성·공정 변화에 따른 조직 차이를 분석하는 입력이 될 수 있다.')
h('2.3 설계 가설')
p('첫째, 원본 공간 특징을 유지하면 과도한 축소로 손실되는 공정 Si 경계를 보존하는 데 도움이 될 수 있다. 둘째, 전체 시야의 문맥은 국소 명도만으로 구분하기 어려운 상의 주변 조직을 설명할 수 있다. 셋째, 예측 상 분포를 저차원 문맥으로 사용하면 고정 편향보다 영상별 결정 경계를 유연하게 조절할 수 있다.')
p('본 연구는 이 가설을 분할 경로의 결합과 조건부 보정에 반영했다. 각각의 구조가 독립적으로 기여한 양을 모두 분리해 입증한 것은 아니며, 확인된 보정 단계 비교와 전체 개발 검증 결과를 구분해 제시한다.')
h('2.4 분석 단위의 구분')
p('영상의 픽셀 크기와 물리적 관찰 배율은 별개이다. 물리 길이를 사용하지 않는 현재 모델에서 128 px 성분 정제는 경험적 픽셀 규칙이다. 2차원 면적분율을 체적분율로 해석하려면 대표 절단면과 입체계량 가정이 추가로 필요하다.')

page(3,'데이터 분석과 관찰 근거')
p('학습 70장과 개발 검증 20장의 외부 제공 영상·마스크를 분석했다. 영상 폭은 675–1,440 px, 높이는 480–1,024 px이다. 파일·복호화 RGB 기준 완전 중복은 원래 영상 집합 100장 중 발견되지 않았으나, 같은 시편의 부분 중첩까지 배제하는 근거는 아니다.')
fig('phase_distribution.png')
cap('그림 1. 이미지별 상 면적분율의 평균. 픽셀을 전체 합산한 분율과 구분한다.')
p('Al의 평균 면적분율은 train 57.91%, valid 61.41%이고, Al₃Ni는 25.14%에서 20.03%로 달라진다. 이러한 차이는 전역 상 비율을 강제하는 대신 현재 영상의 예측 문맥을 사용하는 설계 근거다. 이 통계만으로 모집단의 분포 이동을 확정하지는 않는다.')
fig('morphology.png',W*.92)
cap('그림 2. 원본, 4상 정답 마스크와 국소 확대. 확대 영역은 관찰용이며 물리적 길이 척도를 뜻하지 않는다.')
p('8-이웃 경계에서 1 px 이내에 위치하는 공정 Si 픽셀은 train 63.16%, valid 63.59%였다. 경계 2 px 이내에서는 각각 87.92%, 87.75%로, 많은 픽셀이 경계에 가까운 얇은 조직에 속했다. 이는 경계 보존의 필요성을 뒷받침하며 라벨 오류율이나 성능 상한을 의미하지 않는다.')

page(4,'국소·전역 표현과 추론 구조')
fig('architecture_v2.png')
cap('그림 3. 확률 결합·조건부 보정의 전체 추론 흐름과 대표 Native64–DINOv2 문맥 결합 구조. 모든 경로의 backbone이 동일한 것은 아니다.')
h('4.1 원본 해상도 경로')
p('Native64는 64→128→256→512→768 채널의 인코더, 네 번의 pooling, residual block 및 skip decoder를 사용한다. 입력 공간 크기를 보존하는 stem과 skip 연결을 통해 가는 경계 정보를 디코더로 전달한다.')
h('4.2 동결 문맥의 투영')
p('전체 영상의 장축을 약 448 px, 14의 배수로 조정하여 동결 ViT-B/14의 특징을 얻는다. 학습 가능한 1×1 projection으로 채널을 정합한 뒤 bottleneck 공간 크기로 보간·합산한다. Projection은 0으로 초기화해 기존 국소 경로의 초기 출력을 유지하며, 전체 시각 인코더는 동결한다.')
h('4.3 원본 좌표에서의 확률 결합')
p('최종 9개 고유 checkpoint를 15개 스케일·TTA 경로로 실행한다. 경로별 역변환을 적용해 원본 H×W로 맞춘 뒤 FP32에서 확률 가중합을 계산한다. Argmax 마스크 투표 대신 확률을 결합해 각 상의 상대적 불확실성 정보를 후속 보정에 전달한다.')

page(5,'전처리와 평가 목적의 정렬')
h('5.1 공간 대응과 광학 관찰 특성')
p('원본 PNG의 알파·색상 모드와 크기를 확인한 뒤 회색조로 읽고, 경로별 필요에 따라 RGB 반복·정규화를 적용한다. 정답 RGB 팔레트는 혼합 보간 없이 정수 class로 정확히 대응시킨다. 영상과 마스크의 크기가 다르거나 정의되지 않은 색이 있으면 처리를 중단한다.')
table(['처리','설정 또는 원칙'],[['기하 증강','영상과 마스크에 공동 90도 회전·반전 적용'],['밝기·대비','대표 문맥 경로: 확률 0.5, 대비 0.9–1.1, 밝기 ±0.08'],['감마·잡음','감마 확률 0.3 / 0.9–1.1; Gaussian noise 확률 0.15 / σ=0.01'],['전체·패치 비교','전체 50%, crop 50% 실험; 최종 추가 checkpoint로 채택되지 않음'],['출력','원본 H×W와 네 가지 RGB 팔레트 유지']],[.24,.76])
h('5.2 정답 존재 상을 기준으로 하는 IoU')
fig('metric_formula.png')
p('이미지 i의 정답에 실제 존재하는 상 집합을 Cᵢ로 정의한다. 상별 IoU를 Cᵢ에 대해서만 평균하고, 이미지별 점수를 동일 가중 평균한다. 정답에 없는 상은 예측에도 없거나 예측에만 있더라도 클래스 평균에서 제외한다. 예측 전용 상으로 잘못 분류한 픽셀은 실제 정답 상의 FN에 남는다.')
h('5.3 학습 대리식과 실제 선택 목적')
p('추가 학습 비교는 이미지별·정답 존재 상별 평균을 유지하는 0.8×soft-IoU loss + 0.2×CE를 사용했다. Soft-IoU는 교집합과 합집합을 확률로 계산하는 미분 가능한 대리식이며, argmax 기반 IoU와 수치적으로 동일하지 않다. 평가와 보정 선택에서는 실제 hard IoU를 계산했다.')
p('큰 이미지에 더 높은 가중치를 부여하는 pooled confusion 계산이나 상별 평균을 다시 단순 평균하는 방식은 이 목적과 다르다. 구현에서는 정답 pixel count가 0보다 큰지로 존재 상을 판단하며, 예측 union만으로 집합을 정하지 않는다.')

page(6,'조성 조건부 보정과 선택적 정제')
p('앙상블 확률 q의 공간 평균 m을 예측 상 질량으로 정의한다. Al₃Ni와 공정 Si의 상대 질량 균형 r, 초정 Si의 로그 질량 h를 계산하여 f=[1,r,h]를 구성한다. 이 변수는 화학 조성의 실측값이 아니라 영상 예측으로부터 얻은 조직 문맥이다.')
fig('calibration_formula.png')
cap('그림 4. 연속 문맥에 따른 class별 log 확률 보정. Al 편향은 0으로 두고 비기준 세 상에 각각 3개 계수를 사용한다.')
table(['상','상수항','r 계수','h 계수'],[['Primary Si','−0.489334','0.689134','0.695705'],['Al₃Ni','0.398452','−0.699344','−0.692782'],['Eutectic Si','−0.460067','0.516027','0.698913']],[.28,.24,.24,.24])
cap('설명용 반올림 값. 실행 설정은 원래 정밀도의 계수를 사용한다.')
h('6.1 저차원 조건부 결정 경계')
p('세 상에 각각 상수항·r·h 계수를 적용하므로 전체 보정은 9계수로 표현된다. 한 상의 offset이 증가하면 다른 상과의 상대 경쟁 경계가 바뀐다. 영상별 임계값을 낮은 차원으로 제어하면서, 정답 존재 여부나 영상 ID에 대한 lookup 없이 현재 예측 문맥에 반응한다.')
p('계수 선택에는 hard IoU를 목적값으로 하는 차분진화를 사용했다. 최종 상수항 탐색 범위는 ±0.5, 기울기 범위는 ±0.7이었다. 이는 비미분 목적의 경험적 탐색이며 전역 최적성을 보장하지 않는다.')
h('6.2 상별 형태를 반영한 정제')
p('Primary Si 마스크의 8-연결 성분이 128 px 이하이고 영상 테두리에 닿지 않을 때만 해당 픽셀을 다른 세 상 중 보정 점수가 가장 높은 상으로 재할당한다. 테두리는 큰 입자의 잘린 조각일 수 있어 보호한다. 공정 Si에는 같은 제거 규칙을 적용하지 않아 얇은 구조를 일괄 제거하지 않는다.')
p('예측 질량 조건화와 성분 정제는 서로 다른 수준에서 작동한다. 전자는 영상 전체의 상 간 확률 관계를 바꾸며, 후자는 최종 마스크의 국소적인 연결 성분에만 적용된다.')

page(7,'비교 실험과 검증 결과')
fig('performance.png')
cap('그림 5. 동일한 GT-present image-macro IoU 기준 비교. 그룹 교차검증은 보정 단계만 분리한 결과다.')
table(['비교 설정','개발 검증','보정 단계 그룹 교차검증'],[['고정 상별 보정','80.5305%','80.2004%'],['조건부 보정 · 좁은 범위','80.8203%','80.4673%'],['좁은 범위 + 성분 정제','80.8767%','80.5122%'],['불확실성 특징 추가','80.8553%','80.4295%'],['명도 대비 특징 추가','80.8432%','80.4400%'],['조건부 보정 · 넓은 범위','81.0151%','80.5926%'],['최종 보정 + 정제 · 캐시','81.0664%','80.6410%']],[.46,.24,.30])
p('원본 이미지를 입력하여 새로 생성한 마스크의 평가 점수는 81.0665%이다. 캐시 기반 선택값 81.0664%와의 차이는 약 0.00003%p로 수치 정밀도 차이에 해당한다. 기존 최종 구성 대비 향상은 0.5388%p이다.')
h('7.1 개선되지 않은 변경의 처리')
p('44개 후보에 대한 simplex 가중치 탐색은 기존 가중치를 대체할 검증된 개선을 만들지 못했다. control / aligned / mixed의 세 추가 학습은 같은 DINOv2 Base 문맥 checkpoint에서 비교했으며 시작 step 0이 모두 선택되었다. 따라서 새 학습 가중치는 최종 앙상블에 포함하지 않았다.')
h('7.2 검증 해석')
p('그룹 교차검증은 영상 식별자의 A 그룹을 묶은 5개 구간에서 보정 계수·성분 크기를 적합하고 held-out 구간을 평가한 결과다. 앞선 checkpoint와 후보 선택에 검증셋이 사용되었으므로 전체 파이프라인의 독립 nested CV가 아니다. 제공된 식별자의 물리적 의미가 확정된 것도 아니므로 그룹 구분은 보수적 진단으로 해석한다.')

page(8,'상별 진단과 오류 분석')
table(['상','정답 존재 영상 평균 IoU','해석'],[['Al','94.4574%','넓은 기지 영역에서 높은 일치도'],['Primary Si','91.5439% · 19장','큰 입자의 분할은 상대적으로 안정적'],['Al₃Ni','77.2207%','형태 다양성과 인접 상의 혼동'],['Eutectic Si','62.3868%','얇은 경계와 세부 구조의 잔여 오차']],[.22,.33,.45])
p('위 수치는 각 상이 정답에 존재하는 영상에 한해 평균한 진단값이다. Primary Si는 19장, 나머지 상은 20장으로 분모가 다르므로 네 수치의 단순 평균은 전체 평가 점수가 아니다.')
fig('qualitative.png')
cap('그림 6. 어려운 A71 영상과 높은 점수의 A117 영상. 빨간 픽셀은 정답과 다른 예측이며, 두 예시는 전체 20장 평가를 대체하지 않는다.')
h('8.1 영상별 개선의 비균질성')
p('캐시 기준 13장은 개선되고 7장은 악화되었다. A71은 57.9154%에서 64.6850%, A11_step1_sample4는 76.9625%에서 79.7164%로 증가하여 평균 향상의 큰 부분을 차지했다. 일부 영상에서 보정의 효과가 집중되므로 모든 조직 유형에 일관된 개선이 있다고 해석하지 않는다.')
h('8.2 경계 오차와 정량 지표의 차이')
p('픽셀 IoU는 전체 일치도를 요약하지만, 얇은 경계의 이동과 입자 형상 변화가 소재 지표에 미치는 영향을 충분히 설명하지 못할 수 있다. 상 면적분율 오차, 경계 허용 오차 및 입자 크기 분포 오차를 함께 측정하면 후속 소재 분석에 대한 영향을 더 직접적으로 평가할 수 있다.')

page(9,'알고리즘적 기여와 연구적 확장')
h('9.1 국소·전역 특징의 공간적 역할 분담')
p('원본 해상도 경로는 미세 공정 조직의 경계를 전달하고, 동결 시각 인코더는 전체 시야의 형태 문맥을 제공한다. 학습 가능한 projection을 통한 bottleneck 결합은 두 표현을 서로 다른 공간 범위에서 통합한다. 동결 문맥은 학습 표본이 작은 환경에서 전체 인코더를 재적합하는 부담을 제한한다.')
h('9.2 예측 조직 문맥에 조건화한 결정 경계')
p('영상별 예측 질량을 연속 특징으로 사용함으로써 고정 class bias를 조건부 보정으로 확장한다. 9개 계수는 상 간 질량 균형과 초정 입자의 규모를 네 상의 상대적인 결정 경계로 연결한다. 문맥은 영상의 예측에서만 얻으므로 정답 상 존재 여부를 추론 규칙에 주입하지 않는다.')
h('9.3 상별 형상에 따른 비대칭 정제')
p('초정 Si와 공정 Si는 모두 어둡게 보일 수 있지만 공간적 형상이 다르다. 초정 Si의 작은 성분만 선택적으로 처리하고 공정 Si에는 같은 면적 규칙을 강제하지 않는 설계는 이 도메인 차이를 추론 규칙에 반영한다. 이러한 설계는 개별 backbone의 원천 발명이나 보편적인 우위를 의미하지 않는다.')
table(['연구 방향','연결되는 계산 과제','추가 확인 요소'],[['조직 정량화','상별 면적분율·장축·종횡비','픽셀 오차가 지표에 전파되는 정도'],['조직–물성 분석','조성·공정·조직 특징의 연결','실측 물성, 독립 시편, 교란 요인'],['적응적 데이터 선택','불확실 영상의 전문가 검토','선택 규칙과 학습 효과의 분리'],['모델 경량화','경로 축소·증류·선택적 TTA','정확도, 지연 시간, 메모리 동시 평가']],[.22,.38,.40])
h('9.4 적용 범위')
p('현재 결과는 2차원 영상 분할의 개발 검증이다. 물성 예측이나 분석 시간 단축은 직접 측정하지 않았다. 소재 연구에 적용하려면 촬영 배율·장비·시편의 변화를 분리해 평가하고, 물리적 화소 크기와 정량 조직 지표의 관계를 명시해야 한다.')

page(10,'구현 범위와 학술적 배경')
h('10.1 연구 코드의 구성')
table(['구성','역할'],[['code/src/','원본 해상도 및 실험 분할 모델'],['code/experiments/context/','동결 문맥 특징의 결합 실험'],['code/experiments/calibration/','평가 정렬 손실과 보정 비교'],['code/inference/postprocess.py','조성 조건부 보정·선택적 성분 정제'],['code/evaluate.py','GT-present image-macro IoU'],['results/','개발 검증 예측과 상별·영상별 통계']],[.48,.52])
p('연구 환경은 Python 3.12.3, PyTorch 2.8.0+cu128, torchvision 0.23.0, timm 1.0.30, segmentation_models_pytorch 0.5.0이다. 원본 데이터·정답·checkpoint·대용량 모델 번들은 배포하지 않는다. 평가는 외부 정답 마스크를 준비해야 하며, 전체 추론은 현재 코드에 맞는 모델 번들을 필요로 한다.')
h('10.2 해석상의 경계')
p('실험 폴더에는 최종 구성에 채택되지 않은 손실·샘플링·특징 비교가 포함된다. 기술한 최종 결과는 동결된 모델과 설정을 기준으로 하며, 개별 실험 파일의 존재가 성능 향상이나 채택을 뜻하지 않는다. 기본 분할 구조, 사전학습 시각 표현 및 확률 보정 관점은 아래 학술적 배경과 구분하여 기술하였다.')
h('참고문헌')
refs=[
'[1] Ronneberger et al. U-Net: Convolutional Networks for Biomedical Image Segmentation. MICCAI, 2015. arxiv.org/abs/1505.04597.',
'[2] Oquab et al. DINOv2: Learning Robust Visual Features without Supervision. 2023. arxiv.org/abs/2304.07193.',
'[3] Menon et al. Long-tail learning via logit adjustment. ICLR, 2021. arxiv.org/abs/2007.07314.',
'[4] Berman et al. The Lovász-Softmax loss. CVPR, 2018. arxiv.org/abs/1705.08790. 본 추가 학습은 별도의 soft-IoU+CE 대리식을 사용한다.',
'[5] Liu et al. Semi-Supervised Segmentation Framework for Quantitative Analysis of Material Microstructure Images. CMC 87(1), 2026. doi:10.32604/cmc.2026.074681.',
'[6] Li et al. Patch-sampled contrastive learning for dense prediction pretraining in metallographic images. Scientific Reports 16, 2994. doi:10.1038/s41598-025-32855-5.',
'[7] Abebe et al. SAM-I-Am. Computational Materials Science 246, 113400, 2025. doi:10.1016/j.commatsci.2024.113400. SAM은 본 모델에 사용하지 않았다.'
]
for ref in refs:p(ref,'small')
p('학술적 배경은 구현 범위와 동일하지 않다. 외부 구성요소의 저작권·라이선스 고지는 별도 문서에 유지한다.','small')

def footer(c,d):
 c.setFont('Nanum',8);c.setFillColor(HexColor('#64748b'));c.drawString(48,28,'MICROSTRUCTURE PHASE SEGMENTATION');c.drawRightString(A4[0]-48,28,f'{d.page} / 10')
doc=SimpleDocTemplate(str(O),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=48,title='Microstructure Phase Segmentation',author='Personal Research Project')
doc.build(S,onFirstPage=footer,onLaterPages=footer)
print(O)
