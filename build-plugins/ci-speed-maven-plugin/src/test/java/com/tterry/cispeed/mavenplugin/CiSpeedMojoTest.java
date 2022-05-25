package com.tterry.cispeed.mavenplugin;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.UUID;

public class CiSpeedMojoTest {

    @Test
    @DisplayName("Supposed to do something")
    public void testDoThing(){

        CiSpeedMojo mojo = new CiSpeedMojo(
                "",
                "tim-test",
                UUID.randomUUID().toString(),
                new File("./target/surefire-reports"),
                "TEST.*\\.xml");
        try{
            mojo.execute();
        }
        catch(Exception e){
            System.err.println(e);
        }
    }

}
