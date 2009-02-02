import java.lang.reflect.*;
import java.util.*;

public class Runner {

    private static String VALIDATE = "validate";
    private static String SETUP = "setup";

    public static void usage() {
        System.out.println( "Usage:\n" +
                            "\tjava Runner setup|validate testname [outputfile]" );
    }

    public static void main( String[] args ) {
        if( args.length < 2 ) {
            usage();
            System.exit( 1 );
        }

        int opt = 0;
        String cmd = args[0];

        String testname = args[1].substring( 0, 1 ).toUpperCase() +
            args[1].substring( 1 );

        Class c = null;
        try {
            c = Class.forName( testname );
        }
        catch( ClassNotFoundException e ) {
            e.printStackTrace();
            System.exit( 1 );
        }

        try {
            if( cmd.equals( VALIDATE ) ) {
                Method m = c.getDeclaredMethod( VALIDATE );
                m.invoke( null );
            }
            else if( cmd.equals( SETUP ) ) {
                Method m = c.getDeclaredMethod( SETUP );
                m.invoke( null );
            }
            else {
                usage();
                System.exit( 1 );
            }
        }
        catch( NoSuchMethodException e ) {
            e.printStackTrace();
            System.exit( 1 );
        }
        catch( IllegalAccessException e2 ) {
            e2.printStackTrace();
            System.exit( 1 );
        }
        catch( InvocationTargetException e3 ) {
            e3.printStackTrace();
            System.exit( 1 );
        }
    }
}