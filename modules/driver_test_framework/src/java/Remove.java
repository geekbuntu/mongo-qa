
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Remove {

    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/remove" ) );
        m.getCollection( "remove1" ).drop();
        m.getCollection( "remove2" ).drop();

        DBCollection coll1 = m.getCollection( "remove1" );
        for( int i=0; i<50; i++) {
            DBObject obj = new BasicDBObject();
            obj.put( "a", i );
            coll1.save( obj );
        }

        DBCollection coll2 = m.getCollection( "remove2" );
        DBObject obj1 = new BasicDBObject();
        obj1.put( "a", 3 );
        obj1.put( "b", 1 );
        coll2.save( obj1 );
        DBObject obj2 = new BasicDBObject();
        obj2.put( "a", 3 );
        obj2.put( "b", 3 );
        coll2.save( obj2 );
        DBObject obj3 = new BasicDBObject();
        obj3.put( "a", 2 );
        obj3.put( "b", 3 );
        coll2.save( obj3 );
        DBObject obj4 = new BasicDBObject();
        obj4.put( "b", 3 );
        coll2.save( obj4 );
    }

    public static void main( String[] args ) 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/remove" ) );
        DBCollection coll1 = m.getCollection( "remove1" );

        MyAsserts.assertEquals( 0, coll1.find().count() ); 
        
        DBCollection coll2 = m.getCollection( "remove2" );
        MyAsserts.assertEquals( 2, coll2.find().count() ); 

        DBObject obj = new BasicDBObject();
        obj.put( "b", 3 );
        MyAsserts.assertTrue( coll2.findOne( obj ) != null );
        obj.put( "a", 2 );
        MyAsserts.assertTrue( coll2.findOne( obj ) != null );
    }
}
