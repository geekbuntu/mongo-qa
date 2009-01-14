
import os
import sys
import subprocess
from datetime import datetime


def process_output( true_out , out , report , time ):
    report.write( "RESULTS FOR " + test + "\n\tRUN BY: " + driver_name + "\n\tDATE: " + time[ "id" ] + "\n\n" )

    # create diff
    count = 0
    diffcount = 0
    for line1 in true_out:
        line2 = out.readline()
        if line2 != line1 :
            report.write( "L" + str(count) + ":\n" )
            report.write( "> " + line1 + "\n" )
            report.write( "< " + line2 + "\n" )
            diffcount += 1
        count += 1

    report.write( "\t# incorrect output lines: " + str(diffcount) +"\n\n" )

    # gather reporting info at the end of the output
    extra = {}
    for line2 in out:
        temp = line2.split( ":" )
        if len( temp ) < 2:
            continue
        extra[ temp[0].lstrip() ] = temp[1].lstrip()

    return extra


def report_summary( report, time, stats, exit_code ):

    report.write( "measured by tester.py: \n" )
    report.write( "\tstarted:  " + str(time[ "begin" ]) + "\n" )
    report.write( "\tfinished: " + str(time[ "end" ]) + "\n" )
    report.write( "\tdiff:     " + str(time[ "end" ] - time[ "begin" ]) + "\n\n" )
    report.write( "\texit code: " + str(exit_code) +"\n\n" )

    report.write( "measured by driver: \n" )
    report.write( "\tstarted:  " + stats[ "begintime" ] + "\n" )
    report.write( "\tfinished: " + stats[ "endtime" ] + "\n" )
    report.write( "\tdiff:     " + stats[ "totaltime" ] + "\n\n" )
    report.write( "\texecuted ok: " + stats[ "ok" ] +"\n\n" )


def report_validation( report, exit_code, temp ):
    if exit_code == 0:
        report.write( "\n\nPASSED VALIDATION\n" )
    else:
        report.write( "\n\nFAILED VALIDATION\n" )
        temp.close();
        temp = open( "temp", 'r' )
        for line in temp:
            report.write( line );


test_dir = os.curdir + "/cmd_tests"
tests = os.listdir( test_dir + "/src" )

for driver in sys.argv[1:]:
    try:
        temp = driver.split( "=" )
        driver_name = temp[0]
        driver_path = temp[1]
    except IndexError:
        print "improperly formatted argument: " + driver + ".  skipping..."
        continue

    local_test_dir = test_dir + "/" + driver_name
    if not os.path.exists( local_test_dir ):
        os.mkdir( local_test_dir )

    for test in tests:
        t = { "id" : str( datetime.now() ) }
        test_path = local_test_dir + "/" + test[0:-4] + "_" + t[ "id" ]

        # files
        out = open( test_path + ".out" , 'w' )
        report = open( test_path + ".report", 'w' )

        # run test
        t[ "begin" ] = datetime.now()

        exit_code = subprocess.call( [driver_path, test], 0, None, None, out )

        t[ "end" ] = datetime.now()

        # report output
        out.close();
        out = open( test_path + ".out" , 'r' )
        true_out = open( test_dir + "/src/" + test , "r" )
        stats = process_output( true_out , out , report , t )
        report_summary( report, t, stats, exit_code )

        # validate
        temp = open( "temp", 'w' )
        validate_script = test_dir + "/validate/" + test[0:-4]
        print validate_script
        exit_code = subprocess.call( [ validate_script ], 0, None, None, temp )
        report_validation( report, exit_code, temp )

        # finish up
        temp.close()
        os.remove( "temp" )
        report.close()
        out.close()

