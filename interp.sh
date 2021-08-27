set -euox 
f=$1
ln -s $f interpolate ||true
bf=$(basename $f)
# python datetime_convert.py interpolate/$bf # date time conversion
# python datetime_alt.py interpolate/$bf # date time conversion alternative
# python accProcess.py interpolate/"convert_$bf" --deleteIntermediateFiles False --timeZone UTC
zcat interpolate/"convert_$bf" |awk -F',' '{if($6!=""||$7!="")print $0}'>interpolate/"$bf-withtemp.txt"
base=$(basename $bf .csv.gz)
python interpol.py interpolate/"convert_$base-epoch.csv.gz" interpolate/"$bf-withtemp.txt" interpolate/"convert_$base-X.csv.gz"
python getY.py interpolate/"convert_$base-epoch.csv.gz" 0619_cleanedsleep.txt interpolate/"convert_$base-Y.txt"