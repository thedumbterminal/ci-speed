package com.tterry.mavencispeedsample;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ThingTest {

    @Test
    @DisplayName("Example pass")
    public void testPass(){
        assertTrue(true);
    }

    @Test
    @DisplayName("Example failure")
    public void testFailure(){
        fail();
    }

    @Test
    @DisplayName("Example exception")
    public void testException() throws Exception{
        throw new Exception("boom!");
    }
}
