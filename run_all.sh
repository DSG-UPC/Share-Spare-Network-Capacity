#/user/bin/env bash

#EXPNO=1

for EXPNO in 1 2 3 4 5 6 7 8 9 10
do

	date > done
	echo 'EXPERIMENT' $EXPNO >> done
	fab run_exp:exp=baseline,mixed=mix,exp_no=$EXPNO,duration=60s >> done
	sleep 3m
	date >> done
	echo "MIX EXPERIMENT Baseline Done" >> done
	fab run_exp:exp=baseline,mixed=no,exp_no=$EXPNO,duration=60s >> done
	sleep 3m
	date >> done
	echo "ALONE EXPERIMENT Baseline Done" >> done

	for i in 'ipip' 'tcplp' 'tcpvegas' 'codel' 'borrowing'
	do
		fab setup_$i >> done
		date >> done
		echo "SETUP $i Done" >> done
		fab run_exp:exp=$i,mixed=mix,exp_no=$EXPNO,duration=60s >> done
		sleep 3m
		date >> done
		echo "MIX EXPERIMENT $i Done" >> done
		fab run_exp:exp=$i,mixed=no,exp_no=$EXPNO,duration=60s >> done
		sleep 3m
		date >> done
	        echo "ALONE EXPERIMENT experiment $i Done" >> done
		fab clear_$i >> done
		date >> done
		echo "CLEARED UP $i" >> done
	done
	
	date >> done
	echo 'DONE' >> done
done
echo 'FINALLYYYYY' >> done
exit 0
