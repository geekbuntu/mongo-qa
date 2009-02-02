
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Find {
    public static void setup() 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "test" ).drop();
    }

    public static void main( String[] args ) 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBCollection coll1 = m.getCollection( "test" );

        DBCursor cursor = coll1.find();
        MyAsserts.assertEquals( 2, ((Integer)cursor.next().get( "a" )).intValue() );
        MyAsserts.assertEquals( false, cursor.hasNext() );
    }
}
