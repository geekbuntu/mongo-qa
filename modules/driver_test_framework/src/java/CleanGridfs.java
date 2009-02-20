
import java.util.*;
import java.net.*;

import com.mongodb.*;
import com.mongodb.util.*;

public class CleanGridfs {
    public static void main(String[] args) 
        throws UnknownHostException {
        Mongo m = new Mongo( new DBAddress( "127.0.0.1:27017/driver_test_framework" ) );
        m.getCollection( "fs.files" ).drop();
        m.getCollection( "fs.chunks" ).drop();
    }
}
