
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Count1 {
 
    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "test1" ).drop();

        DBCollection foo = m.getCollection( "test2" );
        foo.drop();
        DBObject obj = new BasicDBObject();
        obj.put( "name", "a" );
        foo.save( obj );

        foo = m.getCollection( "test3" );
        foo.drop();
        for( int i=0; i<100; i++) {
            DBObject obj2 = new BasicDBObject();
            obj2.put( "i", i );
            foo.save( obj2 );
        }
    }

    public static void validate() {
        return;
    }
}
