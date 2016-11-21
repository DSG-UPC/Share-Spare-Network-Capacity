#!/usr/bin/env python
from fabric.api import env, run, local, roles, execute, sudo, warn_only
from fabric.context_managers import cd
import time
import help
import sys,getopt
#from datetime import datetime as dt
##HOUR = datetime.timedelta(minutes=2).now().time().strftime('%H%M')
##EXP_HOUR = (datetime.timedelta(minutes=2)+datetime.datetime.now()).time().strftime('%H%M') 

clears = ['clear_codel','clear_ipip','clear_sfq','clear_tcplp','clear_tcpvegas','clear_borrowing']
setups = ['setup_codel','setup_ipip','setup_sfq','setup_tcplp','setup_tcpvegas','setup_borrowing']
helpers = ['restore_nat','delete_nat', 'setup_limit','clear_limit']
exps = ['run_exp']

__all__ =  clears+setups+exps+['sync'] + helpers


env.key_filename = '/home/xarokk/.ssh/exp'
env.user = 'user'

env.roledefs = {
	'server':['xarokk2@147.83.118.123'],
	'client':['xarokk1@192.168.240.2'],
	'router':['xarokk@147.83.118.126']
}


@roles('router')
def now():
	execute(clear_nat,inface='enx00e04c534458',outface='enp0s25')

def server():
	env.hosts = ['147.83.118.124']

def client():
	env.hosts = ['192.168.240.2']

def router():
	env.hosts = ['localhost']

def all():
	env.hosts = ['147.83.118.124','192.168.240.2','localhost']

def test():
	cmd = '"touch manos/test"'
	run('echo '+cmd+' > command')
	run('at now + 1 minutes < command')


@roles('client')
def setup_ipip_client():
	with cd('roc/tunneling/'):
                sudo('./ipip-server.sh')
		sudo('./tunel_client_setup.bash ipiptun1')
	#sudo('route del default gw 192.168.240.1 enp0s25')
	#sudo('route add default gw 192.168.10.1')

@roles('router')
def setup_ipip_router():
	#execute(clear_nat,inface='enx00e04c534458',outface='enp0s25')
	with cd('roc/tunneling/'):
                sudo('./ipip-client.sh')
	execute(clear_nat_8080,inface='enx00e04c534458',outface='enp0s25')
	execute(setup_nat_8080,inface='ipiptun1',outface='enp0s25')

def setup_ipip():
	execute(setup_ipip_router)
	execute(setup_ipip_client)

@roles('router')
def clear_ipip_router():
	execute(clear_nat_8080,inface='ipiptun1',outface='enp0s25')
	execute(setup_nat_8080,inface='enx00e04c534458',outface='enp0s25')	
	sudo('ip tun del ipiptun1')
	#sudo('route del default gw 192.168.240.1 enp0s25')
	#execute(setup_nat,inface='enx00e04c534458',outface='enp0s25')

@roles('client')
def clear_ipip_client():
	with cd('roc/tunneling/'):
		sudo('./tunel_client_clear.bash ipiptun1')
	sudo('ip tun del ipiptun1')
	

def clear_ipip():
        execute(clear_ipip_router)
        execute(clear_ipip_client)

@roles('router')
def setup_codel():
        with cd('roc/tunneling/'):
                sudo('./tc_codel.bash start')

@roles('router')
def clear_codel():
	with cd('roc/tunneling/'):
                sudo('./tc_codel.bash stop')

@roles('router')
def setup_borrowing():
        with cd('roc/tunneling/'):
                sudo('./tc_borrowing.bash start')

@roles('router')
def clear_borrowing():
        with cd('roc/tunneling/'):
                sudo('./tc_borrowing.bash stop')

@roles('router')
def setup_sfq():
        with cd('roc/tunneling/'):
                sudo('./tc_sfq.bash start')

@roles('router')
def clear_sfq():
        with cd('roc/tunneling/'):
                sudo('./tc_sfq.bash stop')

@roles('client')
def setup_tcplp_client():
        with cd('roc/tunneling/tcp_lp'):
                sudo('screen -S tcplp -d -m ./simpletun_tcplp -i tcplp -s')
        sudo('ifconfig tcplp 192.168.10.2/24 up')
	with cd('roc/tunneling'):
		sudo('./tunel_client_setup.bash tcplp')
	#sudo('route add default gw 192.168.10.1 tcplp')

@roles('router')
def setup_tcplp_router():
	#sudo('screen -wipe')
        with cd('roc/tunneling/tcp_lp'):
                run('sudo screen -S tcplp -d -m ./simpletun_tcplp -i tcplp -c 192.168.240.2')
	with warn_only():
		local('sudo screen -ls')
        #sudo('sudo ifconfig -a')
        run('sudo ifconfig tcplp 192.168.10.1/24 up')
	execute(clear_nat_8080,inface='enx00e04c534458',outface='enp0s25')
	execute(setup_nat_8080,inface='tcplp',outface='enp0s25')

def setup_tcplp():
	execute(setup_tcplp_client)
	execute(setup_tcplp_router)

@roles('router')
def clear_tcplp_router():
	sudo('ifconfig tcplp down')
	sudo('sudo screen -X -S tcplp quit')
	execute(clear_nat_8080,inface='tcplp',outface='enp0s25')
	execute(setup_nat_8080,inface='enx00e04c534458',outface='enp0s25')


@roles('client')
def clear_tcplp_client():
	with cd('roc/tunneling'):
		sudo('./tunel_client_clear.bash tcplp')
	with warn_only():
		sudo('ifconfig tcplp down')
		sudo('sudo screen -X -S tcplp quit')

def clear_tcplp():
        execute(clear_tcplp_router)
        execute(clear_tcplp_client)


@roles('client')
def setup_tcpvegas_client():
        with cd('roc/tunneling/tcp_vegas'):
                sudo('screen -S tcpvegas -d -m ./simpletun_tcpvegas -i tcpvegas -s')
        sudo('ifconfig tcpvegas 192.168.10.2/24 up')
	with cd('roc/tunneling'):
		sudo('./tunel_client_setup.bash tcpvegas')
	#sudo('route add default gw 192.168.10.1 tcpvegas')

@roles('router')
def setup_tcpvegas_router():
        #sudo('screen -wipe')
        with cd('roc/tunneling/tcp_vegas'):
                run('sudo screen -S tcpvegas -d -m ./simpletun_tcpvegas -i tcpvegas -c 192.168.240.2')
        with warn_only():
                local('sudo screen -ls')
        #sudo('sudo ifconfig -a')
        run('sudo ifconfig tcpvegas 192.168.10.1/24 up')
        execute(clear_nat_8080,inface='enx00e04c534458',outface='enp0s25')
        execute(setup_nat_8080,inface='tcpvegas',outface='enp0s25')

def setup_tcpvegas():
        execute(setup_tcpvegas_client)
        execute(setup_tcpvegas_router)

@roles('router')
def clear_tcpvegas_router():
        sudo('ifconfig tcpvegas down')
        sudo('sudo screen -X -S tcpvegas quit')
        execute(clear_nat_8080,inface='tcpvegas',outface='enp0s25')
        execute(setup_nat_8080,inface='enx00e04c534458',outface='enp0s25')


@roles('client')
def clear_tcpvegas_client():
	with cd('roc/tunneling'):
                sudo('./tunel_client_clear.bash tcpvegas')
	with warn_only():
		sudo('ifconfig tcpvegas down')
		sudo('sudo screen -X -S tcpvegas quit')


def clear_tcpvegas():
        execute(clear_tcpvegas_router)
        execute(clear_tcpvegas_client)


@roles('client')
def run_exp_client(exp,mixed,exp_no,duration,ip,delay,size):
	"""Client monitored traffic experiment"""
	#if exp in ['tcpvegas']:
	#	ip = "192.168.10.1"
	with cd('/home/xarokk1/manos/primary/wrk2'):
		with warn_only():
			run('mkdir exps/'+exp)
                cmd_env = 'env dir='+exp+' num='+exp_no+' mixed='+mixed+' '
                #cmd_wrk = ' ./wrk -t1 -c25 -d'+duration+' -R25'
                cmd_wrk = ' ./wrk -t1 -c5 -d'+duration+' -R5 --script scripts/report'+delay+'.lua '
		cmd_wrk_url = ' http://'+ip+'/'+size+'Mb.html '
		cmd =  cmd_env+cmd_wrk+cmd_wrk_url
		run('echo '+cmd+' > command')
		retrans_timeout = 'sudo timeout '+duration
		retrans = ' /home/xarokk1/./tcpretrans > exps/'+exp+'/retrans_'+mixed+'_'+exp_no+'.log 2>&1'
		retrans_cmd = retrans_timeout +	retrans
                run('echo \"'+retrans_cmd+'\" > retrans_cmd')
		run('at now + 2 minutes < command')
		sudo('at now + 2 minutes < retrans_cmd')

@roles('client')
def run_exp_client2(exp,mixed,exp_no,duration,ip,size):
	"""Client background(shared) traffic"""
	port = '8080'
	for i in ['ipip','tcplp','ledbat','tcpvegas']:
		if i in exp:
                	ip = "192.168.10.1"
		#port = '8080'
	#elif exp in ['borrowing']:
	#	port = '8080'
        with cd('/home/xarokk1/manos/secondary/wrk2'):
		with warn_only():
                        run('mkdir exps/'+exp)
                cmd_env = 'env dir='+exp+' num='+exp_no+' mixed='+mixed+' '
		cmd_wrk = ' ./wrk -t1 -c25 -d'+duration+' -R25 --script scripts/report.lua'
                cmd_wrk_url = ' http://'+ip+':'+port+'/'+size+'Mb.html '
                cmd =  cmd_env+cmd_wrk+cmd_wrk_url
                run('echo '+cmd+' > command')
                run('at now + 2 minutes < command')

def run_exp(exp,mixed,exp_no,duration,delay="delay",size='008'):
	"""Experiment traffic and background traffic from client, if mix chosen"""
	#exp = raw_input('Exp name?')
	#mixed = raw_input('mixed?(mix/no)')
	#exp_no = raw_input('Exp number?')
	##FILE_SIZE = raw_input('File size? (1Mb)')
	#duration = raw_input('Duration? (20s)')
	ip = "147.83.118.123"
	execute(run_exp_client,exp,mixed,exp_no,duration,ip,delay,size)
	if mixed == 'mix':
		execute(run_exp_client2,exp,mixed,exp_no,duration,ip,size)

def setup_nat(inface,outface):
	sudo('iptables -t nat -A POSTROUTING -o '+outface+' -j MASQUERADE')
	sudo('iptables -A FORWARD -i '+outface+' -p tcp --sport 80 -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
	sudo('iptables -A FORWARD -i '+inface+' -p tcp --dport 80 -o '+outface+' -j ACCEPT')


def setup_nat_8080(inface,outface):
        sudo('iptables -t nat -A POSTROUTING -o '+outface+' -j MASQUERADE')
	sudo('iptables -A FORWARD -i '+outface+' -p tcp --sport 8080 -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
        sudo('iptables -A FORWARD -i '+inface+' -p tcp --dport 8080 -o '+outface+' -j ACCEPT')


def clear_nat(inface,outface):
	with warn_only():
		sudo('iptables -t nat -D POSTROUTING -o '+outface+' -j MASQUERADE')
        	sudo('iptables -D FORWARD -i '+outface+' -p tcp --sport 80 -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
        	sudo('iptables -D FORWARD -i '+inface+' -p tcp --dport 80 -o '+outface+' -j ACCEPT')

def clear_nat_8080(inface,outface):
	with warn_only():
        	sudo('iptables -t nat -D POSTROUTING -o '+outface+' -j MASQUERADE')
        	sudo('iptables -D FORWARD -i '+outface+' -p tcp --sport 8080 -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
        	sudo('iptables -D FORWARD -i '+inface+' -p tcp --dport 8080 -o '+outface+' -j ACCEPT')

@roles('router')
def restore_nat():
	execute(setup_nat,inface='enx00e04c534458',outface='enp0s25')
	execute(setup_nat_8080,inface='enx00e04c534458',outface='enp0s25')

@roles('router')
def delete_nat():
	execute(clear_nat,inface='enx00e04c534458',outface='enp0s25')
	execute(clear_nat_8080,inface='enx00e04c534458',outface='enp0s25')


def setup_limit():
	 with cd('roc/tunneling/'):
                sudo('./tc_bandwidth_'+env.roles[0]+'.bash start')	

def clear_limit():
         with cd('roc/tunneling/'):
                sudo('./tc_bandwidth_'+env.roles[0]+'.bash stop')

@roles('router')
def sync():
	"""Sync exp result folders from client to router"""
	sudo("iptables-save > iptables.rules")
	sudo("iptables -F")
	run('eval $(ssh-agent) && ssh-add ~/.ssh/exp && rsync -rz xarokk1@192.168.240.2:~/manos/primary/wrk2/exps /home/xarokk/manos/.')
	run('rsync -rz xarokk1@192.168.240.2:~/manos/secondary/wrk2/exps /home/xarokk/manos/.')
	sudo("iptables-restore < iptables.rules")

