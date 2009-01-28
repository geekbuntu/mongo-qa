
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

        MyAsserts.assertEquals( 1, coll1.find().count() );

        ObjectId oid = (ObjectId)coll1.find().next().get( "_id" );
        DBObject obj = new BasicDBObject();
        obj.put( "_id", oid );

        MyAsserts.assertEquals( 2, ((Integer)coll1.find( obj ).next().get( "a" )).intValue() );

        DBObject fields = new BasicDBObject();
        fields.put( "n", 1 );
        MyAsserts.assertEquals( 2, ((Integer)coll1.find( obj, fields, 0, 1 ).next().get( "a" )).intValue() );
    }
}
