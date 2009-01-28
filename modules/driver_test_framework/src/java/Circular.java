
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Circular {
    public static void setup() 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "a" ).drop();
        m.getCollection( "b" ).drop();
        m.getCollection( "c" ).drop();
    }

    public static void main( String[] args ) 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBCollection coll1 = m.getCollection( "a" );
        DBCollection coll2 = null;
        coll2 = (DBCollection)coll2.findOne().get( "c" );
        MyAsserts.assertEquals( 1, ((Integer)coll2.findOne().get( "c" )).intValue() );

        DBCollection coll3 = m.getCollection( "c" );
        MyAsserts.assertEquals( 2, ((Integer)((DBObject)((DBObject)coll3.findOne().get( "thiz" )).get( "thiz" )).get( "that" )).intValue() );
    }
}
