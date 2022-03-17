package com.example.fn;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.lang.InterruptedException;
import org.json.JSONObject;
import java.util.*;

public class BasicAuth {
    public static class Input {
        public String type;
        public String token;
    }

    public static class Result {
        public boolean active = false;
        public String principal;
        public String[] scope;
        public String expiresAt;
    }

    private static final String TOKEN_PREFIX = "Basic ";
    private static final String IDCS_URL = ResourceServerConfig.IDCS_URL;

    public String[] getUserDetailsFromToken(String token) {
        String data = token.substring(TOKEN_PREFIX.length());
        String[] user = new String(Base64.getDecoder().decode(data)).split(":", 2);
        return user;
    }

    public Result handleRequest(Input input) throws UnsupportedEncodingException, InterruptedException {
        Result returnValue = new Result();

        if (input.token == null || !input.token.startsWith(TOKEN_PREFIX)) {
            returnValue.active = false;
            System.out.println("Request error, missing credentials");
            return returnValue;
        }

        String[] user = getUserDetailsFromToken(input.token);
        if (user.length != 2 || user[0] == null || user[0].isEmpty() || user[1] == null || user[1].isEmpty()) {
            System.out.println("Request error username or password missing");
            return returnValue;
        }

        String username = user[0];
        String password = user[1];
        String clientId = ResourceServerConfig.CLIENT_ID;
        String clientSecret = ResourceServerConfig.CLIENT_SECRET;
        String authzHdrVal = clientId + ":" + clientSecret;
        String idcsScope = ResourceServerConfig.SCOPE_AUD;

        String reqBody =   "grant_type=password" +
                "&username=" + username +
                "&password=" + password +
                "&scope=" + idcsScope;

        try {
            HttpClient client = HttpClient.newHttpClient();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(IDCS_URL))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .header("Authorization", "Basic " + Base64.getEncoder().encodeToString(authzHdrVal.getBytes("UTF-8")))
                    .POST(HttpRequest.BodyPublishers.ofString(reqBody))
                    .build();

            HttpResponse<String> response = client.send(    request,
                    HttpResponse.BodyHandlers.ofString() );


            if (response.statusCode() == 200) {

                String responseString = (String) response.body();
                String[] chunks = responseString.split("\\.");
                String respjson = new String(Base64.getUrlDecoder().decode(chunks[1]));
                JSONObject payload = new JSONObject(respjson);
                Date expTime = new Date(payload.getLong("exp")*1000);

                returnValue.principal = payload.getString("sub");
                returnValue.scope = payload.getString("scope").split(" ");
                returnValue.expiresAt = expTime.toString();
                returnValue.active = true;
                System.out.println("Authentication successful");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return returnValue;
    }
}