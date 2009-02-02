
import os
import sys
import subprocess
from datetime import datetime

os.environ["CLASSPATH"] = "build:lib/mongo.jar"

ID = datetime.now().isoformat()

TEST_DIR = "src"
PREP_DIR = "setup"
VALIDATION_DIR = "validate"
OUTPUT_DIR = "output"
TEMP_FILE = os.getcwd() + "/temp_" + ID

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

    def render( self, test, driver, timing, diff, valid ):
        self.render_header( test, driver )
        self.render_stats( timing )
        self.render_diff( diff )
        self.render_validation( valid )
        self.cleanup()

    def render_header( self, test, driver ):
        self.report.write( "RESULTS FOR " + test + "\n" )
        self.report.write( "\tRUN BY: " + driver + "\n" )
        self.report.write( "\tDATE: " + ID + "\n\n" )

    def render_diff( self, diff ):
        if diff and diff[ "exit_code" ] > 0:
            self.report.write( "FAILED DIFF\n" )
            self.report.write( "\nNumber of incorrect output lines: " + str( diff[ "exit_code" ] ) +"\n\n" )

    # gather reporting info at the end of the output
    def get_stats( self ):
        extra = {}
        if not self.output:
            return extra

        for line in self.output:
            temp = line.split( ":" )
            if len( temp ) < 2:
                continue
            extra[ temp[0].lstrip() ] = line[len(temp[0]) + 1:].strip()

        return extra


    def render_stats( self, result ):
        self.report.write( "measured by tester.py: \n" )
        self.report.write( "\tbegintime: " + str(result[ "begin" ]) + "\n" )
        self.report.write( "\tendtime:   " + str(result[ "end" ]) + "\n" )
        self.report.write( "\ttotaltime: " + str(result[ "end" ] - result[ "begin" ]) + "\n" )
        self.report.write( "\texit_code: " + str(result["exit_code"]) +"\n\n" )

        stats = self.get_stats()
        self.report.write( "measured by driver: \n" )
        for i in [ "begintime", "endtime", "totaltime", "exit_code" ]:
            padded_i = (i + ":").ljust(11)
            if i in stats:
                self.report.write( "\t" + padded_i + stats[ i ] + "\n" )
            else:
                self.report.write( "\t" + padded_i + "--no " + i + " recorded--\n" )


    def render_validation( self, result ):
        if not result:
            self.report.write( "\n\nERROR!  COULD NOT RUN VALIDATE!\n" )
        elif result[ "exit_code" ] == 0:
            self.report.write( "\n\nPASSED VALIDATION\n" )
        else:
            self.report.write( "\n\nFAILED VALIDATION\n" )
            if not self.temp:
                self.report.write( "no output\n" )
                return
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

class Summarizable:
    def __init__( self ):
        self.passes = 0
        self.total_tests = 0
        self.start_time = datetime.now()

    def summarize( self, name ):
        print name
        print "Time: " + str( self.get_time() )
        print "Total tests run: " + str( self.get_total() )
        print "Passes: " + str( self.get_passes() )
        print "Fails: " + str( self.get_fails() )
        print "----------------------------"
        if self.get_total() == 0:
            print "Percent passed: 100%"
        else:
            print "Percent passed: " + str( ( self.passes / self.total_tests ) * 100 ) + "%"

    def add_to_stats( self, passed ):
        if passed:
            self.passes += 1
        self.total_tests += 1
    def get_total( self ):
        return self.total_tests
    def get_passes( self ):
        return self.passes
    def get_fails( self ):
        return self.total_tests - self.passes
    def get_time( self ):
        return datetime.now() - self.start_time

class Driver (Summarizable):
    def __init__( self, name, path ):
        self.name = name
        self.path = path
        self.get_dir( OUTPUT_DIR )
        Summarizable.__init__( self )

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
        #     OUTPUT_DIR/driver_name/test_ID
        driver_dir = self.get_dir( test_dir )
        return driver_dir + "/" + ID + "_" + test

class Framework (Summarizable):
    def __init__( self ):
        self.test_dir = os.getcwd() + "/"
        self.tests = os.listdir( VALIDATION_DIR )
        Summarizable.__init__( self )

    # run all tests on all drivers
    def run_all( self, drivers ):
        passed = True
        for driver in drivers:
            if not driver.is_valid():
                continue

            passed = passed and self.run_all_driver( driver )
            if len( drivers ) != 1:
                driver.summarize( "Driver " + driver.get_name() )
        self.summarize( "\n----------------------------\nAll tests" )
        return passed

    # run all tests on a given driver
    def run_all_driver( self, driver ):
        passed = True
        for test in self.tests:
            # if there is a pre-test file to run, do so
            prep = PREP_DIR + "/" + test
            if os.path.exists( prep ):
                subprocess.call( [prep] )
            p = self.run_test( driver, test )
            if p:
                print test + ".",
            else:
                print test + "F",
            passed = passed and p
        return passed

    # run a specific test on a given driver
    def run_test( self, driver, test ):
        # file locations
        out = driver.get_unique_path( OUTPUT_DIR, test ) + ".out"
        report = driver.get_unique_path( OUTPUT_DIR, test ) + ".report"
        perfect_out = OUTPUT_DIR + "/" + test + ".out"

        # run test
        try:
            timing_result = self.run_timed_test( driver, test, out, {} )
        except:
            pass
        if not self.check_results( timing_result ):
            self.add_to_stats( False )
            driver.add_to_stats( False )
            print "driver " + driver.get_name() + " failed to run " + test
            return False

        # diff results
        if os.path.exists( perfect_out ):
            if os.path.exists( out ):
                diff_result = self.diff_test( open( out, "r" ), open( perfect_out, "r" ) )
        else:
            diff_result = { "exit_code" : 0 }
        if not self.check_results( diff_result ):
            print "driver " + driver.get_name() + ":" + test + " generated incorrect output"

        # validate
        validation_result = self.run_validation_test( test, {} )
        if not self.check_results( validation_result ):
            print "driver " + driver.get_name() + ":" + test + " failed validation"

        passed = self.check_results( validation_result ) and self.check_results( diff_result )
        self.add_to_stats( passed )
        driver.add_to_stats( passed )

        # report output
        r = Renderer( out, perfect_out, report )
        r.render( test, driver.get_name(), timing_result, diff_result, validation_result )
        return ( passed == 1 )

    def run_timed_test( self, driver, test, output, result ):
        old_path = os.getcwd()
        output = os.path.abspath(output)
        os.chdir(os.path.dirname(driver.get_path()))
        result[ "begin" ] = datetime.now()
        result[ "exit_code" ] = subprocess.call( [self.test_dir + driver.get_path(), test, output] )
        result[ "end" ] = datetime.now()
        os.chdir(old_path)
        return result

    def run_validation_test( self, test, result ):
        validate_script = VALIDATION_DIR + "/" + test
        result[ "exit_code" ] = subprocess.call( [ validate_script, TEMP_FILE ] )
        return result

    def diff_test( self, out1, out2 ):
        result = {}
        count = 0
        for line2 in out2:
            line1 = out1.readline()
            if line2 != line1 :
                count += 1
        result[ "exit_code" ] = count
        return result

    def check_results( self, result ):
        if result and "exit_code" in result and result[ "exit_code" ] == 0:
            return True
        return False



if len( sys.argv ) < 2:
    print "No drivers given, exiting"
    exit( 0 )

driver_num = 1
drivers = []
for d in sys.argv[1:]:
    if d.find( "=" ) > 0:
        temp = d.split( "=" )
        drivers.append( Driver( temp[0], temp[1] ) )
    else:
        drivers.append( Driver( "driver" + str( driver_num ), d ) )

    driver_num += 1


f = Framework()
passed = f.run_all( drivers )
if passed:
    exit( 0 )
else:
    exit( 1 )
