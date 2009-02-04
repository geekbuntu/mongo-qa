
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Find1 {
    public static void setup() 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBCollection c = m.getCollection( "c" );
        c.drop();

        for( int i = 5; i<= 15; i++ ) {
            DBObject obj = new BasicDBObject();
            obj.put( "x", 0 );
            obj.put( "y", i );
            obj.put( "z", (char)(i+64) + "" );
            c.save( obj );
        }

        for( int i = 1; i<= 50; i++ ) {
            DBObject obj = new BasicDBObject();
            obj.put( "x", 1 );
            obj.put( "y", i );
            obj.put( "z", (char)(i+64) + "" );
            c.save( obj );
        }

        for( int i = 5; i<= 15; i++ ) {
            DBObject obj = new BasicDBObject();
            obj.put( "x", 2 );
            obj.put( "y", i );
            obj.put( "z", (char)(i+64) + "" );
            c.save( obj );
        }
    }

    public static void validate() {
        return;
    }
}
