#!bin/bash
digit=$SGE_TASK_ID
python leave_one_out.py 0610.kai.txt $((10*digit)) 10 window RFwindow_rf.out
