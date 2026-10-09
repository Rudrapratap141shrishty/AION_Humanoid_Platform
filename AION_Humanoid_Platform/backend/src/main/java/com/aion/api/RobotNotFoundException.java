package com.aion.api;

public class RobotNotFoundException extends RuntimeException {
    public RobotNotFoundException(Long id) {
        super("Robot project " + id + " was not found");
    }
}
