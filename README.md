# Experiments with fab
Fab is run the router between the client and the server.
As currently configured fab support the following commands:

    xarokk@Cellsim:~/roc/tunneling$ fab --list
    Available commands:

        clear_borrowing
        clear_codel
        clear_ipip
        clear_limit
        clear_sfq
        clear_tcplp
        clear_tcpvegas
        delete_nat
        restore_nat
        run_exp          Experiment traffic and background traffic from client, if mix chosen
        setup_borrowing
        setup_codel
        setup_ipip
        setup_limit
        setup_sfq
        setup_tcplp
        setup_tcpvegas
        sync             Sync exp result folders from client to router

When running an experiment the parameters are:

* ``exp``: name of experiment. Should be similar to the corresponding command you used for setup. For example to run the TCP-LP experiment the code is ``tcplp``
* ``mixed``: ``mix`` or ``no`` dependind if you want just the primary traffic or both primary and secondary 
* ``exp_no``: The number of the experiment. For new set of experiments is good to give a name in front. Like ``delay_1``
* ``duration``: the duration of the experiments. Typically used ``60s``


# Experiment workflow
Below are explained all the steps. For combining check also the script ``run_all.sh`` (it assumes the limit is already installed)


## Setup limit
Setup limit in server of router withe ``setup_limit`` command using role ``router`` or ``server``. Example:

    xarokk@Cellsim:~/roc/tunneling$ fab -R server setup_limit
    [xarokk2@147.83.118.124] Executing task 'setup_limit'
    [xarokk2@147.83.118.124] sudo: ./tc_bandwidth_server.bash start
    [xarokk2@147.83.118.124] out: sudo password:
    [xarokk2@147.83.118.124] out: Starting bandwidth shaping: done
    [xarokk2@147.83.118.124] out: 


    Done.
    Disconnecting from xarokk2@147.83.118.124... done.
**IMPORTANT**: In the setup it is not normal if the output has errors. Sometimes it happens with ``tcplp`` and ``tcpvegas``. Contact for degub.
## Setup experiment
Use the existing commands. For example:

    xarokk@Cellsim:~/roc/tunneling$ nano fabfile.py
    xarokk@Cellsim:~/roc/tunneling$ fab setup_ipip
    [xarokk@147.83.118.126] Executing task 'setup_ipip_router'
    [xarokk@147.83.118.126] sudo: ./ipip-client.sh
    ...

    Done.
    Disconnecting from xarokk2@147.83.118.124... done.
    Disconnecting from xarokk@147.83.118.126... done.

## Run Experiment
Use command with the corresponding arguments and wait for 3 mins until the experiment is done for sure:

    xarokk@Cellsim:~/roc/tunneling$ fab run_exp:exp=ipip,mixed=mix,expno=1,duration=60s; sleep 3m
  
## Sync Experiments
It needs to be run after one or all the experiment to put the data in the router in the folder /home/xarokk/manos/exps
You need to provide the usual password.

    xarokk@Cellsim:~/roc/tunneling$ fab sync
    
## Clear Setup
Use the existing commands. For example:

    xarokk@Cellsim:~/roc/tunneling$ fab clear_ipip
    [xarokk@147.83.118.126] Executing task 'clear_ipip_router'
    ...
    Done.
    Disconnecting from xarokk2@147.83.118.124... done.
    Disconnecting from xarokk@147.83.118.126... done.
  
**IMPORTANT**: In the clear it is  normal if the output has errors in ``tcplp`` and ``tcpvegas``. Don't worry about them. Everythin went fine.

## Clear limit
Clear limit in server of router withe ``clear_limit`` command using role ``router`` or ``server``. Example:

    xarokk@Cellsim:~/roc/tunneling$ fab -R server clear_limit
    [xarokk2@147.83.118.124] Executing task 'clear_limit'
    [xarokk2@147.83.118.124] sudo: ./tc_bandwidth_server.bash stop
    [xarokk2@147.83.118.124] out: sudo password:
    [xarokk2@147.83.118.124] out: Stopping bandwidth shaping: done
    [xarokk2@147.83.118.124] out: 


    Done.
    Disconnecting from xarokk2@147.83.118.124... done.
