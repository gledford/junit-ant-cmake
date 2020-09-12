package main.java;

public class Controller {
	int myId;
	String name;
	
	public Controller() {
		myId = 100;
		name = new String("This is my name");
	}
	
	public int getId() {
	    if (myId == 100) {
	        return myId; //done only to show branch coverage
	    }
		return myId;
	}
	
	public String getName() {
		return name;
	}

}
