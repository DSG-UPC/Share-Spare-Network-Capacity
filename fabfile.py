#!/usr/bin/env python
from fabric.api import env, run, local, roles, execute, sudo, warn_only
from fabric.context_managers import cd
from time import sleep
#from datetime import datetime as dt
##HOUR = datetime.timedelta(minutes=2).now().time().strftime('%H%M')
##EXP_HOUR = (datetime.timedelta(minutes=2)+datetime.datetime.now()).time().strftime('%H%M') 

clears = ['clear_codel','clear_ipip','clear_sfq','clear_tcplp']
setups = ['setup_codel','setup_ipip','setup_sfq','setup_tcplp']
exps = ['run_exp']
__all__ =  clears+setups+exps+['sync']


env.key_filename = '/home/xarokk/.ssh/exp'
env.user = 'user'

env.roledefs = {
	'server':['xarokk2@147.83.118.124'],
	'client':['user@192.168.240.2'],
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


@roles('server')
def setup_ipip_server():
	with cd('roc/tunneling/'):
                sudo('./ipip-server.sh')

@roles('router')
def setup_ipip_router():
	execute(clear_nat,inface='enx00e04c534458',outface='enp0s25')
	with cd('roc/tunneling/'):
                sudo('./ipip-client.sh')
	execute(setup_nat,inface='enx00e04c534458',outface='ipiptun1')

def setup_ipip():
	execute(setup_ipip_router)
	execute(setup_ipip_server)

@roles('router')
def clear_ipip_router():
	execute(clear_nat,inface='enx00e04c534458',outface='ipiptun1')
	sudo('ip tun del ipiptun1')
	execute(setup_nat,inface='enx00e04c534458',outface='enp0s25')

@roles('server')
def clear_ipip_server():
	sudo('ip tun del ipiptun1')

def clear_ipip():
        execute(clear_ipip_router)
        execute(clear_ipip_server)

@roles('router')
def setup_codel():
        with cd('roc/tunneling/'):
                sudo('./tc_codel.bash start')

@roles('router')
def clear_codel():
	with cd('roc/tunneling/'):
                sudo('./tc_codel.bash stop')

@roles('router')
def setup_sfq():
        with cd('roc/tunneling/'):
                sudo('./tc_sfq.bash start')

@roles('router')
def clear_sfq():
        with cd('roc/tunneling/'):
                sudo('./tc_sfq.bash stop')

@roles('server')
def setup_tcplp_server():
        with cd('roc/tunneling/tcp_lp'):
                sudo('screen -S tcplp -d -m ./simpletun_tcplp -i tcplp -s')
        sudo('ifconfig tcplp 192.168.10.1/24 up')

@roles('router')
def setup_tcplp_router():
	#sudo('screen -wipe')
        with cd('roc/tunneling/tcp_lp'):
                run('sudo screen -S tcplp -d -m ./simpletun_tcplp -i tcplp -c 147.83.118.124')
	with warn_only():
		local('sudo screen -ls')
        #sudo('sudo ifconfig -a')
        run('sudo ifconfig tcplp 192.168.10.2/24 up')
	execute(clear_nat,inface='enx00e04c534458',outface='enp0s25')
	execute(setup_nat,inface='enx00e04c534458',outface='tcplp')

def setup_tcplp():
	execute(setup_tcplp_server)
	execute(setup_tcplp_router)

@roles('router')
def clear_tcplp_router():
	sudo('ifconfig tcplp down')
	sudo('sudo screen -X -S tcplp quit')
        execute(clear_nat,inface='enx00e04c534458',outface='tcplp')
	execute(setup_nat,inface='enx00e04c534458',outface='enp0s25')


@roles('server')
def clear_tcplp_server():
	sudo('ifconfig tcplp down')
	sudo('sudo screen -X -S tcplp quit')

def clear_tcplp():
        execute(clear_tcplp_router)
        execute(clear_tcplp_server)

@roles('client')
def run_exp_client():
	if EXP in ['ipip','tcplp','ledbat']:
		IP = "192.168.10.1"
	with cd('/home/user/manos/wrk2'):
                cmd_env = 'env dir='+EXP+' num='+EXP_NO+' mixed='+MIXED+' '
                cmd_wrk = ' ./wrk -t1 -c5 -d'+DURATION+' -R5 --latency --script scripts/report.lua '
		cmd_wrk_url = ' http://'+IP+'/02Mb.html '
		cmd =  cmd_env+cmd_wrk+cmd_wrk_url
		run('echo '+cmd+' > command')
		run('at now + 2 minutes < command')

@roles('client')
def run_exp_client2():
	if EXP in ['ipip','tcplp','ledbat']:
                IP = "192.168.10.1"
        with cd('/home/user/manos/wrk2'):
		cmd_wrk = ' ./wrk -t1 -c25 -d'+DURATION+' -R25'
                cmd_wrk_url = ' http://'+IP+'/004Mb.html '
                cmd =  cmd_wrk+cmd_wrk_url
                run('echo '+cmd+' > command')
                run('at now + 2 minutes < command')

@roles('router')
def run_exp_router():
	if EXP in ['ipip','tcplp','ledbat']:
                IP = "192.168.10.1"
	with cd('/home/xarokk/manos/wrk2'):
                cmd_wrk = ' ./wrk -t1 -c25 -d'+DURATION+' -R25'
                cmd_wrk_url = ' http://'+IP+'/004Mb.html '
                cmd =  cmd_wrk+cmd_wrk_url
                run('echo '+cmd+' > command')
                run('at now + 2 minutes < command')

def run_exp():
	EXP = raw_input('Exp name?')
	MIXED = raw_input('mixed?(mix/no)')
	EXP_NO = raw_input('Exp number?')
	#FILE_SIZE = raw_input('File size? (1Mb)')
	DURATION = raw_input('Duration? (20s)')
	IP = "147.83.118.124"
	execute(run_exp_client)
	execute(run_exp_client2)

def setup_nat(inface,outface):
	sudo('iptables -t nat -A POSTROUTING -o '+outface+' -j MASQUERADE')
	sudo('iptables -A FORWARD -i '+outface+' -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
	sudo('iptables -A FORWARD -i '+inface+' -o '+outface+' -j ACCEPT')

def clear_nat(inface,outface):
	sudo('iptables -t nat -D POSTROUTING -o '+outface+' -j MASQUERADE')
        sudo('iptables -D FORWARD -i '+outface+' -o '+inface+' -m state --state RELATED,ESTABLISHED -j ACCEPT')
        sudo('iptables -D FORWARD -i '+inface+' -o '+outface+' -j ACCEPT')

@roles('router')
def restore_nat():
	execute(setup_nat,inface='enx00e04c534458',outface='enp0s25')

@roles('router')
def sync():
	run('rsync -rz user@192.168.240.2:~/manos/wrk2/exps /home/xarokk/manos/.')

