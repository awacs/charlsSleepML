# charlsSleepML

# 睡眠数据处理
Excel 表如 睡眠时间记录（手环佩戴）_20210610.xlsx 所示处理，提取后七列数据为0610sleep.txt
## 睡眠数据qc
使用`python timeclean.py 0610sleep.txt > 0610cleansleep.txt` 进行数据清理。如有error手动修改0610sleep.txt。

# Activity monitor 数据处理分析
全部代码在 interp.sh中。

## HMM parameters retraining
hmm_para.py 和 hmm_para_timevar.py 涉及 hmm parameter retraining.

# 数据分析

## Random Forest Training & Evaluation
我们重新进行了random forest的训练与evaluation,基本总结在leave_one_out.py。使用方法参考tosubmit_window.sh。

## 制图
Figure 1 code: qc.py

Figure 2 code: windowsize.py

Figure 3 code: fig6A.py

Figure 4 code: Excel 

Figure 5 code: histogram.py
