<?php
        $file = $_GET['f'];
        $file = preg_replace('![^a-zA-Z0-9-_]!', '', $file);

        if($_GET['h']) {
          $hours = floatval($_GET['h']);
          $time = time() - 60 * 60 * $hours;
        } else if($_GET['d']) {
          $time = strtotime($_GET['d']);
        }


        $file = 'data';

        $command = "rrdtool graph - -a PNG";
        $command .= " -w 800 -h 240 -v \"Time (in ms)\"";
        $command .= " -l 0";
        #$command .= " -u 30 -r";
        $command .= " -s ".$time;

        $command .= " DEF:q1=$file.rrd:q1:AVERAGE";
        $command .= " DEF:q2=$file.rrd:q2:AVERAGE";
        $command .= " DEF:q3=$file.rrd:q3:AVERAGE";
        $command .= " DEF:lo=$file.rrd:lo:AVERAGE";
        $command .= " DEF:hi=$file.rrd:hi:AVERAGE";

        $command .= " CDEF:qbt=q1,lo,-";
        $command .= " CDEF:qlo=q2,q1,-";
        $command .= " CDEF:qhi=q3,q2,-";
        $command .= " CDEF:qtp=hi,q3,-";

        $command .= " AREA:lo";
        $command .= " AREA:qbt#ddffdd::STACK";
        $command .= " AREA:qlo#99ff99::STACK";
        $command .= " AREA:qhi#ff9999::STACK";
        #$command .= " AREA:qtp#ffdddd::STACK";

        $command .= " LINE0.8:q2#333333";

        // print $command;
        // exit;

        if ($_GET['debug']){

                header("Content-type: text/plain");
                echo "$command";

        }else{
                header("Content-type: image/png");
                passthru($command);
        }
?>
