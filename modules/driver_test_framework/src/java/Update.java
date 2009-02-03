
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Update {
    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBCollection c = m.getCollection( "foo" );
        c.drop();

        DBObject obj = new BasicDBObject();
        obj.put( "x", 1 );
        c.save( obj );
    }

    public static void validate() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        DBCollection c = m.getCollection( "foo" );

        DBObject sortObj = new BasicDBObject();
        sortObj.put( "x", 1 );
        DBCursor cursor = c.find().sort( sortObj );
        DBObject obj1 = cursor.next();

        assert ((Integer)obj1.get( "x" )).intValue() == 1;
        assert ((Integer)obj1.get( "y" )).intValue() == 2;

        obj1 = cursor.next();
        assert ((Integer)obj1.get( "x" )).intValue() == 4;
        assert ((Integer)obj1.get( "y" )).intValue() == 1;

        assert !cursor.hasNext();
    }
}
