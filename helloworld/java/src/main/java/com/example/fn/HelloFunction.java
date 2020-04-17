/*
** HelloFunction version 1.0.
**
** Copyright (c) 2020 Oracle, Inc.
** Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

public class HelloFunction {

    public String handleRequest(String input) {
        System.out.println("Entering Java HelloFunction::handleRequest");
        System.out.println("Value of input is " + input);
        String name = (input == null || input.isEmpty()) ? "world"  : input;

        System.out.println("Value of name is " + name);
        System.out.println("Exiting Java HelloFunction::handleRequest");
        return "Hello, " + name + "!";
    }

}
