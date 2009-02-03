
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class Dbs {
    public static void setup() 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "dbs_1" ).drop();
        m.getCollection( "dbs_2" ).drop();
        m.getCollection( "dbs_3" ).drop();
    }

    public static void validate() 
        throws UnknownHostException {

        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        Set<String> s = m.getCollectionNames();
        assert s.contains( "dbs_2" );
        assert s.contains( "dbs_3" );
    }
}
