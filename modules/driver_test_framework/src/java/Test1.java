
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Test1 {
    public static void main( String[] args ) 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/test1" ) );
        DBCollection coll = m.getCollection( "part1" );

        DBObject sortObj = new BasicDBObject();
        sortObj.put( "x", 1 );
        DBCursor c = coll.find().sort( sortObj );

        int count = 0;
        while( c.hasNext() ) {
            DBObject o = c.next();
            int z = ((Integer)o.get( "x" )).intValue();
            MyAsserts.assertEquals( z, count );
            count++;
        }
        MyAsserts.assertEquals( count, 100 );
    }
}
