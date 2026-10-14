"""Generate data-distribution and validation-comparison figures from recorded statistics."""
from pathlib import Path
import json,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import fontManager
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=R/'docs/figures');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
fontManager.addfont(str(R/'docs/fonts/NanumGothic-Regular.ttf'))
plt.rcParams.update({'font.family':['NanumGothic','DejaVu Sans'],'axes.unicode_minus':False,'font.size':10})
s=json.loads((R/'results/validation_statistics.json').read_text())
fig,ax=plt.subplots(figsize=(8,2.8));x=np.arange(4)
for j,split in enumerate(['train','valid']):
 values=np.array(s[split]['image_mean_phase_fractions'])*100
 bars=ax.bar(x+(j-.5)*.34,values,.3,label=f'{split} (n={s[split]["n"]})',color=['#26485d','#9ab7c6'][j])
 for b,v in zip(bars,values):ax.text(b.get_x()+b.get_width()/2,v+.8,f'{v:.2f}',ha='center',fontsize=9)
ax.set_xticks(x,['Al','Primary Si','Al₃Ni','Eutectic Si']);ax.set_ylabel('Mean image area fraction (%)');ax.set_ylim(0,73);ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False);fig.tight_layout();fig.savefig(a.output/'phase_distribution.png',dpi=240);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,2.7));labels=['Base ensemble','Conditional calibration','Calibration + selective filtering','Calibration-stage group crossfit'];v=[80.5276637,81.0151361,81.0664748,80.6409542]
ax.barh(labels[::-1],v[::-1],color=['#9ab0bb','#247e80','#7fb0a8','#becbd1'],height=.55)
ax.set_xlim(75,83);ax.set_xlabel('GT-present image-macro IoU (%)');ax.spines[['top','right']].set_visible(False)
for i,val in enumerate(v[::-1]):ax.text(val+.08,i,f'{val:.4f}',va='center',fontsize=9)
fig.tight_layout();fig.savefig(a.output/'performance.png',dpi=240);plt.close(fig)
