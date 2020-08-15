package test.java;

import org.junit.Test;

import main.java.Controller;

import static org.junit.Assert.fail;
import static org.junit.Assert.assertEquals;

public class ControllerTest {

	@Test
	public void testConstruction() {
		//fail("Not yet implemented");
	}
	
	@Test
	public void test_PassingCondition() {
		Controller c = new Controller();
		assertEquals(100,c.getId());
		
	}

}
