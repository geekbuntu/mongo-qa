
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Capped {
    public static void main( String[] args ) 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/capped" ) );
        DBCollection coll1 = m.getCollection( "capped1" );

        MyAsserts.assertEquals( 2, coll1.find().count() ); 
        
        DBObject sortObj = new BasicDBObject();
        sortObj.put( "$natural", 1 );
        MyAsserts.assertEquals( 1, ((Integer)coll1.find().sort( sortObj ).next().get( "x" )).intValue() );
        sortObj.put( "$natural", -1 );
        MyAsserts.assertEquals( 2, ((Integer)coll1.find().sort( sortObj ).next().get( "x" )).intValue() );

        // make sure it's capped 
        for( int i=0; i<100; i++ ) {
            DBObject obj = new BasicDBObject();
            obj.put( "a" , i );
            coll1.save( obj );
        }

        MyAsserts.assertTrue( 15 > coll1.find().count() );

        sortObj.put( "$natural", 1 );
        DBCursor cursor = coll1.find().sort( sortObj );
        int prev = 0;
        while( cursor.hasNext() ) {
            int current = ((Integer)cursor.next().get( "a" )).intValue();
            MyAsserts.assertTrue( prev < current );
            prev = current;
        }
    }
}
