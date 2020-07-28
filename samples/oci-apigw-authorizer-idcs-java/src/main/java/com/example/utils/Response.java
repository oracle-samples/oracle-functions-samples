/*
# oci-apigw-authorizer-idcs-java version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.utils;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;

public class Response {
    private final HttpURLConnection _connection;

    Response(final HttpURLConnection connection) {
        _connection = connection;
    }

    public void close() throws IOException {
        _connection.disconnect();
    }

    public String getHeader(final String name) {
        return _connection.getHeaderField(name);
    }

    public InputStream getInputStream() throws IOException {
        return _connection.getInputStream();
    }

    public int getStatus() {
        try {
            return _connection.getResponseCode();
        } catch (IOException e) {
            return 404;
        }
    }


    public String getResponseBodyAsString(final String encoding)
        throws Exception {
        StringBuffer sb = new StringBuffer();
        BufferedReader reader = new BufferedReader(new InputStreamReader(
            _connection.getInputStream(), encoding));
        String line = null;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        return sb.toString();
    }
}
