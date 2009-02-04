
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Stress1 {
    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "stress1" ).drop();
    }

    public static void validate() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBObject obj = new BasicDBObject();
        obj.put("date", 1 );
        DBCursor cursor = m.getCollection( "stress1" ).find().sort( obj );

        for( int i=0; i<50000; i++) {
            assert cursor.hasNext();
            DBObject o = cursor.next();
            int id = ((Integer)o.get( "id" )).intValue();
            if( id < 10000 ) {
                assert o.get( "subarray" ) instanceof String;
                assert o.get( "subarray" ).toString().equals( "foo" + id );
            }
            else
                assert o.get( "subarray" ) instanceof Object[];
        }

        assert !cursor.hasNext();
    }
}
