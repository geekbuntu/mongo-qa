
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Setup {
    public static void main( String[] args ) 
        throws UnknownHostException {

        if( args.length == 0 )
            return;

        String testname = args[0];
        if( testname.equals( "capped" ) )
            Capped.setup();
        else if( testname.equals( "circular" ) )
            Circular.setup(); 
        else if( testname.equals( "find" ) )
            Find.setup(); 
        else if( testname.equals( "remove" ) )
            Remove.setup();
        else if( testname.equals( "test1" ) )
            Test1.setup();
        else
            System.out.println( "No setup for "+testname );
    }
}
