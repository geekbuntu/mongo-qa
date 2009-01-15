
import os
import sys
import subprocess
from datetime import datetime

ID = str( datetime.now() )

TEST_DIR = "/src"
VALIDATION_DIR = "/validate"
OUTPUT_DIR = "/out"
TEMP_FILE = "/temp_" + ID

class Renderer :
    def __init__(self, output, p_output, report):
        if os.path.exists( TEMP_FILE ):
            self.temp = open( TEMP_FILE, 'r' )
        else:
            self.temp = None
        if os.path.exists( output ):
            self.output = open( output, 'r' )
        else:
            self.output = None
        if os.path.exists( p_output ):
            self.p_output = open( p_output, 'r' )
        else:
            self.p_output = None
                
        self.report = open( report, 'w' )

    def render_header( self, test, driver ):
        self.report.write( "RESULTS FOR " + test + "\n" )
        self.report.write( "\tRUN BY: " + driver + "\n" )
        self.report.write( "\tDATE: " + ID + "\n\n" )

    def render_diff( self ):
        if not self.p_output:
            return

        # create diff
        diffcount = 0
        for line1 in self.p_output:
            line2 = self.output.readline()
            if line2 != line1 :
                self.report.write( "L" + str(count) + ":\n" )
                self.report.write( "> " + line1 + "\n" )
                self.report.write( "< " + line2 + "\n" )
                diffcount += 1

        self.report.write( "\t# incorrect output lines: " + str(diffcount) +"\n\n" )

    # gather reporting info at the end of the output
    def get_stats( self ):
        extra = {}
        if not self.output:
            return extra

        for line in self.output:
            temp = line.split( ":" )
            if len( temp ) < 2:
                continue
            extra[ temp[0].lstrip() ] = temp[1].lstrip()
            
        return extra


    def render_stats( self, result ):
        self.report.write( "measured by tester.py: \n" )
        self.report.write( "\tbegintime:  " + str(result[ "begin" ]) + "\n" )
        self.report.write( "\tendtime: " + str(result[ "end" ]) + "\n" )
        self.report.write( "\ttotaltime:     " + str(result[ "end" ] - result[ "begin" ]) + "\n\n" )
        self.report.write( "\tok: " + str(result["exit_code"]) +"\n\n" )
        
        stats = self.get_stats()
        self.report.write( "measured by driver: \n" )
        for i in [ "begintime", "endtime", "totaltime", "ok" ]:
            if "begintime" in stats:
                self.report.write( "\t" + i + ":  " + stats[ i ] + "\n" )
            else:
                self.report.write( "\t" + i + ":  --no " + i + " recorded--\n" )


    def render_validation( self, result ):
        if not result: 
            self.report.write( "\n\nERROR!  COULD NOT RUN VALIDATE!\n" )
        elif result[ "exit_code" ] == 0:
            self.report.write( "\n\nPASSED VALIDATION\n" )
        else:
            self.report.write( "\n\nFAILED VALIDATION\n" )
            for line in self.temp:
                self.report.write( line )


    def cleanup( self ):
        if self.temp:
            self.temp.close()
        if os.path.exists( TEMP_FILE ):
            os.remove( TEMP_FILE )
        if self.output:
            self.output.close()
        if self.p_output:
            self.p_output.close()
        if self.report:
            self.report.close()


class Driver:
    def __init__( self, d ):
        try:
            temp = d.split( "=" )
            self.name = temp[0]
            self.path = temp[1]
        except IndexError:
            print "improperly formatted argument: " + driver + ".  skipping..."

    def is_valid( self ):
        return self.name != None and self.path != None

    def get_dir( self, test_dir ):
        dir = test_dir + "/" + self.name
        if not os.path.exists( dir ):
            os.mkdir( dir )
        return dir

    def get_path( self ):
        return self.path

    def get_name( self ):
        return self.name

    def get_unique_path( self, test_dir, test ):
        # a unique location for this driver/test/run's files:
        #     TEST_DIR/driver_name/test_ID
        driver_dir = self.get_dir( test_dir );
        return driver_dir + "/" + test + "_" + ID


class Framework:
    def __init__( self ):
        self.test_dir = os.curdir + TEST_DIR
        self.tests = os.listdir( self.test_dir + VALIDATION_DIR )

    # run all tests on all drivers
    def run_all( self ):
        for d in sys.argv[1:]:
            driver = Driver( d )
            if not driver.is_valid():
                continue

            self.run_all_driver( driver );

    # run all tests on a given driver
    def run_all_driver( self, driver ):
        for test in self.tests:
            self.run_test( driver, test )

    # run a specific test on a given driver
    def run_test( self, driver, test ):
        # file locations
        out = driver.get_unique_path( self.test_dir, test ) + ".out"
        report = driver.get_unique_path( self.test_dir, test ) + ".report"
        perfect_out = self.test_dir + OUTPUT_DIR + "/" + test + ".out"
        
        # run test
        timing_result = self.run_timed_test( driver, test, out, {} );

        # validate
        validation_result = None
        try:
            validation_result = self.run_validation_test( test, {} )
        except OSError:
            print "OSError: are the permissions correct for " + VALIDATION_DIR + "/" + test + "?\n"

        # report output
        r = Renderer( out, perfect_out, report )
        r.render_header( test, driver.get_name() )
        r.render_diff()
        r.render_stats( timing_result )
        r.render_validation( validation_result )
        r.cleanup()

    def run_timed_test( self, driver, test, output, result ):
        result[ "begin" ] = datetime.now()
        result[ "exit_code" ] = subprocess.call( [driver.get_path(), test, output] )
        result[ "end" ] = datetime.now()
        return result

    def run_validation_test( self, test, result ):
        validate_script = self.test_dir + "/validate/" + test
        result[ "exit_code" ] = subprocess.call( [ validate_script, TEMP_FILE ] )
        return result


f = Framework()
f.run_all()
