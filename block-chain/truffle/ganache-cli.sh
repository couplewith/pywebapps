PWD=$(pwd)
PFILE="_ganache.pid"


cd $PWD

function start(){
    ganache-cli  -h 0.0.0.0 -p 8545 > _ganache.log  &
    PID=$!
    echo " ganache-cli pid : $PID"
    echo "$PID" > $PFILE
	status
   cat _ganache.log
}

function status() {

    PID=`ps -ef | grep "bin/ganache-cli"| grep -v "grep"| cut -d" " -f 8`
    if [ ! -z "$PID" ]
    then
        CNT=`ps -ef | grep -c "$PID"`
        echo " >> process running :[pid: $PID] cnt: $CNT "
	else
        echo " !! process stopped :[pid: $PID] cnt: $CNT "
    fi
}

function pscheck() {

    if [ -f "$PFILE" ]
    then
        echo " $PFILE exists !!"
        exit
    fi
}

function stop()
{
	if [ -f "$PFILE" ]
    then
        PID=`cat "$PFILE" 2>/dev/null`
	else
        PID=`ps -ef | grep "bin/ganache-cli"| grep -v "grep"| cut -d" " -f 8`
	fi

	if [ ! -z $PID ]
	then
         ps -ef | grep "$PID"
         kill -9 "$PID"
		 rm -rf "$PFILE"
	fi

    status
}


# ---------------------------------
    OPT="${1-}"
	echo $OPT

    case "${OPT-}" in
        "status") 
           status
          ;;
        "start") 
           pscheck
           echo " $0 start ---------- "
           start
          ;;
        "stop") 
           stop
          ;;
       *)
	  echo " usage: $0 [start|stop|staus]"
          exit
          ;;
    esac


# truffle develop 으로 ganache를 기동 할 수도 있다.
#  이때 구동되는 포트는 9545 이다.
# ganache  instances list
