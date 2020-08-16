package main.java;

public class Controller {
	int myId;
	String name;
	
	public Controller() {
		myId = 100;
		name = new String("This is my name");
	}
	
	public int getId() {
		return myId;
	}
	
	public String getName() {
		return name;
	}

}
