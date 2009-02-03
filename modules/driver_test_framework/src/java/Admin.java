
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Admin {
    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "tester" ).drop();

        DBObject foo = new BasicDBObject();
        foo.put( "profile", 1 );
        m.getCollection( "$cmd" ).findOne( foo );
    }

    public static void validate() {
        return;
    }
}
