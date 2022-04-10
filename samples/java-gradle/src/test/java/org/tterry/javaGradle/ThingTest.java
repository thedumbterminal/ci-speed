package org.tterry.javaGradle;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class ThingTest {

    @Test
    @DisplayName("Supposed to do something")
    public void testDoThing(){
        assertEquals(true, (new Thing()).doThing());
    }

    @Test
    @DisplayName("Supposed to not do something")
    public void testDoNothing(){
        assertEquals(false, (new Thing()).doThing());
    }
}

